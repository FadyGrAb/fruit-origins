import Col from "react-bootstrap/Col";

const Result = (props) => {
  return (
    <Col className="d-flex align-items-center justify-content-center">
      <p>{JSON.stringify(props.prediction)}</p>
    </Col>
  );
};

export default Result;
