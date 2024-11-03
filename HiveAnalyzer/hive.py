
# External Imports
from datetime import datetime, timedelta
import logging


logger = logging.getLogger(__name__)


class Hive:
    def __init__(self, reg_hive_path, reg_hive, output, findings_config=None):
        self.reg_hive_path = reg_hive_path
        self.reg_hive = reg_hive
        self.output = output
        self.findings_config = findings_config
        
    def get_configurable(self):
        for finding_config in self.findings_config:
            if self.reg_hive.hive_type == "system" and finding_config["registry_key_path"].startswith(r"\CurrentControlSet"):
                finding_config["registry_key_path"] = finding_config["registry_key_path"].replace("CurrentControlSet", self.current_control_set)
            
            registry_path = fr"{self.prefix}{finding_config["registry_key_path"]}\{finding_config["registry_value_name"]}"
            registry_value_data, last_modified = self.get_value_data(finding_config["registry_key_path"], finding_config["registry_value_name"])
            
            if finding_config["timestamp_from_key_last_modified"]:
                timestamp = last_modified
            elif finding_config["timestamp_from_value_hex"]:
                timestamp = self.convert_hex_filetime(registry_value_data)
                registry_value_data = timestamp
                
            elif finding_config["timestamp_from_value_decimal"]:
                timestamp = self.convert_decimal_filetime(registry_value_data)
                registry_value_data = timestamp
            
            self.output.file_evidence(timestamp=timestamp, category=finding_config["category"], timestamp_description=finding_config["timestamp_desc"],
                                  finding=registry_value_data, description=finding_config["description"], registry_path=registry_path,
                                  source=self.reg_hive_path)

    def get_value_data(self, reg_key, reg_value_name):
        reg_key_obj = self.reg_hive.get_key(reg_key)

        last_modified = reg_key_obj.header.last_modified
        reg_last_modified = self.convert_decimal_filetime(last_modified)
        reg_value_data = reg_key_obj.get_value(reg_value_name)
        return reg_value_data, reg_last_modified

    def convert_hex_filetime(self, timestamp_hex_bytes):
        
        # Convert the hex value to a decimal timestamp
        shutdown_time_decimal = int.from_bytes(timestamp_hex_bytes, byteorder='little', signed=False)

        readable_timestamp = self.convert_decimal_filetime(shutdown_time_decimal)

        return readable_timestamp

    @staticmethod
    def convert_decimal_filetime(timestamp_decimal):
        
        # Convert the decimal timestamp to a datetime object
        timestamp = datetime(1601, 1, 1) + timedelta(seconds=(timestamp_decimal / 10**7))

        readable_timestamp = timestamp.strftime("%Y-%m-%d %H:%M:%S")
        
        return readable_timestamp
