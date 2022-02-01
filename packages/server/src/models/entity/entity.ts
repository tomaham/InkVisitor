import {
  IDbModel,
  UnknownObject,
  fillFlatObject,
  fillArray,
} from "@models/common";
import { r as rethink, Connection, WriteResult, RDatum } from "rethinkdb-ts";
import { IStatement, IEntity, IResponseEntity, IProp } from "@shared/types";
import { EntityClass, Language, UserRole, UserRoleMode } from "@shared/enums";
import { InternalServerError } from "@shared/types/errors";
import User from "@models/user/user";
import emitter from "@models/events/emitter";
import { EventTypes } from "@models/events/types";
import { findEntitiesByIds } from "@service/shorthands";
import Base from "../base";

export default class Entity extends Base implements IEntity, IDbModel {
  static table = "actants";
  static publicFields: string[] = [
    "id",
    "class",
    "data",
    "label",
    "detail",
    "status",
    "language",
    "notes",
    "props",
  ];

  id: string = "";
  class: EntityClass = EntityClass.Person;
  data: any = {};
  label: string = "";
  detail: string = "";
  language: Language = Language.Latin;
  notes: string[] = [];
  props: IProp[] = [];

  usedIn: IStatement[] = [];
  right: UserRoleMode = UserRoleMode.Read;

  constructor(data: UnknownObject) {
    super();

    if (!data) {
      return;
    }

    fillFlatObject(this, { ...data, data: undefined });
    fillArray(this.notes, String, data.notes);
    fillArray(this.props, Object, data.props);
  }

  async save(db: Connection | undefined): Promise<WriteResult> {
    const result = await rethink
      .table(Entity.table)
      .insert({ ...this, id: this.id || undefined })
      .run(db);

    if (result.generated_keys) {
      this.id = result.generated_keys[0];
    }

    return result;
  }

  update(
    db: Connection | undefined,
    updateData: Record<string, unknown>
  ): Promise<WriteResult> {
    return rethink.table(Entity.table).get(this.id).update(updateData).run(db);
  }

  async delete(db: Connection | undefined): Promise<WriteResult> {
    if (!this.id) {
      throw new InternalServerError(
        "delete called on entity with undefined id"
      );
    }

    if (db) {
      await emitter.emit(EventTypes.BEFORE_ENTITY_DELETE, db, this.id);
    }

    const result = await rethink
      .table(Entity.table)
      .get(this.id)
      .delete()
      .run(db);

    if (result.deleted && db) {
      await emitter.emit(EventTypes.AFTER_ENTITY_DELETE, db, this.id);
    }

    return result;
  }

  isValid(): boolean {
    return true;
  }

  canBeViewedByUser(user: User): boolean {
    return true;
  }

  canBeCreatedByUser(user: User): boolean {
    return true;
  }

  canBeEditedByUser(user: User): boolean {
    return true;
  }

  canBeDeletedByUser(user: User): boolean {
    return true;
  }

  /**
   * getUserRoleMode returns derived user role mode for this instance.
   * By default this method counts with default right to view - helps with
   * performance.
   * @param user
   * @returns
   */
  getUserRoleMode(user: User): UserRoleMode {
    if (user.role === UserRole.Admin) {
      return UserRoleMode.Admin;
    }

    if (this.canBeEditedByUser(user)) {
      return UserRoleMode.Write;
    }

    return UserRoleMode.Read;
  }

  getDependentStatements(db: Connection | undefined): Promise<IStatement[]> {
    return rethink
      .table(Entity.table)
      .filter({ class: EntityClass.Statement })
      .filter((row: any) => {
        return rethink.or(
          row("data")("actants").contains((actantElement: any) =>
            actantElement("actant").eq(this.id)
          ),
          row("data")("props").contains((propElement: any) =>
            propElement("origin").eq(this.id)
          )
        );
      })
      .run(db);
  }

