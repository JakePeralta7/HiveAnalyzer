
# Internal Imports
from HiveAnalyzer.hive import Hive


class SystemHive(Hive):
    def __init__(self, reg_hive_path, reg_hive, output):
        super().__init__(reg_hive_path, reg_hive, output)
        self.prefix = r"HKEY_LOCAL_MACHINE\SYSTEM"
        self.current_control_set = self.get_current_control_set()
    
    def get_current_control_set(self):
        
        # We can determine what is the CurrentControlSet based on 'HKEY_LOCAL_MACHINE\SYSTEM\Select\Current'
        current_control_set_value = self.reg_hive.get_key(r"\Select").get_value("Current")
        
        match current_control_set_value:
            case 1:
                current_control_set = "ControlSet001"
            case 2:
                current_control_set = "ControlSet002"
            case _:
                raise Exception("Couldn't find the current control set")
                current_control_set = None
        return current_control_set

    def get_computer_name(self):
        reg_key = fr"\{self.current_control_set}\Control\ComputerName\ComputerName"
        reg_value_name = "ComputerName"

        timestamp_description = "Last Change Time"
        category = "General Info"
        description = "Computer Name"
        registry_path = fr"{self.prefix}{reg_key}\{reg_value_name}"

        computer_name, last_modified = self.get_value_data(reg_key, reg_value_name)

        self.output.file_evidence(timestamp=last_modified, category=category, timestamp_description=timestamp_description,
                                  finding=computer_name, description=description, registry_path=registry_path,
                                  source=self.reg_hive_path)

    def get_last_shutdown(self):
        reg_key = fr"\{self.current_control_set}\Control\Windows"
        reg_value_name = "ShutdownTime"

        timestamp_description = "Last Shutdown Time"
        category = "General Info"
        description = "Last Shutdown Time"
        registry_path = fr"{self.prefix}{reg_key}\{reg_value_name}"
        
        shutdown_time_hex_bytes, _ = self.get_value_data(reg_key, reg_value_name)
        shutdown_time = self.convert_hex_filetime(shutdown_time_hex_bytes)

        self.output.file_evidence(timestamp=shutdown_time, category=category, timestamp_description=timestamp_description,
                                  finding=shutdown_time, description=description, registry_path=registry_path,
                                  source=self.reg_hive_path)
