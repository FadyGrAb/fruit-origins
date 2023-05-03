import Col from "react-bootstrap/Col";
import Row from "react-bootstrap/Row";

const HorizontalBar = (props) => {
  const width = `${props.data[1]}%`;
  return (
    <Row className="m-1 align-middle">
      <Col className="col-3 fs-6">{props.data[0]}</Col>
      <Col>
        <div
          className="rounded-4 rounded-start bg-warning border border-danger border-3 text-danger"
          style={{ width: width }}
        >
          {width}
        </div>
      </Col>
    </Row>
  );
};
export default HorizontalBar;
