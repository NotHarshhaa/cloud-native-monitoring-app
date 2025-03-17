import logging
from kubernetes import client, config

# Configure logging
logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")

def load_kube_config():
    """Loads Kubernetes configuration (either local or in-cluster)."""
    try:
        config.load_kube_config()  # Use for local development
        logging.info("Loaded kubeconfig from local environment.")
    except Exception:
        config.load_incluster_config()  # Use when running inside a Kubernetes cluster
        logging.info("Loaded in-cluster Kubernetes configuration.")

def create_deployment(api_instance):
    """Creates a Kubernetes Deployment for the Flask app."""
    deployment = client.V1Deployment(
        metadata=client.V1ObjectMeta(name="my-flask-app"),
        spec=client.V1DeploymentSpec(
            replicas=1,
            selector=client.V1LabelSelector(match_labels={"app": "my-flask-app"}),
            template=client.V1PodTemplateSpec(
                metadata=client.V1ObjectMeta(labels={"app": "my-flask-app"}),
                spec=client.V1PodSpec(
                    containers=[
                        client.V1Container(
                            name="my-flask-container",
                            image="568373317874.dkr.ecr.us-east-1.amazonaws.com/my_monitoring_app_image:latest",
                            ports=[client.V1ContainerPort(container_port=5000)]
                        )
                    ]
                )
            )
        )
    )

    try:
        api_instance.create_namespaced_deployment(namespace="default", body=deployment)
        logging.info("Deployment created successfully.")
    except Exception as e:
        logging.error(f"Failed to create deployment: {e}")

def create_service(api_instance):
    """Creates a Kubernetes Service for the Flask app."""
    service = client.V1Service(
        metadata=client.V1ObjectMeta(name="my-flask-service"),
        spec=client.V1ServiceSpec(
            selector={"app": "my-flask-app"},
            ports=[client.V1ServicePort(port=5000, target_port=5000)]
        )
    )

    try:
        api_instance.create_namespaced_service(namespace="default", body=service)
        logging.info("Service created successfully.")
    except Exception as e:
        logging.error(f"Failed to create service: {e}")

def main():
    """Main function to deploy the application."""
    load_kube_config()
    api_client = client.ApiClient()
    
    # Create Deployment and Service
    create_deployment(client.AppsV1Api(api_client))
    create_service(client.CoreV1Api(api_client))

if __name__ == "__main__":
    main()
