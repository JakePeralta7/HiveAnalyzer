
# External Imports
import logging

# Internal Imports
from HiveAnalyzer.hive import Hive


logger = logging.getLogger(__name__)


class SecurityHive(Hive):
    def __init__(self, reg_hive_path, reg_hive, output, findings_config):
        super().__init__(reg_hive_path, reg_hive, output, findings_config)
        self.prefix = r"HKEY_LOCAL_MACHINE\SECURITY"
        self.get_configurable()
