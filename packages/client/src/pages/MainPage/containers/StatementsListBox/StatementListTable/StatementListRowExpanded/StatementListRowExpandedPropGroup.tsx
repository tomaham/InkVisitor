import { IEntity, IProp } from "@shared/types";
import React from "react";
import { EntityTag } from "../../../EntityTag/EntityTag";
import {
  StyledPropGroup,
  StyledPropRow,
} from "./StatementListRowExpandedStyles";

interface StatementListRowExpandedPropGroup {
  level: 1 | 2 | 3;
  props: IProp[];
  entities: { [key: string]: IEntity };
  renderChildrenPropRow?: (props: IProp[]) => React.ReactElement;
}
export const StatementListRowExpandedPropGroup: React.FC<
  StatementListRowExpandedPropGroup
> = ({ level, props, entities, renderChildrenPropRow }) => {
  return (
    <StyledPropGroup>
      {props.map((prop, key) => {
        const propTypeEntity: IEntity = entities[prop.type.id];
        const propValueEntity: IEntity = entities[prop.value.id];
        return (
          <React.Fragment key={key}>
            <StyledPropRow key={`${key}-`} level={level}>
              {propTypeEntity ? (
                <>
                  <EntityTag
                    actant={propTypeEntity}
                    tooltipPosition="bottom center"
                  />
                  <span>&nbsp;</span>
                </>
              ) : (
                <span>[type]&nbsp;</span>
              )}
              {propValueEntity ? (
                <EntityTag
                  actant={propValueEntity}
                  tooltipPosition="bottom center"
                />
              ) : (
                "[value]"
              )}
            </StyledPropRow>
            <div key={`children-${key}`}>
              {renderChildrenPropRow && renderChildrenPropRow(prop.children)}
            </div>
          </React.Fragment>
        );
      })}
    </StyledPropGroup>
  );
};