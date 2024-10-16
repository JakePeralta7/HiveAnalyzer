
# Internal Imports
from hive import Hive


class SoftwareHive(Hive):
    def __init__(self, reg_hive):
        super().__init__(reg_hive)

    def get_winlogon_shell(self):
        reg_key = r"\Microsoft\Windows NT\CurrentVersion\Winlogon"
        reg_value_name = "Shell"
        return self.get_value_data(reg_key, reg_value_name)

    def get_operating_system(self):
        reg_key = r"\Microsoft\Windows NT\CurrentVersion"
        reg_value_name = "ProductName"
        return self.get_value_data(reg_key, reg_value_name)

    def detect_disabled_event_log(self):
        reg_key = r"\Microsoft\Windows\CurrentVersion\WINEVT\Channels"
        reg_value_name = "Enabled"

        timestamp_description = "Last Time Key Modified"
        category = ""
        description = "Disabled Important Event Logs"

        important_event_logs = [
            "Microsoft-Windows-TaskScheduler/Operational",
            "Microsoft-Windows-PowerShell/Operational"
            ]

        for event_log_name in important_event_logs:
            current_reg_key = fr"{reg_key}\{event_log_name}"
            event_log_status, last_modified = self.get_value_data(current_reg_key, reg_value_name)
            if self.get_value_data(current_reg_key, reg_value_name) == 0:
                self.output.file_evidence(timestamp=last_modified, timestamp_description=timestamp_description,
                                  source=None, category=category, registry_path=None, description=description,
                                  finding=event_log_name)
            
