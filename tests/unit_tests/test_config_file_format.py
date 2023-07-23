from src.figh.config_file_format import ConfigFileFormat


def test_config_file_format_matched():
    f = ConfigFileFormat.YAML
    assert f.matched("item.yaml")
    assert f.matched("foo/bar/item.yaml")
    assert f.matched("foo/bar/item.yml")
