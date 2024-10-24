
# External Imports
from os import walk
from yaml import safe_load

# Internal Imports
from HiveAnalyzer.constants import CONFIG_DIR, SUPPORTED_HIVE_TYPES


class FindingsConfigHandler:
    def __init__(self):
        self.valid_config_ext = ["yml", "yaml"]
        self.config_file_count = 0
        self.configuration_files = []
        self.finding_configs = {}

        for supported_hive_type in SUPPORTED_HIVE_TYPES:
            self.finding_configs[supported_hive_type] = []

        self.get_configurations()
        self.read_configurations()

    def get_configurations(self):
        for dir_path, dir_names, file_names in walk(CONFIG_DIR):
            for file_name in file_names:
                relative_path = fr"{dir_path}\{file_name}"

                # Extracts the extension of the file
                file_ext = file_name.split(".")[-1]

                # Validates the extension of the file
                if file_ext in self.valid_config_ext:
                    self.config_file_count += 1
                    self.configuration_files.append(relative_path)
        print(f"Loaded {self.config_file_count} configuration files")

    def read_configurations(self):
        for current_configuration_file in self.configuration_files:
            print(current_configuration_file)
            with open(current_configuration_file, 'r') as current_configuration_file_stream:
                current_configuration_file_data = current_configuration_file_stream.read()

                # Uses pyyaml's safe_load to parse the yaml format to dictionary
                current_configuration = safe_load(current_configuration_file_data)
                self.parse_configuration(current_configuration)

    def parse_configuration(self, configuration):
        if type(configuration["findings"]) == list:
            for finding in configuration["findings"]:
                if type(finding) == dict:

                    # Parse hive type
                    try:
                        hive_type = finding["hive_type"]
                    except KeyError:
                        try:
                            hive_type = configuration["hive_type"]
                        except KeyError:
                            raise Exception("hive_type is a mandatory attribute")

                    if hive_type not in SUPPORTED_HIVE_TYPES:
                        raise Exception(f"{hive_type} is not a supported hive type")

                    # Parse category
                    try:
                        category : str = finding["category"]
                    except KeyError:
                        try:
                            category : str = configuration["category"]
                        except KeyError:
                            raise Exception("category is a mandatory attribute")

                    # Parse description
                    try:
                        description : str = finding["description"]
                    except KeyError:
                        try:
                            description : str = configuration["description"]
                        except KeyError:
                            raise Exception("description is a mandatory attribute")

                    # Parse timestamp description
                    try:
                        timestamp_desc : str = finding["timestamp_desc"]
                    except KeyError:
                        try:
                            timestamp_desc : str = configuration["timestamp_desc"]
                        except KeyError:
                            raise Exception("timestamp_desc is a mandatory attribute")

                    # Parse registry key path
                    try:
                        registry_key_path : str = finding["registry_key_path"]
                    except KeyError:
                        try:
                            registry_key_path : str = configuration["registry_key_path"]
                        except KeyError:
                            raise Exception("registry_key_path is a mandatory attribute")

                    # Parse registry value name
                    try:
                        registry_value_name : str = finding["registry_value_name"]
                    except KeyError:
                        try:
                            registry_value_name : str = configuration["registry_value_name"]
                        except KeyError:
                            raise Exception("registry_value_name is a mandatory attribute")

                    # Parse registry value data
                    try:
                        registry_value_data : str = finding["registry_value_data"]
                    except KeyError:
                        try:
                            registry_value_data : str = configuration["registry_value_data"]
                        except KeyError:
                            registry_value_data = None

                    # Parse timestamp from key last modified
                    try:
                        timestamp_from_key_last_modified : bool = finding["timestamp_from_key_last_modified"]
                    except KeyError:
                        try:
                            timestamp_from_key_last_modified : bool = configuration["timestamp_from_key_last_modified"]
                        except KeyError:
                            timestamp_from_key_last_modified : bool = False

                    # Parse timestamp from value decimal
                    try:
                        timestamp_from_value_decimal : bool = finding["timestamp_from_value_decimal"]
                    except KeyError:
                        try:
                            timestamp_from_value_decimal : bool = configuration["timestamp_from_value_decimal"]
                        except KeyError:
                            timestamp_from_value_decimal : bool = False

                    # Parse timestamp from value hex
                    try:
                        timestamp_from_value_hex : bool = finding["timestamp_from_value_hex"]
                    except KeyError:
                        try:
                            timestamp_from_value_hex : bool = configuration["timestamp_from_value_hex"]
                        except KeyError:
                            timestamp_from_value_hex : bool = False

                    if not (timestamp_from_key_last_modified or timestamp_from_value_decimal or timestamp_from_value_hex):
                        raise Exception(
                            "It is required to specify the location from which the timestamp will be parsed")
                    elif (timestamp_from_key_last_modified + timestamp_from_value_decimal + timestamp_from_value_hex) != 1:
                        raise Exception("You can specify only one location from which the timestamp will be parsed")

                    finding_config = {
                        "category": category,
                        "description": description,
                        "timestamp_desc": timestamp_desc,
                        "registry_key_path": registry_key_path,
                        "registry_value_name": registry_value_name,
                        "registry_value_data": registry_value_data,
                        "timestamp_from_key_last_modified": timestamp_from_key_last_modified,
                        "timestamp_from_value_decimal": timestamp_from_value_decimal,
                        "timestamp_from_value_hex": timestamp_from_value_hex
                    }
                    print(finding_config)
                    self.finding_configs[hive_type].append(finding_config)
