import Actant from "@models/actant/actant";
import { fillFlatObject, IModel, UnknownObject } from "@models/common";
import { EntityClass, EntityLogicalType } from "@shared/enums";
import { IPerson } from "@shared/types";

class PersonData implements IModel {
  logicalType: EntityLogicalType = EntityLogicalType.Definite;

  constructor(data: UnknownObject) {
    if (!data) {
      return;
    }

    fillFlatObject(this, data);
  }

  isValid(): boolean {
    return true;
  }
}

class Person extends Actant implements IPerson {
  static table = "actants";
  static publicFields = Actant.publicFields;

  class: EntityClass.Person = EntityClass.Person; // just default
  data: PersonData;

  constructor(data: UnknownObject) {
    super(data);

    if (!data) {
      data = {};
    }

    this.data = new PersonData(data.data as UnknownObject);
  }

  isValid(): boolean {
    if (this.class !== EntityClass.Person) {
      return false;
    }

    return this.data.isValid();
  }
}

export default Person;