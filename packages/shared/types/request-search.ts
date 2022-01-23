/**
 * type of the /user endpoint response
 */

import {
  ActantStatus,
  ActantType,
  EntityLogicalType,
  isValidActantType,
  Language,
} from "../enums";
import { BadParams } from "./errors";

export interface IResponseSearch {
  class: ActantType | false;
  label: string | false;
  actantId: string | false;
}

export class RequestSearch implements IResponseSearch {
  class: ActantType | false;
  label: string | false;
  actantId: string | false;
  excluded?: ActantType[];

  constructor(requestData: IResponseSearch & { excluded?: ActantType[] }) {
    this.class = requestData.class || false;
    this.label = requestData.label || false;
    this.actantId = requestData.actantId || false;
    if (requestData.excluded) {
      if (requestData.excluded.constructor.name === "String") {
        requestData.excluded = [requestData.excluded as any];
      }
      this.excluded = requestData.excluded;
    }
  }

  validate(): Error | void {
    if (this.class !== false && !isValidActantType(this.class)) {
      return new BadParams("invalid 'class' value");
    }

    if (!this.label && !this.actantId) {
      return new BadParams("at least some search field has to be set");
    }

    return;
  }
}

interface IEntityHasProps {
  value?: string; // 'any' as default, otherwise this is the id of the actant that was used as the value within prop
  type?: string; // 'any' as default, id of the actat used as the type of the prop
  negative?: boolean; // false on default
  operator?: "and" | "or"; // and on default and may be implemented in 1.4.0
  bundleStart?: boolean; // false on default and may be implemented in 1.4.0
  bundleEnd?: boolean; // false on default and may be implemented in 1.4.0
}
interface IEntityUsedInTerritory {
  territoryId?: string;
  position?: ISearchPositionInStatement; // any as default, may be implemented in 1.4.0
  negative?: boolean; // false on default
  operator?: "and" | "or"; // and on default and may be implemented in 1.4.0
  bundleStart?: boolean; // false on default and may be implemented in 1.4.0
  bundleEnd?: boolean; // false on default and may be implemented in 1.4.0
}

interface IEntityUsedInStatementWith {
  entityPosition?: ISearchPositionInStatement; // position of the original entity within the statement
  withEntity?: string; // entity that is used within the same statement
  withEntityPosition?: ISearchPositionInStatement; // what is this "with" entity position? default any
  negative?: boolean; // false as default, should be within 1.3.0
  operator?: "and" | "or"; // and on default and may be implemented in 1.4.0
  bundleStart?: boolean; // false on default and may be implemented in 1.4.0
  bundleEnd?: boolean; // false on default and may be implemented in 1.4.0
}

export interface IRequestSearchEntity {
  class?: string; //izy
  label?: string; // regex, should also work from the middle...
  detail?: string; // also regex
  notes?: string; // is the text used within any note
  status?: ActantStatus; // izy
  language?: Language; //izy
  logicalType?: EntityLogicalType;
  hasProps?: IEntityHasProps[]; //this should be checked within meta props and within all statements where the entity is used as the prop origin
  usedInTerritories?: IEntityUsedInTerritory[]; // this is probably little bit complicated
  usedInStatements?: IEntityUsedInStatementWith[]; // and this is supposed to be complicated as well
}

export type ISearchPositionInStatement =
  | "any"
  | "action"
  | "actant"
  | "tag"
  | "reference"
  | "prop value"
  | "prop type";

interface IUsedEntityStatement {
  entityId?: string;
  position?: ISearchPositionInStatement;
  negative?: boolean; // positive as default, should be within 1.3.0
  operator?: "and" | "or"; // and on default and may be implemented in 1.4.0
  bundleStart?: boolean; // false on default and may be implemented in 1.4.0
  bundleEnd?: boolean; // false on default and may be implemented in 1.4.0
}

export interface IRequestSearchStatement {
  text?: string; // izy
  author?: string; // is author of the statement the user with this id ?
  editor?: string; // is user id in any audit?
  note?: string; // is the text used within any note
  territory?: string; // check the whole tree to the root
  usedEntities?: IUsedEntityStatement[]; // see below
}

export class RequestSearchEntity {
  constructor(requestData: any) {}
  validate(): Error | void {
    return;
  }
}

export class RequestSearchStatement {
  constructor(requestData: any) {}

  validate(): Error | void {
    return;
  }
}