  static determineOrder(want: number, sibl: Record<number, unknown>): number {
    const sortedOrders: number[] = Object.keys(sibl)
      .map((k) => parseFloat(k))
      .sort((a, b) => a - b);
    let out = -1;

    if (want === undefined) {
      out = sortedOrders.length ? sortedOrders[sortedOrders.length - 1] + 1 : 0;
    } else if (sibl[want]) {
      // if there is a conflict - order number already exist
      for (let i = 0; i < sortedOrders.length; i++) {
        if (sortedOrders[i] === want) {
          // conflict occured on the biggest number - use closest bigger free
          // integer
          if (sortedOrders.length === i + 1) {
            const ceiled = Math.ceil(sortedOrders[i]);
            out = ceiled === sortedOrders[i] ? ceiled + 1 : ceiled;
            break;
          }

          // new number would be somewhere behind the wanted one(i) and before
          // the next one(i+1)
          out = sortedOrders[i] + (sortedOrders[i + 1] - sortedOrders[i]) / 2;
          if (!sibl[Math.round(out)]) {
            out = Math.round(out);
          }

          break;
        }
      }
    } else {
      // all good
      out = want;
      // less than zero -> zero optional fix
      if (out < 0 && (sortedOrders.length === 0 || sortedOrders[0] > 0)) {
        out = 0;
      }
    }

    return out;
  }

  /**
   * Returns entity ids that are present in data fields
   * @returns list of ids
   */
  getEntitiesIds(): string[] {
    const entityIds: Record<string, null> = {};

    this.props.forEach((p) => {
      entityIds[p.type.id] = null;
      entityIds[p.value.id] = null;

      p.children.forEach((p2) => {
        entityIds[p2.type.id] = null;
        entityIds[p2.value.id] = null;
      });
    });

    return Object.keys(entityIds);
  }

  async getEntities(db: Connection): Promise<IEntity[]> {
    const entities = findEntitiesByIds<IEntity>(db, this.getEntitiesIds());
    return entities;
  }

  /*
   * finds statements which are linked to current entity
   * @param db db connection
   * @param territoryId id of the entity
   * @returns list of statements data
   */
  async findDependentStatements(
    db: Connection | undefined
  ): Promise<IStatement[]> {
    const statements = await rethink
      .table(Entity.table)
      .filter({
        class: EntityClass.Statement,
      })
      .filter((row: RDatum) => {
        return rethink.or(
          row("data")("territory")("id").eq(this.id),
          row("data")("actions").contains((entry: RDatum) =>
            entry("action").eq(this.id)
          ),
          row("data")("actants").contains((entry: RDatum) =>
            entry("actant").eq(this.id)
          ),
          row("data")("tags").contains(this.id),
          row("data")("props").contains((entry: RDatum) =>
            entry("value")("id").eq(this.id)
          ),
          row("data")("props").contains((entry: RDatum) =>
            entry("type")("id").eq(this.id)
          ),
          row("data")("props").contains((entry: RDatum) =>
            entry("origin").eq(this.id)
          ),
          row("data")("references").contains((entry: RDatum) =>
            entry("resource").eq(this.id)
          )
        );
      })
      .run(db);

    return statements.sort((a, b) => {
      return a.data.territory.order - b.data.territory.order;
    });
  }

  async prepareResponseFields(user: User, db: Connection | undefined) {
    this.usedIn = await this.findDependentStatements(db);
    this.right = this.getUserRoleMode(user);
  }

  static getPublicFields(a: Entity): string[] {
    return Object.keys(a).filter((k) => k.indexOf("_") !== 0);
  }

  toJSON(): IResponseEntity {
    const entity = this;
    const strippedObject: IEntity = Entity.getPublicFields(this).reduce(
      (acc, curr) => {
        acc[curr] = (entity as Record<string, unknown>)[curr];
        return acc;
      },
      {} as any
    );

    return strippedObject;
  }
}
