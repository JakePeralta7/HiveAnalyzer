from regipy.registry import RegistryHive
import datetime


class SystemHive:
    def __init__(self, reg_hive):
        self.reg_hive = reg_hive
        self.get_current_control_set()
    
    def get_current_control_set(self):
        
        # We can determine what is the CurrentControlSet based on 'HKEY_LOCAL_MACHINE\SYSTEM\Select\Current'
        current_control_set_value = self.reg_hive.get_key(r"\Select").get_value("Current")
        
        match current_control_set_value:
            case 1:
                self.current_control_set = "ControlSet001"
            case 2:
                self.current_control_set = "ControlSet002"
            case _:
                raise Exception("Couldn't find the current control set")

    def get_computer_name(self):
        return self.reg_hive.get_key(fr"\{self.current_control_set}\Control\ComputerName\ComputerName").get_value("ComputerName")

    def get_last_shutdown(self):
        shutdown_time_hex_bytes = self.reg_hive.get_key(fr"\{self.current_control_set}\Control\Windows").get_value("ShutdownTime")

        # Convert the hex value to a decimal timestamp
        shutdown_time_decimal = int.from_bytes(shutdown_time_hex_bytes, byteorder='little', signed=False) / 10**7
        
        # Convert the decimal timestamp to a datetime object
        shutdown_time = datetime.datetime(1601, 1, 1) + datetime.timedelta(seconds=shutdown_time_decimal)
    
        return shutdown_time
