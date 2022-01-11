import styled from "styled-components";
import { space1 } from "Theme/constants";

interface StyledCheckbox {
  disabled: boolean;
}
export const StyledCheckbox = styled.input<StyledCheckbox>`
  height: ${({ theme }) => theme.space[10]};
  text-align: left;
  font-size: ${({ theme }) => theme.fontSize["xs"]};
  padding: ${space1};
  width: ${({ width }) => (width ? `${width}px` : "auto")};
  resize: none;
  :focus {
    outline: 0;
  }
`;

export const StyledCheckBoxWrap = styled.div`
  display: flex;
  align-items: center;
`;

export const StyledLabel = styled.label`
  margin-left: ${({ theme }) => theme.space[1]};
  font-size: ${({ theme }) => theme.fontSize["sm"]};
`;
