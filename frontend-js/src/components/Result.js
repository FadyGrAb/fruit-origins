import Col from "react-bootstrap/Col";
import Chart from "chart.js/auto";

const Result = (props) => {
  let top10 = "";
  if (props.prediction !== null) {
    const res = props.prediction;
    res.sort((a, b) => b[1] - a[1]);
    top10 = res.slice(0, 10);
    top10 = top10.filter((item) => {
      return item[1] >= 5;
    });
  }
  const ctx = document.getElementById("results");
  console.log(ctx);
  if (ctx !== null) {
    const resultsChart = new Chart(ctx, {
      type: "bar",
      data: {
        labels: ["Red", "Blue", "Yellow", "Green", "Purple", "Orange"],
        datasets: [
          {
            label: "# of Votes",
            data: [12, 19, 3, 5, 2, 3],
            borderWidth: 1,
          },
        ],
      },
      options: {
        scales: {
          y: {
            beginAtZero: true,
          },
        },
      },
    });
  }

  return (
    <Col className="d-flex align-items-center justify-content-center">
      <p>{JSON.stringify(top10)}</p>
      <dev id="results"></dev>
    </Col>
  );
};

export default Result;
