import { useState, useCreateRef } from "react";

import Result from "./components/Result";
import UploadedImage from "./components/UploadedImage";
import UploadForm from "./components/UploadForm";
import AppHeader from "./components/AppHeader";

import Container from "react-bootstrap/Container";
import Row from "react-bootstrap/Row";

import * as tf from "@tensorflow/tfjs";

const model = tf.loadLayersModel("/model/model.json");

function App() {
  const [image, setImag] = useState(null);
  const [prediction, setPrediction] = useState(null);

  const resize = () => {};

  const handleUpload = (file) => {
    const reader = new FileReader();
    let img = null;
    reader.readAsDataURL(file);
    reader.onloadend = () => {
      const base64Data = reader.result;
      setImag(base64Data);
    };
  };

  const predict = (file) => {
    handleUpload(file);
    const canvas = document.createElement("canvas");
    const ctx = canvas.getContext("2d");
    ctx.drawImage(image, 0, 0, 100, 100);
    setPrediction(model.predict(canvas));
  };

  const hideImage = () => {
    setImag(null);
  };

  return (
    <Container className="text-center shadow p-3 mb-5 bg-body-tertiary rounded bg-warning">
      <AppHeader />
      <Row>
        <UploadedImage showImage={image !== null} src={image} />
        <Result />
      </Row>
      <Row>
        <UploadForm predict={predict} hideImage={hideImage} />
      </Row>
    </Container>
  );
}

export default App;
