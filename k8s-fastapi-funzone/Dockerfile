# Use the official Python runtime as the base image
FROM python:3.10

# Set the working directory in the container
WORKDIR /app

# Copy requirements.txt to the container
COPY requirements.txt requirements.txt

# Install app dependencies
RUN pip install -r requirements.txt

# Copy the rest of the app source code to the container
COPY . .

# Expose the port on which the app will run
EXPOSE 5000

# Define the command to run the app when the container starts
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "5000"]
