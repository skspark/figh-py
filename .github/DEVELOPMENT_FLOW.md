# Prerequisites
```shell
make local_setup
```

Note that we use pdm for package manager.
```shell
pdm add {package-name}
pdm remove {package-name}
pdm add {package-name} --dev # dev dependency
```

# Build
```shell
pdm build
#pip install dist/....whl
```

# Publish
```shell
#python -m pip install --upgrade twine
python -m twine upload --repository testpypi dist/*
python -m twine upload --repository pypi dist/*
```

# Run tests
## Unit tests
```shell
make unit_tests
```

## Integration Tests
for integration tests, you need to setup env variables to fully test all functions.

```shell
cp .env.sample .env
# and fill in all env variables in .env
make integration_tests
```
