import { GetObjectCommand, S3Client } from "@aws-sdk/client-s3";
import * as tf from "@tensorflow/tfjs";

const client = new S3Client();

export async function handler(event, context) {
  // Get classNames.json
  const command = new GetObjectCommand({
    Bucket: process.env.MODEL_BUCKET,
    Key: "classNames.json",
  });
  try {
    const response = await client.send(command);
    const str = await response.Body.transformToString();
    const CLASS_NAMES = JSON.parse(str).classNames;
    // Load model
    const MODEL_URL = `https://${process.env.MODEL_BUCKET}.s3.amazonaws.com/model.json`;
    const model = await tf.loadGraphModel(MODEL_URL);
    return { body: CLASS_NAMES, version: JSON.stringify(model.modelVersion) };
  } catch (err) {
    console.error(err);
  }
}
