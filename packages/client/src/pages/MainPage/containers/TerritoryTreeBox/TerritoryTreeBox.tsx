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

  useEffect(() => {
    console.log(filterData);
  }, [filterData]);

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
