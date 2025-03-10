FROM public.ecr.aws/lambda/python:3.8

# Copy function code
COPY app.py ${LAMBDA_TASK_ROOT}
COPY requirements.txt ./

# Install dependencies
RUN pip install -r requirements.txt

# Set the CMD to your handler
CMD ["app.lambda_handler"]
