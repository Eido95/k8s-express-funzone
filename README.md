# Components

- k8s cluster: minikube

# Setup

## k8s

To create and deploy a "Fun Zone" apps to Kubernetes (k8s), you'll need to follow a few steps. Here's a high-level overview of the process:

1. Complete steps in `k8s-express-funzone/README.md`

2. Set up a Kubernetes cluster:
   - Install and configure a Kubernetes Minikube cluster (or k3s, or a managed Kubernetes service such as Google Kubernetes Engine (GKE), Amazon Elastic Kubernetes Service (EKS), or Azure Kubernetes Service (AKS)).

3. Create Kubernetes deployment and service files:
   - https://kubernetes.io/docs/tasks/configure-pod-container/pull-image-private-registry/
   - Create a file named `deployment.yaml`.
   - Create a file named `service.yaml`.

4. Deploy the app to Kubernetes:
   - Apply the deployment and service files: Run `kubectl apply -f deployment.yaml` and `kubectl apply -f service.yaml`.

# Run

1. Verify the deployment:
   - Run `kubectl get deployments` to check the status of the deployment.
   - Run `kubectl get services` to get the external IP address of the service.

2. Access deployed application:
   - Run `minikube service k8s-funzone-service` 🎉
