import {
  Button,
  ButtonGroup,
  Loader,
  Modal,
  ModalContent,
  ModalFooter,
  ModalHeader,
} from "components";
import React from "react";

interface Submit {
  title?: string;
  text?: string;
  show: boolean;
  onSubmit: () => void;
  onCancel: () => void;
  loading?: boolean;
}
export const Submit: React.FC<Submit> = ({
  title,
  text,
  show,
  onSubmit,
  onCancel,
  loading = false,
}) => {
  return (
    <>
      <Modal
        onEnterPress={onSubmit}
        onClose={onCancel}
        showModal={show}
        disableBgClick
      >
        <ModalHeader title={title} />
        <ModalContent>
          <p>{text}</p>
        </ModalContent>
        <ModalFooter>
          <ButtonGroup>
            <Button label="Cancel" color="info" onClick={onCancel} />
            <Button label="Submit" color="danger" onClick={onSubmit} />
          </ButtonGroup>
        </ModalFooter>
        <Loader show={loading} />
      </Modal>
    </>
  );
};
