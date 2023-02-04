from prefect.infrastructure.docker import DockerContainer

# alternative to creating a docker block in the UI
docker_block = DockerContainer(
    image_name="lisareiber/de-zoomcamp", # insert image here
    image_pull_policy="ALWAYS",
    auto_remove=True
)

docker_block.save("de-zoomcamp", overwrite=True)