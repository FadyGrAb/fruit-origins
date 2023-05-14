import { GetObjectCommand, S3Client } from "@aws-sdk/client-s3";
// import { getSignedUrl } from "@aws-sdk/s3-request-presigner";
import * as tf from "@tensorflow/tfjs";
import * as tfnode from "@tensorflow/tfjs-node";
import classNames from "./classNames.mjs";

// const client = new S3Client();

export async function handler(event, context) {
  // Get classNames.json
  // const classesCommand = new GetObjectCommand({
  //   Bucket: process.env.MODEL_BUCKET,
  //   Key: "classNames.json",
  // });
  // const modelCommand = new GetObjectCommand({
  //   Bucket: process.env.MODEL_BUCKET,
  //   Key: "model.json",
  // });
  try {
    // const response = await client.send(classesCommand);
    // const str = await response.Body.transformToString();
    // const CLASS_NAMES = JSON.parse(str).classNames;
    const CLASS_NAMES = classNames;
    console.log({ classNames: CLASS_NAMES });
    // Load model
    // const MODEL_URL = await getSignedUrl(client, modelCommand, {
    //   expiresIn: 3600,
    // });
    const handler = tfnode.io.fileSystem("model.json");
    const model = await tf.loadGraphModel(handler);
    return { body: CLASS_NAMES, version: JSON.stringify(model.modelVersion) };
  } catch (err) {
    console.error(err);
  }
}
