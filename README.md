# figh-py

## Usage
```python
from figh import GithubConfigStorage

# for github
s = GithubConfigStorage(repo_name="<github_repo>", token="<github-token>")
latest_configs = s.get()
tag_configs = s.get(version="<tag>")
```

## Development Flow
for development flow, please refer to this [guide](.github/DEVELOPMENT_FLOW.md)
