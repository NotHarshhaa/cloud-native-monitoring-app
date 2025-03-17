import boto3
import botocore

# AWS Session (Optional: Modify if using multiple profiles)
session = boto3.session.Session()
ecr_client = session.client('ecr')

# Define repository name
repository_name = "my_monitoring_app_image"

try:
    # Check if the repository already exists
    existing_repos = ecr_client.describe_repositories()
    repo_names = [repo['repositoryName'] for repo in existing_repos.get('repositories', [])]

    if repository_name in repo_names:
        print(f"✅ Repository '{repository_name}' already exists.")
    else:
        # Create a new ECR repository
        response = ecr_client.create_repository(repositoryName=repository_name)
        repository_uri = response['repository']['repositoryUri']
        print(f"🎉 Successfully created repository: {repository_name}")
        print(f"🔗 Repository URI: {repository_uri}")

except botocore.exceptions.ClientError as e:
    error_code = e.response['Error']['Code']
    if error_code == "RepositoryAlreadyExistsException":
        print(f"⚠️ Repository '{repository_name}' already exists.")
    else:
        print(f"❌ An error occurred: {e}")
