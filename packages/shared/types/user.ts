import { UserRole, UserRoleMode } from "./../enums";

export interface IUser {
  id: string;
  email: string;
  name: string;
  password?: string;
  role: UserRole;
  options: IUserOptions;
  bookmarks: IBookmarkFolder[];
  storedTerritories: IStoredTerritory[];
  rights: IUserRight[];
  active: boolean;
}

export interface IUserRight {
  territory: string; // entity id
  mode: UserRoleMode;
}

export interface IUserOptions {
  defaultTerritory: string;
  defaultLanguage: string;
  searchLanguages: string[];
}

export interface IStoredTerritory {
  territoryId: string; // reference to entities table, for response type see IResponseStoredTerritory
  // more field could be added here
}

export interface IBookmarkFolder {
  id: string;
  name: string;
  entityIds: string[]; // list of ids are stored in the db, for response type see IResponseBookmarks
}
