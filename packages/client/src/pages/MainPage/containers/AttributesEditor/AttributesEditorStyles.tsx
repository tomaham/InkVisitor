import styled from "styled-components";

export const StyledAttributeWrapper = styled.div`
  //width: 100%;
`;
export const StyledAttributeModalContent = styled.div`
  height: 100%;
`;
export const StyledAttributeModalRow = styled.div`
  display: inline-flex;
  padding-bottom: ${({ theme }) => theme.space[1]};
  width: 100%;
`;
export const StyledAttributeModalRowLabel = styled.div`
  display: inline-flex;
  margin-top: ${({ theme }) => theme.space[1]};
`;
export const StyledAttributeModalRowLabelIcon = styled.div`
  margin-right: ${({ theme }) => theme.space[2]};
  display: inline-flex;
`;

export const StyledAttributeModalRowLabelText = styled.div`
  display: inline-flex;
  width: 10em;
`;

export const StyledAttributeModalHeaderWrapper = styled.div`
  display: block;
`;

export const StyledAttributeModalHeaderIcon = styled.div`
  display: inline-block;
  margin-right: 2px;
  width: auto;
  vertical-align: text-top;
`;