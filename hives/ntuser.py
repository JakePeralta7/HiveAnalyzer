
# External Imports
from regipy import convert_wintime
from regipy.exceptions import RegistryKeyNotFoundException
from pathlib import Path

# Internal Imports
from hive import Hive


class NTUserHive(Hive):
    def __init__(self, reg_hive_path, reg_hive, output):
        super().__init__(reg_hive_path, reg_hive, output)
        self.prefix = "HKEY_CURRENT_USER"

        # The Username is always the name of the directory in which NTUSER.DAT is stored
        self.username = self.get_username()

    def get_username(self):
        return Path(self.reg_hive_path).parent.parts[-1]

    def is_user_signed_in(self):
        reg_key = r"\Software\Microsoft\Windows\CurrentVersion\Explorer"
        reg_value_name = "UserSignedIn"
        print(self.get_value_data(reg_key, reg_value_name))

    def get_logon_count(self):
        reg_key = r"\Software\Microsoft\Windows\CurrentVersion\Explorer"
        reg_value_name = "LogonCount"

        return self.get_value_data(reg_key, reg_value_name)

    def get_last_logon(self):
        reg_key = r"\Software\Microsoft\Windows\CurrentVersion\Explorer\SessionInfo\2"
        reg_value_name = "LastLogonTime"

        last_logon_time_hex_bytes = self.get_value_data(reg_key, reg_value_name)
        last_logon_time = self.convert_hex_filetime(last_logon_time_hex_bytes)
    
        return last_logon_time

    def get_used_sysinternals(self):
        reg_key =r"\Software\Sysinternals"

        timestamp_description = "First Used"
        category = "Evidence of Execution"
        description = f"{self.username} accepted the EULA of a Sysinternals program"

        try:
            for subkey in self.reg_hive.get_key(reg_key).iter_subkeys():
                program_name = subkey.name

                registry_path = fr"{self.prefix}{reg_key}\{program_name}"

                last_modified = self.convert_decimal_filetime(subkey.header.last_modified)

                self.output.file_evidence(timestamp=last_modified, category=category,
                                          timestamp_description=timestamp_description, description=description,
                                          finding=program_name, registry_path=registry_path, source=self.reg_hive_path)
        except RegistryKeyNotFoundException:
            pass
