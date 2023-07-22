import yaml
from github import Github, InputGitTreeElement

class GitConfigStorage:
    def __init__(self, config_class, repo_name, github_token):
        self.config_class = config_class
        self.repo_name = repo_name
        self.github = Github(github_token)
        self.repo = self.github.get_repo(repo_name)

    def _get_repo_contents(self, branch):
        contents = self.repo.get_contents("", ref=branch)
        config_files = [content for content in contents if content.type == "file" and content.name.endswith(".yaml")]
        return config_files

    def _merge_yaml_configs(self, config_files):
        merged_config = {}
        for file in config_files:
            config_content = file.decoded_content.decode()
            config_data = yaml.safe_load(config_content)
            merged_config.update(config_data)
        return merged_config

    def get(self, branch="master", tag=None):
        config_files = self._get_repo_contents(branch)

        if tag:
            tag_ref = self.repo.get_git_ref(f"tags/{tag}")
            tag_sha = tag_ref.object.sha
            config_files = self._get_repo_contents(tag_sha)

        merged_config = self._merge_yaml_configs(config_files)
        return self.config_class(merged_config)

# Example Usage
class MyConfig:
    def __init__(self, data):
        self.data = data

    def get(self, key):
        return self.data.get(key)

# Replace with your GitHub repository and token
repo_name = "username/repo_name"
github_token = "YOUR_GITHUB_TOKEN"

config_storage = GitConfigStorage(MyConfig, repo_name, github_token)
config_data = config_storage.get(branch="main")
print(config_data.get("example_key"))