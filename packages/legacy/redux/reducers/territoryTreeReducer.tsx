import { FETCH_TERRITORY, TerritoryAction } from "redux/types";
import { ResponseTerritoryI } from "@shared/types/response-territory";

const initialState: ResponseTerritoryI = {
  class: "T",
  id: "",
  data: {
    label: "",
    parent: "",
  },
  meta: {},
  children: [],
  parent: false,
  statements: [],
  actants: [],
};
const territory = (
  state: ResponseTerritoryI = initialState,
  action: TerritoryAction
): ResponseTerritoryI => {
  switch (action.type) {
    case FETCH_TERRITORY:
      return action.payload;
    default:
      return state;
  }
};

export { territory };