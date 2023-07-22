# Components

- Container registry: Docker Hub

# Setup

## CI

1. [Introduction to GitHub Actions | Configure CI/CD](https://docs.docker.com/build/ci/github-actions/)
2. Create a `.github/workflows/k8s-express-funzone.yml` file.

## App

To create and deploy a "Fun Zone" Express.js app to Kubernetes (k8s), you'll need to follow a few steps. Here's a high-level overview of the process:

1. Set up your development environment:
   - Install Node.js and npm (Node Package Manager) on your machine.
   - Install Docker to build container images.

2. Create an Express.js app:
   - Initialize a new Node.js project: Run `npm init` in a new directory and follow the prompts.
   - Install Express.js as a dependency: Run `npm install express`.
   - Create an `index.js` file.

3. Dockerize the Express.js app:
   - Create a `Dockerfile` file.

4. Build and push the Docker image:
   - `cd k8s-express-funzone`
   - Build the Docker image: Run `docker build -t <Docker ID>/k8s-express-funzone:latest .` in the project directory.
   - `docker login`
   - Push the image to Docker Hub container registry using `docker push <Docker ID>/k8s-express-funzone:latest`.
