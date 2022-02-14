import { IUser } from "../../shared/types/user";
import { hashPassword } from "../../server/src/common/auth";
import { IAudit } from "../../shared/types";
const fs = require("fs");
const r = require("rethinkdb");
var tunnel = require("tunnel-ssh");

const datasets: Record<string, any> = {
  all: [
    {
      name: "acl_permissions",
      data: "datasets/all/acl_permissions.json",
    },
    {
      name: "actants",
      data: "datasets/all/actants.json",
      indexes: [
        r.table("actants").indexCreate("class"),
        r.table("actants").indexCreate("label"),
        r
          .table("actants")
          .indexCreate(
            "data.actants.actant",
            r.row("data")("actants")("actant")
          ),
        r
          .table("actants")
          .indexCreate(
            "data.actions.action",
            r.row("data")("actions")("action")
          ),
        r.table("actants").indexCreate("data.tags", r.row("data")("tags")),
        r
          .table("actants")
          .indexCreate(
            "data.props.type.id",
            r.row("data")("props")("type")("id")
          ),
        r
          .table("actants")
          .indexCreate(
            "data.props.value.id",
            r.row("data")("props")("value")("id")
          ),
        r
          .table("actants")
          .indexCreate(
            "data.references.resource",
            r.row("data")("references")("resource")
          ),
        r
          .table("actants")
          .indexCreate("data.props.origin", r.row("data")("props")("origin")),
        r
          .table("actants")
          .indexCreate("data.territory.id", r.row("data")("territory")("id")),
        r
          .table("actants")
          .indexCreate("data.parent.id", r.row("data")("parent")("id")),
      ],
    },
    {
      name: "users",
      data: "datasets/all/users.json",
    },
    {
      name: "audits",
      data: "datasets/all/audits.json",
    },
  ],
};

const datasetId: string = process.argv[2];
const dbMode = process.argv[3];

const envData = require("dotenv").config({ path: `env/.env.${dbMode}` }).parsed;

const tablesToImport = datasets[datasetId];

console.log(`***importing dataset ${datasetId}***`);
console.log("");

function doIndex(statement: any, connection: any): Promise<any> {
  return new Promise((resolve) => {
    statement.run(connection, resolve);
  });
}

//-----------------------------------------------------------------------------
// Main
//-----------------------------------------------------------------------------

const importData = async () => {
  const config = {
    db: envData.DB_NAME,
    host: envData.DB_HOST,
    port: envData.DB_PORT,
    password: envData.DB_AUTH,
    tables: tablesToImport,
  };

  let conn:any = null;

  try {
    conn = await r.connect(config);

    // set default database
    conn.use(config.db);
    console.log(config);

    // Drop the database.
    try {
      await r.dbDrop(config.db).run(conn);
      console.log("database dropped");
    } catch (e) {
      console.log("database not dropped");
    }

    // Recreate the database
    try {
      await r.dbCreate(config.db).run(conn);
      console.log("database created");
    } catch (e) {
      console.log("database not created");
    }


    // Insert data to tables.
    for (let i = 0; i < config.tables.length; ++i) {
      const table = config.tables[i];

	  console.log(`table ${table.name} will be created`);
	  //console.log(conn);
	  
	  // Recreate the table
		try {
		  //await await r.tableCreate(table.name).run(conn);
		  r.tableCreate(table.name).run(conn,() => {
        console.log('xxx created');
		
		console.log(`table ${table.name} created`);

      let data = JSON.parse(fs.readFileSync(table.data));
	  //console.log(data)
	  
      if (table.name === "users") {
        data = data.map((user: IUser) => {
          user.password = hashPassword(user.password ? user.password : "");
          return user;
        });
      }

      if (table.name === "audits") {
        data = data.map((audit: IAudit) => {
          audit.date = new Date(audit.date);
          return audit;
        });
      }

      //await 
	  r.table(table.name).insert(data).run(conn, ()=> {
		  console.log(`data into the table ${table.name} inserted`);
		  //console.log(data)
	  });
      
		
	
		
      })
		  
		  
		  console.log(`table created`);
		} catch (e) {
		  console.log(`table not created ${e}`);
		}
		  

      
    }
  } catch (error) {
    console.log(error);
  } finally {
    console.log("closing connection");
    if (conn) {
      console.log("There is connection.");		
      conn.close();
	  console.log("There was connection.");
    }
  }
};

if (dbMode == "prod") {
  const tnl = tunnel(
    {
      host: envData.SSH_IP,
      port: 28015,
      dstPort: 28017,
      username: envData.SSH_USERNAME,
      password: envData.SSH_PASSWORD,
    },
    function (error: any, tnl: any) {
      console.log("in the tunnel");
      importData();
      tnl.close();
    }
  );
} else {
  importData();
}
