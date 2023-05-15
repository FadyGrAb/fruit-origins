import * as tf from "@tensorflow/tfjs";
import * as tfnode from "@tensorflow/tfjs-node";
import classNames from "./classNames.mjs";

export async function handler(event, context) {
  try {
    console.log({ event });
    // Get classes
    const CLASS_NAMES = classNames;
    // Load model
    const handler = tfnode.io.fileSystem("model.json");
    const model = await tf.loadGraphModel(handler);
    // Predict
    const payload = JSON.parse(event.body);
    const data = Object.values(payload.data).map((item) => parseFloat(item));
    const img = tf.tensor(data, payload.shape, payload.dtype);
    const batch_img = tf.expandDims(img, 0);
    const predictions = tf.softmax(model.predict(batch_img)).dataSync();
    console.log({ predictions });
    let predArray = [];
    for (let i = 0; i < predictions.length; ++i) {
      predArray.push([CLASS_NAMES[i], predictions[i]]);
    }
    predArray = predArray.map((item) => [item[0], parseInt(item[1] * 100)]);
    console.log({ predictions });
    return { predictions: predArray };
  } catch (err) {
    console.error(err);
  }
}
