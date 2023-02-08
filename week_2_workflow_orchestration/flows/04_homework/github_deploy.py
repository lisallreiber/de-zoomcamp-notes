from prefect.deployments import Deployment
from prefect_github.repository import GitHubRepository
from etl_web_to_gcs import etl_web_to_gcs

# import function from parameterized flow to login to GH
github_repo_block = GitHubRepository.load("de-zoomcamp-github")

deployment = Deployment.build_from_flow(
    flow=etl_web_to_gcs,
    name="github-flow",
    storage=github_repo_block,
    parameters={"year":2020, "month":11, "color":"green"},
    tags=["homework"],
    entrypoint="week_2_workflow_orchestration/flows/04_homework/etl_web_to_gcs.py:etl_web_to_gcs")

if __name__ == "__main__":
    deployment.apply()