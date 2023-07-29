# Components

- Container registry: Docker Hub

# Setup

## CI

1. [Introduction to GitHub Actions | Configure CI/CD](https://docs.docker.com/build/ci/github-actions/)
2. Create a `.github/workflows/k8s-fastapi-funzone.yml` file.

## App

To create and deploy a "Fun Zone" FastAPI app to Kubernetes (k8s), you'll need to follow a few steps. Here's a high-level overview of the process:

1. Set up your development environment:
   - Install FastAPI and Uvicorn on your machine.
   - Install Docker to build container images.

2. Create an FastAPI app with Uvicorn AGI:
   - Install FastAPI as a dependency: Run `pip install fastapi`.
   - Install Uvicorn as a dependency: Run `pip install uvicorn[standard]`.
   - Create an `main.py` file.

3. Dockerize the FastAPI app:
   - Create a `Dockerfile` file.

4. Build and push the Docker image:
   - `cd k8s-fastapi-funzone`
   - Build the Docker image: Run `docker build -t <Docker ID>/k8s-fastapi-funzone:latest .` in the project directory.
   - (Optional) Run the container app `docker run -dp <ip>:<port>:<port> <Docker ID>/k8s-fastapi-funzone:latest`
   - (Optional) Access running app using  `curl <ip>:<port>`
   - `docker login`
   - Push the image to Docker Hub container registry using `docker push <Docker ID>/k8s-fastapi-funzone:latest`.