
# External Imports
import logging

# Internal Imports
from HiveAnalyzer.hive import Hive


logger = logging.getLogger(__name__)


class SoftwareHive(Hive):
    def __init__(self, reg_hive_path, reg_hive, output, findings_config):
        super().__init__(reg_hive_path, reg_hive, output, findings_config)
        self.prefix = r"HKEY_LOCAL_MACHINE\SOFTWARE"
        self.get_configurable()

    def get_winlogon_shell(self):
        reg_key = r"\Microsoft\Windows NT\CurrentVersion\Winlogon"
        reg_value_name = "Shell"

        timestamp_desc = "Last Registry Key Change"
        category = "Detection Signature"
        description = r"Winlogon\Shell was Replaced"
        registry_path = fr"{self.prefix}{reg_key}\{reg_value_name}"

        shell_executable, last_modified = self.get_value_data(reg_key, reg_value_name)

        if shell_executable != "explorer.exe":
            self.output.file_evidence(timestamp=last_modified, category=category, timestamp_desc=timestamp_desc,
                                  finding=shell_executable, description=description, registry_path=registry_path,
                                  source=self.reg_hive_path)

    def detect_disabled_event_log(self):
        reg_key = r"\Microsoft\Windows\CurrentVersion\WINEVT\Channels"
        reg_value_name = "Enabled"

        timestamp_desc = "Last Registry Key Change"
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
                self.output.file_evidence(timestamp=last_modified, category=category, timestamp_desc=timestamp_desc,
                                  finding=event_log_name, description=description, registry_path=registry_path,
                                  source=self.reg_hive_path)
            
