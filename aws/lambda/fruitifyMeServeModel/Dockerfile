FROM public.ecr.aws/lambda/nodejs:16

COPY function.mjs package.json ${LAMBDA_TASK_ROOT}/

RUN npm install

CMD ["function.handler"]