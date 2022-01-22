import "ts-jest";
import { Db } from "@service/RethinkDB";
import { clearAudits } from "@modules/common.test";
import { IAudit } from "@shared/types";
import Audit from "./audit";
import { ResponseAudit } from "./response";

describe("test Audit.save", function () {
  const rand = Math.random().toString();

  describe("save one audit", () => {
    it("should correctly save audit instance", async () => {
      const db = new Db();
      await db.initDb();

      const audit = new Audit({
        actantId: `audit-${rand}`,
        changes: [],
        date: new Date(),
        id: "",
        user: "1",
      } as IAudit);

      await audit.save(db.connection);

      expect(audit.id).not.toBe("");

      await clearAudits(db);
    });
  });
});

describe("test Audit.getFirstForActant", function () {
  const db = new Db();
  const rand = Math.random().toString();
  const actantId = `actant-${rand}`;

  const a1Date = new Date();
  const a2Date = new Date();
  a2Date.setSeconds(a2Date.getSeconds() + 10);

  const auditData: IAudit[] = [
    {
      actantId: actantId,
      changes: {},
      id: "",
      date: a1Date,
      user: "1",
    },
    {
      actantId: actantId,
      changes: {},
      id: "",
      date: a2Date,
      user: "1",
    },
  ];

  beforeAll(async () => {
    await db.initDb();

    for (const audit of auditData) {
      const auditModel = new Audit(audit);
      await auditModel.save(db.connection);
    }
  });

  afterAll(async () => await clearAudits(db));

  it("should return exactly the first audit entry", async () => {
    const response = new ResponseAudit(actantId);
    await response.getFirstForActant(db.connection);
    expect(response.first).not.toBe(null);
    if (response.first) {
      expect(response.first.id).not.toBe("");
    }
  });
});

describe("test Audit.getLastNForActant", function () {
  const db = new Db();
  const rand = Math.random().toString();
  const actantId = `actant-${rand}`;

  const a1Date = new Date();
  const a2Date = new Date();
  a2Date.setSeconds(a2Date.getSeconds() + 10);

  const auditData: IAudit[] = [
    {
      actantId: actantId,
      changes: { a1Date },
      id: "",
      date: a1Date,
      user: "1",
    },
    {
      actantId: actantId,
      changes: { a2Date },
      id: "",
      date: a2Date,
      user: "1",
    },
  ];

  beforeAll(async () => {
    await db.initDb();

    for (const audit of auditData) {
      const auditModel = new Audit(audit);
      await auditModel.save(db.connection);
    }
  });

  afterAll(async () => await clearAudits(db));

  it("should return both entries", async () => {
    const response = new ResponseAudit(actantId);
    await response.getLastNForActant(db.connection, 2);
    expect(response.last).toHaveLength(2);
    expect(response.last[0].date).toEqual(auditData[1].date);
    expect(response.last[1].date).toEqual(auditData[0].date);
  });

  it("should return one last entry", async () => {
    const response = new ResponseAudit(actantId);
    await response.getLastNForActant(db.connection, 1);
    expect(response.last).toHaveLength(1);
    expect(response.last[0].date).toEqual(auditData[1].date);
  });
});
