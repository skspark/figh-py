from typing import Any, Dict, List

import yaml
from github import Auth, Github
from github.ContentFile import ContentFile
from github.Repository import Repository

from src.figh_skspark.base import VERSION_LATEST, ConfigStorage
from src.figh_skspark.config_file_format import ConfigFileFormat
from src.figh_skspark.util import nested_set


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
        file_format: ConfigFileFormat = ConfigFileFormat.YAML,
    ):
        self.repo_name = repo_name
        self.github = Github(auth=Auth.Token(token))
        self.repo = self.github.get_repo(repo_name)
        self.base_branch = base_branch
        self.file_format = file_format

    def _get_repo_contents(self, ref, root_path: str = "/") -> List[ContentFile]:
        contents = self.repo.get_contents(root_path, ref=ref)
        config_files = [
            content
            for content in contents
            if content.type == "file" and self.file_format.matched(content.name)
        ]
        return config_files

    def _merge_configs(self, root_path: str, config_files: List[ContentFile]) -> Dict[str, Any]:
        merged_config = {}
        if self.file_format == ConfigFileFormat.YAML:
            for file in config_files:
                config_keys = self._file_config_keys(root_path, file.path)
                config_content = file.decoded_content.decode()
                config_data = yaml.safe_load(config_content)
                nested_set(merged_config, config_keys, config_data)
            return merged_config
        else:
            raise ValueError(f"unsupported config file format: {self.file_format}")

    @staticmethod
    def _file_config_keys(root_path: str, file_path: str) -> List[str]:
        root_path = root_path.strip("/")
        file_path = file_path.lstrip("/")
        if file_path.startswith(root_path):
            file_path = file_path[len(root_path) :].lstrip("/")
            items = file_path.split("/")
            items = [item for item in items if item]
            return items
        else:
            return []

    def get(self, version: str = VERSION_LATEST, root_path: str = "/") -> Dict[str, Any]:
        if version is VERSION_LATEST:
            config_files = self._get_repo_contents(ref=self.base_branch, root_path=root_path)
        else:
            tag_ref = self.repo.get_git_ref(f"tags/{version}")
            tag_sha = tag_ref.object.sha
            config_files = self._get_repo_contents(ref=tag_sha, root_path=root_path)

        return self._merge_configs(root_path=root_path, config_files=config_files)
