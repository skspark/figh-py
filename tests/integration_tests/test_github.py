import os

import pytest

from src.figh_skspark.github import GithubConfigStorage

TEST_RESOURCES_PATH = "/tests/resources"


@pytest.fixture(scope="module")
def github_test_storage(setup_test_env) -> GithubConfigStorage:
    token = os.getenv("TEST_GITHUB_TOKEN")
    repo = "skspark/figh-py"
    return GithubConfigStorage(repo_name=repo, token=token)


def test_single_file(github_test_storage):
    config = github_test_storage.get(root_path=f"{TEST_RESOURCES_PATH}/single-yaml")
    print(f"single-yaml file config: {config}")
    assert len(config) >= 1
    for k, v in config.items():
        assert len(k) >= 1
        assert len(v) >= 1


def test_nested(github_test_storage):
    config = github_test_storage.get(root_path=f"{TEST_RESOURCES_PATH}/nested-yaml")
    print(f"single-yaml file config: {config}")
    assert len(config) >= 1
    for k, v in config.items():
        assert len(k) >= 1
        assert len(v) >= 1
