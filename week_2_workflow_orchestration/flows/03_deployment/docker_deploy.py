from prefect.deployments import Deployment
from prefect.infrastructure.docker import DockerContainer
from parameterized_flow import etl_parent_flow

# import function from parameterized flow to deploy docker container

# load docker block 
docker_container_block = DockerContainer.load("de-zoomcamp")

# define docker deployment
docker_deploy = Deployment.build_from_flow(
    flow=etl_parent_flow,
    name="docker-flow",
    infrastructure=docker_container_block
)

if __name__ == "__main__":
    # deploy docker container
    docker_deploy.apply()