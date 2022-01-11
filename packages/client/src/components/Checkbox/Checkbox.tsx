import React, { useEffect, useState } from "react";
import {
  StyledCheckbox,
  StyledCheckBoxWrap,
  StyledLabel,
} from "./CheckboxStyles";

interface Checkbox {
  value?: boolean;
  onChangeFn: Function;
  label?: string;
  id?: string;
  disabled?: boolean;
}
export const Checkbox: React.FC<Checkbox> = ({
  value,
  onChangeFn,
  label,
  id = "default",
  disabled = false,
}) => {
  const [checked, setChecked] = useState(value);

  useEffect(() => {
    onChangeFn(checked);
  }, [checked]);
  return (
    <StyledCheckBoxWrap>
      <StyledCheckbox
        type="checkbox"
        id={id}
        checked={checked}
        onChange={() => {
          setChecked(!checked);
        }}
        disabled={disabled}
      />
      {label && <StyledLabel htmlFor={id}>{label}</StyledLabel>}
    </StyledCheckBoxWrap>
  );
};
