import Col from "react-bootstrap/Col";
import HBarChart from "./HBarChart";
// import BarChart from "./ResultsChart";

const Result = (props) => {
  let top10 = [];
  if (props.prediction !== null) {
    const res = props.prediction;
    res.sort((a, b) => b[1] - a[1]);
    top10 = res.slice(0, 10);
    top10 = top10.filter((item) => {
      return item[1] >= 5;
    });
  }

  return (
    <Col hidden={props.hideChart}>
      <div
        class="spinner-border text-primary m-5 p-5"
        role="status"
        hidden={props.prediction !== null}
      >
        <span class="visually-hidden">Loading...</span>
      </div>
      <div hidden={props.prediction === null}>
        <HBarChart data={top10} />
      </div>
    </Col>
  );
};

export default Result;
