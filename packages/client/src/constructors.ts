import {
  ActantStatus,
  ActantType,
  CategoryActantType,
  Certainty,
  Elvl,
  Language,
  Logic,
  Mood,
  MoodVariant,
  Operator,
  Partitivity,
  Position,
  UserRole,
  Virtuality,
} from "@shared/enums";
import {
  IActant,
  IBookmarkFolder,
  IProp,
  IStatement,
  IStatementActant,
  IStatementAction,
  IStatementReference,
  ITerritory,
} from "@shared/types";
import { v4 as uuidv4 } from "uuid";

export const CBookmarkFolder = (bookmarkName: string): IBookmarkFolder => ({
  id: uuidv4(),
  name: bookmarkName,
  actantIds: [],
});

export const CProp = (): IProp => ({
  id: uuidv4(),
  elvl: Elvl.Textual,
  certainty: Certainty.Empty,
  logic: Logic.Positive,
  mood: [Mood.Indication],
  moodvariant: MoodVariant.Realis,
  operator: Operator.And,
  bundleStart: false,
  bundleEnd: false,
  children: [],

  type: {
    id: "",
    elvl: Elvl.Textual,
    logic: Logic.Positive,
    virtuality: Virtuality.Reality,
    partitivity: Partitivity.Unison,
  },
  value: {
    id: "",
    elvl: Elvl.Textual,
    logic: Logic.Positive,
    virtuality: Virtuality.Reality,
    partitivity: Partitivity.Unison,
  },
});

export const CStatement = (
  territoryId: string,
  userRole: UserRole,
  label?: string,
  detail?: string
): IStatement => ({
  id: uuidv4(),
  class: ActantType.Statement,
  label: label ? label : "",
  detail: detail ? detail : "",
  status:
    userRole === UserRole.Admin ? ActantStatus.Approved : ActantStatus.Pending,
  language: Language.Latin,
  notes: [],
  data: {
    actions: [],
    text: "",
    territory: {
      id: territoryId,
      order: -1,
    },
    actants: [],
    references: [],
    tags: [],
  },
  props: [],
});

// duplicate statement
export const DStatement = (statement: IStatement): IStatement => {
  const duplicatedStatement = { ...statement };
  duplicatedStatement.id = uuidv4();

  duplicatedStatement.data.actants.map((a) => (a.id = uuidv4()));
  duplicatedStatement.props.map((p) => (p.id = uuidv4()));
  duplicatedStatement.data.references.map((r) => (r.id = uuidv4()));
  duplicatedStatement.data.territory.order += 0.00001;

  return duplicatedStatement;
};

export const CStatementAction = (actionId: string): IStatementAction => ({
  id: uuidv4(),
  action: actionId,
  certainty: Certainty.Empty,
  elvl: Elvl.Textual,
  logic: Logic.Positive,
  mood: [Mood.Indication],
  moodvariant: MoodVariant.Realis,
  operator: Operator.And,
  bundleStart: false,
  bundleEnd: false,
  props: [],
});

export const CTerritoryActant = (
  label: string,
  parentId: string,
  parentOrder: number,
  userRole: UserRole,
  detail?: string
): ITerritory => ({
  id: uuidv4(),
  class: ActantType.Territory,
  label: label,
  detail: detail ? detail : "",
  status:
    userRole === UserRole.Admin ? ActantStatus.Approved : ActantStatus.Pending,
  language: Language.Latin,
  notes: [],
  data: {
    parent: { id: parentId, order: parentOrder },
  },
  props: [],
});

export const CActant = (
  category: CategoryActantType,
  label: string,
  userRole: UserRole,
  detail?: string
): IActant => ({
  id: uuidv4(),
  class: category,
  label: label,
  detail: detail ? detail : "",
  data: {},
  status:
    userRole === UserRole.Admin ? ActantStatus.Approved : ActantStatus.Pending,
  language: Language.Latin,
  notes: [],
  props: [],
});

export const CReference = (resourceId: string): IStatementReference => ({
  id: uuidv4(),
  resource: resourceId,
  part: "",
  type: "",
});
