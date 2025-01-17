/**
 * type of the /user endpoint response
 */

import { IEntity, IStatement } from ".";
import { UserRoleMode } from "../enums";

export interface IResponseEntity extends IEntity {
  // usedCount?: number;
  // usedIn?: IStatement[];
  right?: UserRoleMode;
}
