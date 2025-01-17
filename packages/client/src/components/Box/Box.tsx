import React, { ReactNode, useState } from "react";
import { animated, useSpring } from "react-spring";
import { springConfig } from "Theme/constants";
import theme from "Theme/theme";
import { Colors } from "types";
import {
  StyledBox,
  StyledButtonWrap,
  StyledContent,
  StyledContentAnimationWrap,
  StyledHead,
  StyledVerticalText,
} from "./BoxStyles";

interface BoxProps {
  label?: string;
  color?: typeof Colors[number];
  height?: number;
  noPadding?: boolean;
  isExpanded?: boolean;
  button?: ReactNode;
  children?: ReactNode;
}

export const Box: React.FC<BoxProps> = ({
  label = "",
  color = "",
  height,
  noPadding = false,
  isExpanded = true,
  button,
  children,
}) => {
  const [hideContent, setHideContent] = useState<boolean>(false);
  const [showContentLabel, setShowContentLabel] = useState<boolean>(false);

  const animatedExpand = useSpring({
    opacity: isExpanded ? 1 : 0,
    contentLabelOpacity: isExpanded ? 0 : 1,
    contentBackgroundColor: isExpanded
      ? theme.color["gray"]["200"]
      : theme.color["gray"]["300"],
    onRest: () =>
      isExpanded ? setShowContentLabel(false) : setHideContent(true),
    onStart: () =>
      isExpanded ? setHideContent(false) : setShowContentLabel(true),
    config: springConfig.panelExpand,
  });

  return (
    <StyledBox height={height}>
      <StyledHead $isExpanded={isExpanded} color={color} $noPadding={noPadding}>
        {!hideContent && (
          <animated.div style={animatedExpand}>{label}</animated.div>
        )}
        <StyledButtonWrap>{button && button}</StyledButtonWrap>
      </StyledHead>
      <StyledContent
        color={color}
        $noPadding={noPadding}
        $isExpanded={isExpanded}
        style={{
          backgroundColor: animatedExpand.contentBackgroundColor as any,
        }}
      >
        <StyledContentAnimationWrap
          $hideContent={hideContent}
          style={animatedExpand}
        >
          {children}
        </StyledContentAnimationWrap>
        <StyledVerticalText
          $showContentLabel={showContentLabel}
          style={{
            opacity: animatedExpand.contentLabelOpacity as any,
          }}
        >
          {label}
        </StyledVerticalText>
      </StyledContent>
    </StyledBox>
  );
};
