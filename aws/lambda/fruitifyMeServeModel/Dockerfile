FROM public.ecr.aws/lambda/nodejs:16

COPY function.mjs package.json model.json classNames.js *.bin ${LAMBDA_TASK_ROOT}/

RUN npm install

CMD ["function.handler"]