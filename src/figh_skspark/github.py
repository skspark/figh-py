from typing import Generic, TypeVar

import yaml
from github import Github
from pydantic import BaseModel

T = TypeVar("T")


class GithubConfigStorage(Generic[T], BaseModel):
    def __init__(self, repo_name, github_token):
        self.repo_name = repo_name
        self.github = Github(github_token)
        self.repo = self.github.get_repo(repo_name)

    def _get_repo_contents(self, branch):
        contents = self.repo.get_contents("", ref=branch)
        config_files = [
            content
            for content in contents
            if content.type == "file" and content.name.endswith(".yaml")
        ]
        return config_files

    def _merge_yaml_configs(self, config_files):
        merged_config = {}
        for file in config_files:
            config_content = file.decoded_content.decode()
            config_data = yaml.safe_load(config_content)
            merged_config.update(config_data)
        return merged_config

    def get(self, version="latest") -> T:
        config_files = self._get_repo_contents(branch)
        if tag:
            tag_ref = self.repo.get_git_ref(f"tags/{tag}")
            tag_sha = tag_ref.object.sha
            config_files = self._get_repo_contents(tag_sha)

        merged_config = self._merge_yaml_configs(config_files)
        return T(**merged_config)
