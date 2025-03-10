FROM public.ecr.aws/lambda/python:3.8

# Copy function code
COPY app.py ${LAMBDA_TASK_ROOT}
COPY requirements.txt ./
COPY templates ${LAMBDA_TASK_ROOT}/templates
COPY static ${LAMBDA_TASK_ROOT}/static
COPY cdp_api_key.json ${LAMBDA_TASK_ROOT}

# Install dependencies
RUN pip install -r requirements.txt

# Set the CMD to your handler
CMD ["app.lambda_handler"]
