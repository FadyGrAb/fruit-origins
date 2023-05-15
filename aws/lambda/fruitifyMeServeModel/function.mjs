import * as tf from "@tensorflow/tfjs";
import * as tfnode from "@tensorflow/tfjs-node";
import classNames from "./classNames.mjs";

export async function handler(event, context) {
  try {
    console.log({ event });
    // Get classes
    const CLASS_NAMES = classNames;
    console.log({ classNames: CLASS_NAMES });
    // Load model
    const handler = tfnode.io.fileSystem("model.json");
    const model = await tf.loadGraphModel(handler);
    // Predict
    const payload = JSON.parse(event.body);
    console.log({ payload });
    console.log("Type====", typeof payload.data);
    console.log({ data: payload.data });
    const img = tf.tensor(payload.data.values(), payload.shape, payload.dtype);
    console.log({ img });
    const batch_img = tf.expandDims(img, 0);
    console.log({ batch_img });
    const predictions = tf.softmax(model.predict(batch_img)).dataSync();
    console.log({ predictions });
    let predArray = [];
    for (let i = 0; i < predictions.length; ++i) {
      predArray.push([[CLASS_NAMES[i]], predictions[i]]);
    }
    predArray = predArray.map((item) => [item[0], parseInt(item[1] * 100)]);
    console.log("======predictions", { predArray });
    return { body: CLASS_NAMES, predictions: predArray };
  } catch (err) {
    console.error(err);
  }
}
