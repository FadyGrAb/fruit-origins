import { useState } from "react";

import Form from "react-bootstrap/Form";
import Button from "react-bootstrap/Button";
import Col from "react-bootstrap/Col";

const UploadFrom = (props) => {
  const [file, setFile] = useState(null);

  const handleFileChange = (e) => {
    e.preventDefault();
    setFile(e.target.files[0]);
  };

  const handleSubmit = (e) => {
    e.preventDefault();
    props.handleUpload(file);
  };
  return (
    <Col>
      <Form className="bg-primary rounded mt-1 shadow" onSubmit={handleSubmit}>
        <label htmlFor="upload-button" style={{ color: "white" }}>
          Ready to be fruitified 🍉🍎🍇🍌🍏🍐? Upload your photo 😉
        </label>
        <input
          type="file"
          className="btn btn-info m-3 p-1"
          accept=".jpg, .jpeg, .png"
          onChange={handleFileChange}
          onClick={props.hideImage}
        ></input>
        <Button
          id="upload-button"
          //   as="input"
          variant="danger"
          className="m-2 p-3"
          type="submit"
        >
          Fruitfy
        </Button>
      </Form>
    </Col>
  );
};

export default UploadFrom;
