
# Internal Imports
from hive import Hive


class SoftwareHive(Hive):
    def __init__(self, reg_hive_path, reg_hive, output):
        super().__init__(reg_hive_path, reg_hive, output)
        self.prefix = r"HKEY_LOCAL_MACHINE\SOFTWARE"

    def get_winlogon_shell(self):
        reg_key = r"\Microsoft\Windows NT\CurrentVersion\Winlogon"
        reg_value_name = "Shell"

        timestamp_description = "Last Key Change Time"
        category = "Detection Signature"
        description = r"Winlogon\Shell was Replaced"
        registry_path = fr"{self.prefix}{reg_key}\{reg_value_name}"

        shell_executable, last_modified = self.get_value_data(reg_key, reg_value_name)

        if shell_executable != "explorer.exe":
            self.output.file_evidence(timestamp=last_modified, category=category, timestamp_description=timestamp_description,
                                  finding=shell_executable, description=description, registry_path=registry_path,
                                  source=self.reg_hive_path)

    def get_operating_system(self):
        reg_key = r"\Microsoft\Windows NT\CurrentVersion"
        reg_value_name = "ProductName"

        timestamp_description = "Last Key Change Time"
        category = "General Info"
        description = r"Operating System"
        registry_path = fr"{self.prefix}{reg_key}\{reg_value_name}"

        operating_system, last_modified = self.get_value_data(reg_key, reg_value_name)

        self.output.file_evidence(timestamp=last_modified, category=category, timestamp_description=timestamp_description,
                                  finding=operating_system, description=description, registry_path=registry_path,
                                  source=self.reg_hive_path)

    def detect_disabled_event_log(self):
        reg_key = r"\Microsoft\Windows\CurrentVersion\WINEVT\Channels"
        reg_value_name = "Enabled"

        timestamp_description = "Last Time Key Modified"
        category = "Detection Signature"
        description = "Disabled Important Event Logs"

        important_event_logs = [
            "Microsoft-Windows-TaskScheduler/Operational",
            "Microsoft-Windows-PowerShell/Operational"
            ]

        for event_log_name in important_event_logs:
            current_reg_key = fr"{reg_key}\{event_log_name}"
            event_log_status, last_modified = self.get_value_data(current_reg_key, reg_value_name)
            if event_log_status == 0:
                registry_path = fr"{self.prefix}{current_reg_key}\{reg_value_name}"
                self.output.file_evidence(timestamp=last_modified, category=category, timestamp_description=timestamp_description,
                                  finding=event_log_name, description=description, registry_path=registry_path,
                                  source=self.reg_hive_path)
            
