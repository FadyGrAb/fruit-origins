import { useState } from "react";

import Col from "react-bootstrap/Col";

const UploadedImage = (props) => {
  return (
    <Col className="d-flex align-items-center justify-content-center">
      <img src={props.src} alt={"input"} hidden={!props.showImage} />
    </Col>
  );
};

export default UploadedImage;
