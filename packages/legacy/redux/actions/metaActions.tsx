import { Dispatch } from "redux";
import { ResponseMetaI } from "@shared/types/response-meta";

import { getMeta } from "api/getMeta";
import { FETCH_META, MetaAction } from "redux/types";

export const fetchMeta = () => (
  dispatch: Dispatch<MetaAction>
): Promise<void> => {
  getMeta().then((data: ResponseMetaI) =>
    dispatch({
      type: FETCH_META,
      payload: data,
    })
  );
  return Promise.resolve();
};