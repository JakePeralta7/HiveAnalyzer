from regipy.registry import RegistryHive
from regipy.utils import convert_wintime


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
