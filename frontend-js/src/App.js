// React imports
import { useState, useCreateRef } from "react";

// Components imports
import Result from "./components/Result";
import UploadedImage from "./components/UploadedImage";
import UploadForm from "./components/UploadForm";
import AppHeader from "./components/AppHeader";

import Container from "react-bootstrap/Container";
import Row from "react-bootstrap/Row";
import * as tf from "@tensorflow/tfjs";
import classNames from "./assets/classNames.json";

const model = tf.loadLayersModel("/model/model.json");
const CLASS_NAMES = classNames.classNames;

function App() {
  const [image, setImag] = useState(null);
  const [prediction, setPrediction] = useState(null);

  const handleUpload = (file) => {
    const reader = new FileReader();
    reader.readAsDataURL(file);
    reader.onloadend = () => {
      const base64Data = reader.result;
      setImag(base64Data);
    };
  };

  const objectToArray = (result) => {
    //Convert Object to list to invoke ordering
    let pred = [];
    for (let i = 0; i < result.length; ++i) {
      pred.push([[CLASS_NAMES[i]], result[i]]);
    }
    return pred.map((item) => [item[0], parseInt(item[1] * 100)]);
  };

  const predict = () => {
    // set "prediction" state
    const img = document.getElementById("uploaded-image");
    const img_tensor = tf.browser.fromPixels(img);
    const img_resized = tf.image.resizeBilinear(img_tensor, [100, 100]);
    const batch_img = tf.expandDims(img_resized, 0);
    model.then((result) => {
      const predResult = tf.softmax(result.predict(batch_img)).dataSync();
      setPrediction(objectToArray(predResult));
    });
  };

  const hideImage = () => {
    setImag(null);
  };

  return (
    <Container className="text-center shadow p-3 mb-5 bg-body-tertiary rounded bg-warning">
      <AppHeader />
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
      </Row>
    </Container>
  );
}

export default App;
