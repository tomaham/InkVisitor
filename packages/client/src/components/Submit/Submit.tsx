import React from "react";

import {
  Button,
  Modal,
  ModalHeader,
  ModalContent,
  ModalFooter,
  ModalCard,
} from "components";

interface Submit {
  title?: string;
  text?: string;
  show: boolean;
  onSubmit: Function;
  onCancel: Function;
}
export const Submit: React.FC<Submit> = ({
  title,
  text,
  show,
  onSubmit,
  onCancel,
}) => {
  return (
    <>
      <Modal onClose={(): void => onCancel()} showModal={show} disableBgClick>
        <ModalCard>
          <ModalHeader onClose={(): void => onCancel()} title={title} />
          <ModalContent>
            <p>{text}</p>
          </ModalContent>
          <ModalFooter>
            <Button
              label="Submit"
              color="danger"
              onClick={(): void => onSubmit()}
              marginRight
            />
            <Button
              label="Cancel"
              color="info"
              onClick={(): void => onCancel()}
            />
          </ModalFooter>
        </ModalCard>
      </Modal>
    </>
  );
};