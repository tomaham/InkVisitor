import { ActionDoesNotExits, BadParams } from "@common/errors";
import * as chai from "chai";
import "mocha";
import request from "supertest";
import { supertestConfig } from "..";
import { apiPath } from "../../common/constants";
import app from "../../Server";
import { IAction } from "@shared/types";

const should = chai.should();

const testValidAction = (res: any) => {
  res.body.should.not.empty;
  res.body.should.be.a("object");
  const actionExample: IAction = {
    id: "",
    labels: [],
    note: "",
    parent: "",
    rulesActants: [],
    rulesProperties: [],
    types: [],
    valencies: [],
  };
  res.body.should.have.keys(Object.keys(actionExample));
  res.body.id.should.not.empty;
};

describe("Actions get", function () {
  describe("Empty param", () => {
    it("should return a 400 code with BadParams error", (done) => {
      return request(app)
        .get(`${apiPath}/actions/get`)
        .set("authorization", "Bearer " + supertestConfig.token)
        .expect({ error: new BadParams("whatever").toString() })
        .expect(400, done);
    });
  });
  describe("Wrong param", () => {
    it("should return a 400 code with ActantDoesNotExits error", (done) => {
      return request(app)
        .get(`${apiPath}/actions/get/invalidId12345`)
        .set("authorization", "Bearer " + supertestConfig.token)
        .expect({ error: new ActionDoesNotExits("whatever").toString() })
        .expect(400, done);
    });
  });
  describe("Correct param", () => {
    it("should return a 200 code with user response", (done) => {
      return request(app)
        .get(`${apiPath}/actions/get/A1`)
        .set("authorization", "Bearer " + supertestConfig.token)
        .expect(testValidAction)
        .expect(200, done);
    });
  });
});