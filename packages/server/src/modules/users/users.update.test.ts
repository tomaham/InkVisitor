import "@modules/common.test";
import { BadParams } from "@common/errors";
import request from "supertest";
import { apiPath } from "../../common/constants";
import app from "../../Server";
import { successfulGenericResponse } from "../common.test";

describe("Users update", function () {
  describe("empty data", () => {
    it("should return a 400 code with BadParams error", (done) => {
      return request(app)
        .put(`${apiPath}/users/update/1`)
        .expect("Content-Type", /json/)
        .expect({ error: new BadParams("whatever").toString() })
        .expect(400, done);
    });
  });
  describe("faulty data ", () => {
    it("should return a 400 code with BadParams error", (done) => {
      return request(app)
        .put(`${apiPath}/users/update/1`)
        .send({ test: "" })
        .expect("Content-Type", /json/)
        .expect({ error: new BadParams("whatever").toString() })
        .expect(400, done);
    });
  });
  describe("ok data", () => {
    it("should return a 200 code with successful response", (done) => {
      return request(app)
        .put(`${apiPath}/users/update/1`)
        .send({ email: `admin${Math.random()}@admin.com` })
        .expect("Content-Type", /json/)
        .expect(successfulGenericResponse)
        .expect(200, done);
    });
  });
});
