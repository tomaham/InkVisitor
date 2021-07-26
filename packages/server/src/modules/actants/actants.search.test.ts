import { testErroneousResponse } from "@modules/common.test";
import { BadParams } from "@shared/types/errors";
import request, { Response } from "supertest";
import { apiPath } from "../../common/constants";
import app from "../../Server";
import { supertestConfig } from "..";
import { Db } from "@service/RethinkDB";
import "ts-jest";
import { createAction } from "@service/shorthands";
import { deleteActants } from "@service/shorthands";
import { IActant, IAction, IStatement } from "@shared/types";
import { ActantType } from "@shared/enums";
import { getActantType } from "@models/factory";

describe("Actants search", function () {
  describe("empty data", () => {
    it("should return a BadParams error wrapped in IResponseGeneric", (done) => {
      return request(app)
        .post(`${apiPath}/actants/search`)
        .set("authorization", "Bearer " + supertestConfig.token)
        .expect("Content-Type", /json/)
        .expect(testErroneousResponse.bind(undefined, new BadParams("")))
        .then(() => done());
    });
  });
  describe("invalid request data(only class)", () => {
    it("should return a BadParams error wrapped in IResponseGeneric", (done) => {
      return request(app)
        .post(`${apiPath}/actants/search`)
        .send({ class: ActantType.Concept })
        .set("authorization", "Bearer " + supertestConfig.token)
        .expect("Content-Type", /json/)
        .expect(testErroneousResponse.bind(undefined, new BadParams("")))
        .then(() => done());
    });
  });
  describe("invalid class data", () => {
    it("should return a BadParams error wrapped in IResponseGeneric", (done) => {
      return request(app)
        .post(`${apiPath}/actants/search`)
        .send({ class: "something", label: "mn" })
        .set("authorization", "Bearer " + supertestConfig.token)
        .expect("Content-Type", /json/)
        .expect(testErroneousResponse.bind(undefined, new BadParams("")))
        .then(() => done());
    });
  });

  describe("search by params", () => {
    let db: Db;
    const rand = Math.random().toString();

    const actantData: IActant = {
      id: `testactant${rand}`,
      class: ActantType.Person,
      data: {},
      label: `testactant${rand}`,
    };

    const wantedLinkedActant: IActant = {
      id: `testactant2${rand}`,
      class: ActantType.Event,
      data: {},
      label: `testactant2${rand}`,
    };

    const actionData: IAction = {
      id: `testaction${rand}`,
      labels: [
        {
          id: `testlabel${rand}`,
          lang: "",
          value: `testlabel${rand}`,
        },
      ],
      note: "",
      parent: "",
      rulesActants: [],
      rulesProperties: [],
      types: [],
      valencies: [],
    };

    const statementData: IStatement = {
      class: ActantType.Statement,
      data: {
        actants: [
          {
            actant: actantData.id,
            certainty: "",
            elvl: "",
            id: actantData.id,
            position: "",
          },
          {
            actant: wantedLinkedActant.id,
            certainty: "",
            elvl: "",
            id: wantedLinkedActant.id,
            position: "",
          },
        ],
        action: actionData.id,
        certainty: "",
        elvl: "",
        modality: "",
        note: "",
        props: [],
        references: [],
        tags: [],
        territory: {
          id: "",
          order: 0,
        },
        text: "",
      },
      id: `teststatement${rand}`,
      label: "",
    };

    beforeAll(async () => {
      db = new Db();
      await db.initDb();

      await createAction(db, actionData);

      const actantP = getActantType(actantData as any);
      if (actantP) {
        await actantP.save(db.connection);
      }

      const linkedActant = getActantType(wantedLinkedActant as any);
      if (linkedActant) {
        await linkedActant.save(db.connection);
      }

      const statement = getActantType(statementData as any);
      if (statement) {
        await statement.save(db.connection);
      }
    });

    afterAll(async () => {
      await deleteActants(db);
      await db.close();
    });

    describe("search only class + by existing label", () => {
      it("should return a 200 code with successful response", async (done) => {
        await request(app)
          .post(`${apiPath}/actants/search`)
          .send({ class: actantData.class, label: actantData.label })
          .set("authorization", "Bearer " + supertestConfig.token)
          .expect("Content-Type", /json/)
          .expect(200)
          .expect((res: Response) => {
            expect(res.body[0].actantId).toEqual(actantData.id);
          });

        done();
      });
    });

    describe("search only by non-existing label", () => {
      it("should return a 400 code with successful response for invalid label", async (done) => {
        await request(app)
          .post(`${apiPath}/actants/search`)
          .send({ label: actantData.label + "xxx" })
          .set("authorization", "Bearer " + supertestConfig.token)
          .expect("Content-Type", /json/)
          .expect(200)
          .expect((res: Response) => {
            expect(res.body).toHaveLength(0);
          });

        done();
      });
    });

    describe("search only by class + existing actant in statement", () => {
      it("should return a 200 code with successful response", async (done) => {
        await request(app)
          .post(`${apiPath}/actants/search`)
          .send({
            class: wantedLinkedActant.class,
            actantId: actantData.id,
          })
          .set("authorization", "Bearer " + supertestConfig.token)
          .expect("Content-Type", /json/)
          .expect(200)
          .expect((res: Response) => {
            expect(res.body).toHaveLength(1);
            expect(res.body[0].actantId).toEqual(wantedLinkedActant.id);
          });

        done();
      });
    });

    describe("search only by non-existing actant in statement", () => {
      it("should return a 200 code with successful response", async (done) => {
        await request(app)
          .post(`${apiPath}/actants/search`)
          .send({
            actantId: actantData.id + "xxx", // does not exist
          })
          .set("authorization", "Bearer " + supertestConfig.token)
          .expect("Content-Type", /json/)
          .expect(200)
          .expect((res: Response) => {
            expect(res.body).toHaveLength(0);
          });

        done();
      });
    });

    describe("search only by class + existing action in statement", () => {
      it("should return a 200 code with successful response", async (done) => {
        await request(app)
          .post(`${apiPath}/actants/search`)
          .send({
            class: wantedLinkedActant.class,
            actionId: actionData.id,
          })
          .set("authorization", "Bearer " + supertestConfig.token)
          .expect("Content-Type", /json/)
          .expect(200)
          .expect((res: Response) => {
            expect(res.body).toHaveLength(1);
            expect(res.body[0].actantId).toEqual(wantedLinkedActant.id);
          });

        done();
      });
    });

    describe("search only by non-existing action in statement", () => {
      it("should return a 200 code with successful response", async (done) => {
        await request(app)
          .post(`${apiPath}/actants/search`)
          .send({
            actionId: actionData.id + "xxx", // does not exist
          })
          .set("authorization", "Bearer " + supertestConfig.token)
          .expect("Content-Type", /json/)
          .expect(200)
          .expect((res: Response) => {
            expect(res.body).toHaveLength(0);
          });

        done();
      });
    });

    describe("search by all params", () => {
      it("should return a 200 code with successful response", async (done) => {
        await request(app)
          .post(`${apiPath}/actants/search`)
          .send({
            class: wantedLinkedActant.class,
            actantId: actantData.id,
            actionId: actionData.id,
            label: wantedLinkedActant.label,
          })
          .set("authorization", "Bearer " + supertestConfig.token)
          .expect("Content-Type", /json/)
          .expect(200)
          .expect((res: Response) => {
            expect(res.body[0].actantId).toEqual(wantedLinkedActant.id);
          });

        done();
      });
    });

    describe("search by all params + misused label", () => {
      it("should return a 200 code with successful response", async (done) => {
        await request(app)
          .post(`${apiPath}/actants/search`)
          .send({
            class: wantedLinkedActant.class,
            actantId: actantData.id,
            actionId: actionData.id,
            label: wantedLinkedActant.label + "xxx", // does not exist
          })
          .set("authorization", "Bearer " + supertestConfig.token)
          .expect("Content-Type", /json/)
          .expect(200)
          .expect((res: Response) => {
            expect(res.body).toHaveLength(0);
          });

        done();
      });
    });
  });
});