import Col from "react-bootstrap/Col";

const UploadedImage = (props) => {
  return (
    <Col className="d-flex align-items-center justify-content-center col-3">
      <img
        id="uploaded-image"
        src={props.src}
        alt={"input"}
        hidden={!props.showImage}
        onLoad={props.predict}
        className="shadow"
      />
    </Col>
  );
};

export default UploadedImage;
