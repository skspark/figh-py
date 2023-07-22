import os

from src.figh_skspark.github import GithubConfigStorage


def test_github_config_storage_single_file(setup_test_env):
    token = os.getenv("TEST_GITHUB_TOKEN")
    repo = os.getenv("TEST_GITHUB_REPO")
    storage = GithubConfigStorage(repo_name=repo, token=token, base_path="simple")
    print(storage.get())
