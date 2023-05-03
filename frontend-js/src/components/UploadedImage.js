import { useState } from "react";

import Col from "react-bootstrap/Col";

const UploadedImage = (props) => {
  return (
    <Col className="d-flex align-items-center justify-content-center">
      <img
        id="uploaded-image"
        src={props.src}
        alt={"input"}
        hidden={!props.showImage}
        onLoad={props.predict}
      />
    </Col>
  );
};

export default UploadedImage;