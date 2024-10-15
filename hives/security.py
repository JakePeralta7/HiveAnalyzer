from hive import Hive


class SecurityHive(Hive):
    def __init__(self, reg_hive):
        super().__init__(reg_hive)
