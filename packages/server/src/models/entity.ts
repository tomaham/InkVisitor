import { fillFlatObject, UnknownObject, IModel } from "./common";
import { ActantType, EntityActantType } from "@shared/enums";
import { IEntity, entityLogicalTypeValues } from "@shared/types/entity";
import Actant from "./actant";

class EntityData implements IModel {
  logicalType: typeof entityLogicalTypeValues[number] = "s";

  constructor(data: UnknownObject) {
    if (!data) {
      return;
    }
  }

  isValid(): boolean {
    return true;
  }
}

class Entity extends Actant implements IEntity {
  static table = "actants";

  id = "";
  class: EntityActantType = ActantType.Concept; // just default
  label = "";
  data = new EntityData({});

  constructor(data: UnknownObject) {
    super();

    if (!data) {
      return;
    }

    fillFlatObject(this, data);
    this.data = new EntityData(data.data as UnknownObject);
  }

  isValid(): boolean {
    const alloweedClasses = [
      ActantType.Person,
      ActantType.Group,
      ActantType.Object,
      ActantType.Concept,
      ActantType.Location,
      ActantType.Value,
      ActantType.Event,
    ];
    if (alloweedClasses.indexOf(this.class) === -1) {
      return false;
    }

    return this.data.isValid();
  }
}

export default Entity;