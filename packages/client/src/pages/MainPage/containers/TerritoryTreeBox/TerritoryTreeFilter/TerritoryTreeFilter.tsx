import { Button, Checkbox, Input } from "components";
import React, { useState } from "react";
import { ITerritoryFilter } from "types";
import { BsFilter } from "react-icons/bs";
import {
  StyledFilterList,
  StyledFilterWrap,
} from "./TerritoryTreeFilterStyles";

interface TerritoryTreeFilter {
  filterData: ITerritoryFilter;
  handleFilterChange: (key: string, value: string | boolean) => void;
}
export const TerritoryTreeFilter: React.FC<TerritoryTreeFilter> = ({
  filterData,
  handleFilterChange,
}) => {
  const [isOpen, setIsOpen] = useState(true);

  return (
    <StyledFilterWrap>
      <Button
        onClick={() => setIsOpen(!isOpen)}
        color="info"
        inverted
        fullWidth
        icon={<BsFilter />}
      />
      {isOpen && (
        <StyledFilterList>
          <Checkbox
            label="non empty"
            value={filterData.nonEmpty}
            onChangeFn={(value: boolean) =>
              handleFilterChange("nonEmpty", value)
            }
          />
          <Checkbox
            label="starred"
            value={filterData.starred}
            onChangeFn={(value: boolean) =>
              handleFilterChange("starred", value)
            }
          />
          <Checkbox
            label="editor rights"
            value={filterData.editorRights}
            onChangeFn={(value: boolean) =>
              handleFilterChange("editorRights", value)
            }
          />
          <Input
            value={filterData.filter}
            onChangeFn={(value: string) => handleFilterChange("filter", value)}
            changeOnType
          />
        </StyledFilterList>
      )}
    </StyledFilterWrap>
  );
};
