from typing import Any, Dict

import yaml
from github import Github
from github.Repository import Repository

from src.figh_skspark.base import VERSION_LATEST, ConfigStorage
from src.figh_skspark.config_file_format import ConfigFileFormat


class GithubConfigStorage(ConfigStorage):
    github: Github
    repo: Repository
    base_branch: str
    file_format: ConfigFileFormat

    class Config:
        arbitrary_types_allowed = True

    def __init__(
        self,
        repo_name: str,
        token: str,
        base_branch: str = "main",
        base_path: str = "/",
        file_format: ConfigFileFormat = ConfigFileFormat.YAML,
    ):
        self.repo_name = repo_name
        self.github = Github(token)
        self.repo = self.github.get_repo(repo_name)
        self.base_branch = base_branch
        self.base_path = base_path
        self.file_format = file_format

    def _get_repo_contents(self, branch):
        contents = self.repo.get_contents(self.base_path, ref=branch)
        config_files = [
            content
            for content in contents
            if content.type == "file" and self.file_format.matched(content.name)
        ]
        return config_files

    # TODO: add filename prefix
    def _merge_configs(self, config_files) -> Dict[str, Any]:
        if self.file_format == ConfigFileFormat.YAML:
            merged_config = {}
            for file in config_files:
                config_content = file.decoded_content.decode()
                config_data = yaml.safe_load(config_content)
                merged_config.update(config_data)
            return merged_config
        else:
            raise ValueError(f"unsupported config file format: {self.file_format}")

    def get(self, version: str = VERSION_LATEST) -> Dict[str, Any]:
        if version is VERSION_LATEST:
            config_files = self._get_repo_contents(self.base_branch)
        else:
            tag_ref = self.repo.get_git_ref(f"tags/{version}")
            tag_sha = tag_ref.object.sha
            config_files = self._get_repo_contents(tag_sha)

        return self._merge_configs(config_files)
