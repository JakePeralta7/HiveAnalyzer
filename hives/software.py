class SoftwareHive():
    def __init__(self, reg_hive):
        self.reg_hive = reg_hive

    def get_winlogon_shell(self):
        return self.reg_hive.get_key(r"\Microsoft\Windows NT\CurrentVersion\Winlogon").get_value("Shell")
