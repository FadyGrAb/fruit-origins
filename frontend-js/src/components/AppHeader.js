import Col from "react-bootstrap/Col";
import Row from "react-bootstrap/Row";

const AppHeader = (props) => {
  return (
    <Row>
      <Col className="d-flex justify-content-end">
        <img
          src="assets/title-banana.gif"
          alt="fruity"
          className="title-gifs"
        />
      </Col>
      <Col md="auto">
        <h1 style={{ color: "white" }}>FRUITIFY ME</h1>
      </Col>
      <Col className="d-flex justify-content-star">
        <img
          src="assets/title-pumpkin.gif"
          alt="fruity"
          className="title-gifs"
        />
      </Col>
    </Row>
  );
};

export default AppHeader;
