from uuid import UUID

import pylibyaml  # noqa; needed to monkey patch c bindings for yaml
import yaml
from aiocache.serializers import BaseSerializer
from yaml.constructor import SafeConstructor
from yaml.representer import SafeRepresenter

try:
    from yaml import CSafeDumper as SafeDumper, CSafeLoader as SafeLoader
except ImportError:
    from yaml import SafeDumper, SafeLoader


class YamlSerializer(BaseSerializer):
    DEFAULT_ENCODING = None

    UUID_YAML_TAG = 'tag:yaml.org,2023:uuid'

    @staticmethod
    def represent_uuid(dumper, data):
        value = str(data)
        return dumper.represent_scalar(tag=YamlSerializer.UUID_YAML_TAG, value=value)

    @staticmethod
    def construct_uuid(constructor, node):
        return UUID(constructor.construct_scalar(node))

    SafeRepresenter.add_multi_representer(UUID, represent_uuid)
    SafeConstructor.add_constructor(UUID_YAML_TAG, construct_uuid)

    def dumps(self, value):
        return yaml.dump(value, Dumper=SafeDumper)

    def loads(self, value):
        if value is None:
            return None
        return yaml.load(value, Loader=SafeLoader)
