
# External Imports
from regipy import convert_wintime

# Internal Imports
from hive import Hive


class NTUserHive(Hive):
    def __init__(self, reg_hive):
        super().__init__(reg_hive)

    def get_username(self):
        reg_key = r"\Volatile Environment"
        reg_value_name = "USERNAME"
        self.username = self.get_value_data(reg_key, reg_value_name)

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
        last_logon_time = self.convert_filetime_timestamp(last_logon_time_hex_bytes)
    
        return last_logon_time

    def get_used_sysinternals(self):
        reg_key =r"\Software\Sysinternals"

        for subkey in self.reg_hive.get_key(reg_key).iter_subkeys():
            program_name = subkey.name
            first_used = convert_wintime(subkey.header.last_modified)
            print(f"{program_name} - {first_used}")
