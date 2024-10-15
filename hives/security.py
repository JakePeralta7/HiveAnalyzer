from regipy.registry import RegistryHive
from regipy.utils import convert_wintime


class SecurityHive():
    def __init__(self, reg_hive):
        self.reg_hive = reg_hive
