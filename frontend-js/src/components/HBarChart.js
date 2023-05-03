import HorizontalBar from "./HorizontalBar";

const HBarChart = (props) => {
  const bars = props.data.map((item) => (
    <HorizontalBar data={item} key={item[0]} />
  ));
  return <div className="rounded bg-primary shadow text-light p-1">{bars}</div>;
};
export default HBarChart;
