from regipy.registry import RegistryHive
from regipy.utils import convert_wintime

from hives.system import SystemHive


def handle_hive(reg_hive):
    print("Software Hive Handled!")
    print(reg_hive.get_key(r"\Microsoft\Windows NT\CurrentVersion\Winlogon").get_value("Shell"))


def main():
    reg_hive = RegistryHive(r"D:\Tools\KAPE\output\C\Windows\System32\config\SYSTEM")
    
    match reg_hive.hive_type:
        case "system":
            system_hive = SystemHive(reg_hive)
            print(system_hive.current_control_set)
        case "software":
            software.handle_hive(reg_hive)

if __name__ == "__main__":
    main()
