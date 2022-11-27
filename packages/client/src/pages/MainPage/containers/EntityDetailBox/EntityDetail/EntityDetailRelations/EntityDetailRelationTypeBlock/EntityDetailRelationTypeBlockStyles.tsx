import styled from "styled-components";

export const StyledRelation = styled.div`
  display: inline-flex;
  overflow: hidden;
  flex-wrap: wrap;
`;
export const StyledEntityWrapper = styled.div`
  display: inline-flex;
  overflow: hidden;
  max-width: 100%;
  margin-right: ${({ theme }) => theme.space[1]};
  margin-bottom: ${({ theme }) => theme.space[1]};
`;
export const StyledCloudEntityWrapper = styled.div`
  display: inline-flex;
  overflow: hidden;
  max-width: 100%;
  margin: ${({ theme }) => theme.space[1]};
`;
interface StyledGrid {
  hasAttribute?: boolean;
  isMultiple: boolean;
}
export const StyledGrid = styled.div<StyledGrid>`
  display: grid;
  grid-template-columns: ${({ hasAttribute, isMultiple }) =>
    `${isMultiple ? "2rem" : ""} auto ${hasAttribute ? "14rem" : ""}`};
  max-width: 100%;
  align-items: center;
  width: fit-content;
`;
export const StyledGridColumn = styled.div`
  margin: ${({ theme }) => theme.space[1]};
  display: grid;
  align-items: center;
`;
export const StyledRelationType = styled.div`
  display: flex;
  flex-direction: column;
  align-items: center;
`;
export const StyledLabelSuggester = styled.div`
  display: flex;
  flex-direction: column;
`;
export const StyledLabel = styled.div`
  color: ${({ theme }) => theme.color["info"]};
  font-size: ${({ theme }) => theme.fontSize["xs"]};
`;
export const StyledRelationValues = styled.div`
  margin-left: ${({ theme }) => theme.space[12]};
`;
export const StyledSuggesterWrapper = styled.div`
  margin-top: ${({ theme }) => theme.space[1]};
  margin-left: ${({ theme }) => theme.space[2]};
`;
