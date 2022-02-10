import { UserRoleMode } from "@shared/enums";
import api from "api";
import { Button, Loader } from "components";
import { useSearchParams } from "hooks";
import React, { useEffect, useState } from "react";
import { FaPlus } from "react-icons/fa";
import { useMutation, useQuery, useQueryClient } from "react-query";
import { setSelectedTerritoryPath } from "redux/features/territoryTree/selectedTerritoryPathSlice";
import { useAppDispatch, useAppSelector } from "redux/hooks";
import { rootTerritoryId } from "Theme/constants";
import { searchTree } from "utils";
import { ContextMenuNewTerritoryModal } from "./ContextMenuNewTerritoryModal/ContextMenuNewTerritoryModal";
import { StyledTreeWrapper } from "./TerritoryTreeBoxStyles";
import { TerritoryTreeNode } from "./TerritoryTreeNode/TerritoryTreeNode";
import { ITerritoryFilter } from "types";
import { TerritoryTreeFilter } from "./TerritoryTreeFilter/TerritoryTreeFilter";
import { IResponseTree } from "@shared/types";

const initValues: ITerritoryFilter = {
  nonEmpty: false,
  starred: false,
  editorRights: false,
  filter: "",
};

export const TerritoryTreeBox: React.FC = () => {
  const queryClient = useQueryClient();

  const { status, data, error, isFetching } = useQuery(
    ["tree"],
    async () => {
      const res = await api.treeGet();
      return res.data;
    },
    { enabled: api.isLoggedIn() }
  );
  const userId = localStorage.getItem("userid");

  const {
    status: userStatus,
    data: userData,
    error: userError,
    isFetching: userIsFetching,
  } = useQuery(
    ["user"],
    async () => {
      if (userId) {
        const res = await api.usersGet(userId);
        return res.data;
      }
    },
    { enabled: api.isLoggedIn() }
  );

  const [storedTerritoryIds, setStoredTerritoryIds] = useState<string[]>([]);
  useEffect(() => {
    if (userData?.storedTerritories) {
      setStoredTerritoryIds(
        userData.storedTerritories.map((territory) => territory.territory.id)
      );
    }
  }, [userData?.storedTerritories]);

  const updateUserMutation = useMutation(
    async (changes: object) => {
      if (userId) {
        await api.usersUpdate(userId, changes);
      }
    },
    {
      onSuccess: () => {
        queryClient.invalidateQueries(["tree"]);
        queryClient.invalidateQueries(["user"]);
      },
    }
  );

  const userRole = localStorage.getItem("userrole");
  const { territoryId } = useSearchParams();
  const [showCreate, setShowCreate] = useState(false);

  const dispatch = useAppDispatch();
  const selectedTerritoryPath = useAppSelector(
    (state) => state.territoryTree.selectedTerritoryPath
  );

  useEffect(() => {
    if (data) {
      const foundTerritory = searchTree(data, territoryId);
      if (foundTerritory) {
        dispatch(setSelectedTerritoryPath(foundTerritory.path));
      }
    }
  }, [data, territoryId]);

  const [filterData, setFilterData] = useState<ITerritoryFilter>(initValues);

  const handleFilterChange = (key: string, value: string | boolean) => {
    setFilterData({
      ...filterData,
      [key]: value,
    });
  };

  const findTextOld = (
    element: IResponseTree,
    matchingTitle: string
  ): IResponseTree | null => {
    var result = null;
    if (element.territory.label.includes(matchingTitle)) {
      return element;
    } else if (element.children != null) {
      var i;
      // var result = null;
      for (i = 0; result === null && i < element.children.length; i++) {
        result = findTextOld(element.children[i], matchingTitle);
        if (result) {
          return result;
        }
      }
      return result;
    }
    return null;
  };

  const findNonEmpty = (
    element: IResponseTree
  ): IResponseTree | null | undefined => {
    if (element.children.length > 0) {
      // ma deti
      console.log("ma deti", element.territory.label);
      for (var i = 0; i < element.children.length; i++) {
        var result;
        console.log("child ter label", element.children[i].territory.label);
        result = findNonEmpty(element.children[i]);
        // prosel jsem dite
        if (!result) {
          console.log("mazu", element.children[i].territory.label);
          element.children.splice(i, 1);
          i--;
        }
      }
    } else {
      // RESULT (kdyz nema deti, tak vytvarim result pro parent vrstvu)
      console.log("nema deti", element.territory.label);
      // kdyz nema deti
      if (element.empty === true) {
        // prazdny
        console.log("EMPTY");
        return null;
      } else {
        return element;
      }
    }
    if (element && element.territory.id === "T0") {
      // TODO: return filtered tree object
      console.log("----- LOGUJU element", element);
    }
  };
  // if (element.territory.label.includes(matchingTitle)) {

  useEffect(() => {
    if (data) {
      const foundTerritory = findNonEmpty(JSON.parse(JSON.stringify(data)));
      if (foundTerritory) {
      } else {
      }
    }
  }, [data]);

  // useEffect(() => {
  //   if (data) {
  //     const newData: IResponseTree = JSON.parse(JSON.stringify(data));
  //     newData.children.splice(0, 2);
  //     console.log(newData);
  //   }
  // }, [data]);

  return (
    <>
      {userRole === UserRoleMode.Admin && (
        <Button
          label="new territory"
          icon={<FaPlus />}
          onClick={() => setShowCreate(true)}
        />
      )}
      <TerritoryTreeFilter
        filterData={filterData}
        handleFilterChange={handleFilterChange}
      />

      <StyledTreeWrapper id="Territories-box-content">
        {data && (
          <TerritoryTreeNode
            right={data.right}
            territory={data.territory}
            children={data.children}
            lvl={data.lvl}
            statementsCount={data.statementsCount}
            initExpandedNodes={selectedTerritoryPath}
            empty={data.empty}
            storedTerritories={storedTerritoryIds ? storedTerritoryIds : []}
            updateUserMutation={updateUserMutation}
          />
        )}
      </StyledTreeWrapper>

      {showCreate && (
        <ContextMenuNewTerritoryModal
          onClose={() => setShowCreate(false)}
          territoryActantId={rootTerritoryId}
        />
      )}
      <Loader
        show={isFetching || userIsFetching || updateUserMutation.isLoading}
      />
    </>
  );
};
