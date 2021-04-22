import React, { ReactNode, useRef, useState } from "react";
import {
  DragSourceMonitor,
  DropTargetMonitor,
  useDrag,
  useDrop,
  XYCoord,
} from "react-dnd";
const queryString = require("query-string");

import { DragItem, ItemTypes } from "types";
import { TagWrapper, EntityTag, Label, ButtonWrapper } from "./TagStyles";
import { Tooltip } from "components";
import { useHistory, useLocation } from "react-router-dom";

interface TagProps {
  propId: string;
  label?: string;
  category: string;
  color: string;
  mode?: "selected" | "disabled" | "invalid" | false;
  borderStyle?: "solid" | "dashed" | "dotted";
  button?: ReactNode;
  invertedLabel?: boolean;
  short?: boolean;
  index?: number;
  moveFn?: (dragIndex: number, hoverIndex: number) => void;
}

export const Tag: React.FC<TagProps> = ({
  propId,
  label = "",
  category = "T",
  color,
  mode = false,
  borderStyle = "solid",
  button,
  invertedLabel,
  short = false,
  index,
  moveFn,
}) => {
  let history = useHistory();
  let location = useLocation();
  var hashParams = queryString.parse(location.hash);

  const ref = useRef<HTMLDivElement>(null);
  const [, drop] = useDrop({
    accept: ItemTypes.TAG,
    hover(item: DragItem, monitor: DropTargetMonitor) {
      if (!ref.current) {
        return;
      }
      const dragIndex = item.index;
      const hoverIndex = index;

      // Don't replace items with themselves
      if (dragIndex === hoverIndex) {
        return;
      }
      // Determine rectangle on screen
      const hoverBoundingRect = ref.current?.getBoundingClientRect();
      // Get vertical middle
      const hoverMiddleY =
        (hoverBoundingRect.bottom - hoverBoundingRect.top) / 2;
      // Determine mouse position
      const clientOffset = monitor.getClientOffset();
      // Get pixels to the top
      const hoverClientY = (clientOffset as XYCoord).y - hoverBoundingRect.top;
      // Only perform the move when the mouse has crossed half of the items height
      // When dragging downwards, only move when the cursor is below 50%
      // When dragging upwards, only move when the cursor is above 50%
      if (!hoverIndex) {
        return;
      }
      // Dragging downwards
      if (dragIndex < hoverIndex && hoverClientY < hoverMiddleY) {
        return;
      }
      // Dragging upwards
      if (dragIndex > hoverIndex && hoverClientY > hoverMiddleY) {
        return;
      }
      // Time to actually perform the action
      moveFn && moveFn(dragIndex, hoverIndex);
      // Note: we're mutating the monitor item here!
      // Generally it's better to avoid mutations,
      // but it's good here for the sake of performance
      // to avoid expensive index searches.
      item.index = hoverIndex;
    },
  });

  const [{ isDragging }, drag] = useDrag({
    item: { type: ItemTypes.TAG, id: propId, index, category },
    collect: (monitor: DragSourceMonitor) => ({
      isDragging: monitor.isDragging(),
    }),
  });
  drag(drop(ref));

  const renderEntityTag = () => <EntityTag color={color}>{category}</EntityTag>;
  const renderButton = () => <ButtonWrapper>{button}</ButtonWrapper>;

  const onDoubleClick = (e: React.MouseEvent) => {
    e.stopPropagation();
    e.nativeEvent.stopImmediatePropagation();

    hashParams["actant"] = propId;
    history.push({
      hash: queryString.stringify(hashParams),
    });
  };

  return (
    <>
      {short ? (
        <Tooltip label={label}>
          <div>
            <TagWrapper
              ref={ref}
              borderStyle={borderStyle}
              onDoubleClick={(e: React.MouseEvent) => onDoubleClick(e)}
            >
              {renderEntityTag()}
              {button && renderButton()}
            </TagWrapper>
          </div>
        </Tooltip>
      ) : (
        <>
          <TagWrapper
            ref={ref}
            borderStyle={borderStyle}
            onDoubleClick={(e: React.MouseEvent) => onDoubleClick(e)}
          >
            {renderEntityTag()}
            {label && (
              <Label invertedLabel={invertedLabel} borderStyle={borderStyle}>
                {label}
              </Label>
            )}
            {button && renderButton()}
          </TagWrapper>
        </>
      )}
    </>
  );
};
