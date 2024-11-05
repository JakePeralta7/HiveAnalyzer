
# External Imports
import logging

# Internal Imports
from HiveAnalyzer.hive import Hive


logger = logging.getLogger(__name__)


class SystemHive(Hive):
    def __init__(self, reg_hive_path, reg_hive, output, current_findings_config):
        super().__init__(reg_hive_path, reg_hive, output, current_findings_config)
        self.prefix = r"HKEY_LOCAL_MACHINE\SYSTEM"
        self.current_control_set = self.get_current_control_set()
        self.get_configurable()
    
    def get_current_control_set(self):
        logger.info("Trying to figure out the current control set")
        
        # We can determine what is the CurrentControlSet based on 'HKEY_LOCAL_MACHINE\SYSTEM\Select\Current'
        reg_key = r"\Select"
        reg_value_name = "Current"
        current_control_set_value, _ = self.get_value_data(reg_key, reg_value_name)
        
        match current_control_set_value:
            case 1:
                current_control_set = "ControlSet001"
            case 2:
                current_control_set = "ControlSet002"
            case _:
                logger.error("Couldn't find the current control set")
                current_control_set = None
        logger.info(f"CurrentControlSet is {current_control_set}")
        return current_control_set
