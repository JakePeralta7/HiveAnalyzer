
# External Imports
from datetime import datetime, timedelta

class Hive:
    def __init__(self, reg_hive_path, reg_hive, output):
        self.reg_hive_path = reg_hive_path
        self.reg_hive = reg_hive
        self.output = output

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
