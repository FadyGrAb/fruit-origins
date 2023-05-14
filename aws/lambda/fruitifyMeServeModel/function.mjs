import { GetObjectCommand, S3Client } from "@aws-sdk/client-s3";
const client = new S3Client();

export async function handler(event, context) {
  const command = new GetObjectCommand({
    Bucket: process.env.MODEL_BUCKET,
    Key: "classNames.json",
  });
  try {
    const response = await client.send(command);
    const str = await response.Body.transformToString();
    console.log(str);
  } catch (err) {
    console.error(err);
  }
  console.log("Hello, It worked");
  return { body: str };
}
