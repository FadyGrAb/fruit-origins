// React imports
import { useState } from "react";

// Components imports
import Result from "./components/Result";
import UploadedImage from "./components/UploadedImage";
import UploadForm from "./components/UploadForm";
import AppHeader from "./components/AppHeader";

import Container from "react-bootstrap/Container";
import Row from "react-bootstrap/Row";
import Col from "react-bootstrap/Col";
import * as tf from "@tensorflow/tfjs";

function App() {
  const [image, setImag] = useState(null);
  const [prediction, setPrediction] = useState(null);

  const API_GATEWAY = "https://gqsh3e64y9.execute-api.us-east-1.amazonaws.com";

  const handleUpload = (file) => {
    const reader = new FileReader();
    reader.readAsDataURL(file);
    reader.onloadend = () => {
      const base64Data = reader.result;
      setImag(base64Data);
    };
  };

  const predict = async () => {
    // set "prediction" state
    const img = document.getElementById("uploaded-image");
    const img_tensor = tf.browser.fromPixels(img);
    const img_resized = tf.image.resizeBilinear(img_tensor, [100, 100]);
    const { shape, dtype } = img_resized;
    const data = img_resized.dataSync();
    const payload = {
      shape,
      dtype,
      data,
    };
    const response = await fetch(`${API_GATEWAY}/predict`, {
      method: "POST",
      body: JSON.stringify(payload),
    });
    const result = await response.json();
    const predArray = result["predictions"];
    console.log(predArray);
    setPrediction(predArray);
  };

  const hideImage = () => {
    setImag(null);
    setPrediction(null);
  };

  return (
    <Container className="text-center mt-5 shadow p-2 mb-5 bg-body-tertiary rounded bg-warning">
      <Row>
        <Col className="justify-content-center">
          <AppHeader />
        </Col>
      </Row>
      <Row>
        <UploadedImage
          predict={predict}
          showImage={image !== null}
          src={image}
        />
        <Result prediction={prediction} hideChart={image === null} />
      </Row>
      <Row>
        <UploadForm hideImage={hideImage} handleUpload={handleUpload} />
        <footer className="text-start">
          <p>
            * This app uses an actual deeplearning model to figure out your
            fruit resemblance. Choose a photo of an actual fruit and see for
            yourself. Nothing too complex as the model is very basic and simple
            and isn't that strong 😉
          </p>
        </footer>
      </Row>
    </Container>
  );
}

export default App;
