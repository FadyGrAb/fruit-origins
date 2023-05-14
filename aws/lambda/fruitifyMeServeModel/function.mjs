import { GetObjectCommand, S3Client } from "@aws-sdk/client-s3";
// import { getSignedUrl } from "@aws-sdk/s3-request-presigner";
import * as tf from "@tensorflow/tfjs";

const client = new S3Client();

export async function handler(event, context) {
  // Get classNames.json
  const classesCommand = new GetObjectCommand({
    Bucket: process.env.MODEL_BUCKET,
    Key: "classNames.json",
  });
  // const modelCommand = new GetObjectCommand({
  //   Bucket: process.env.MODEL_BUCKET,
  //   Key: "model.json",
  // });
  try {
    const response = await client.send(classesCommand);
    const str = await response.Body.transformToString();
    const CLASS_NAMES = JSON.parse(str).classNames;
    // Load model
    // const MODEL_URL = await getSignedUrl(client, modelCommand, {
    //   expiresIn: 3600,
    // });
    const model = await tf.loadGraphModel("file:///model.json");
    return { body: CLASS_NAMES, version: JSON.stringify(model.modelVersion) };
  } catch (err) {
    console.error(err);
  }
}
