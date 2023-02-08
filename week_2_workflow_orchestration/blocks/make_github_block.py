from prefect.filesystems import GitHub

# create a GitHub block
github_block = GitHub(repository="https://github.com/lisallreiber/de-zoomcamp-notes")

# list files in repo
# github_block.get_directory("week_2_workflow_orchestration/flows")  # specify a subfolder of repo

# save the block
github_block.save("de-zoomcamp-github", overwrite=True)


# block = GitHub(repository="https://github.com/lisallreiber/de-zoomcamp-notes")
# block.get_directory("week_2_workflow_orchestration/flows")  # specify a subfolder of repo
# block.save("test-gh", overwrite=True)
