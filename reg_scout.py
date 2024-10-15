
# Externals Imports
from regipy.registry import RegistryHive

# Internals Imports
from hives.security import SecurityHive
from hives.software import SoftwareHive
from hives.system import SystemHive


def main():
    reg_hive = RegistryHive(r"D:\Tools\KAPE\output\C\Windows\System32\config\SYSTEM")
    
    match reg_hive.hive_type:

        # Hanldes the SECURITY hive (located in the live registry in 'HKEY_LOCAL_MACHINE\SECURITY\')
        case "security":
            security_hive = SecurityHive(reg_hive)

        # Hanldes the SOFTWARE hive (located in the live registry in 'HKEY_LOCAL_MACHINE\SOFTWARE\')
        case "software":
            software_hive = SoftwareHive(reg_hive)
            print(software_hive.get_winlogon_shell())

        # Hanldes the SYSTEM hive (located in the live registry in 'HKEY_LOCAL_MACHINE\SYSTEM\')
        case "system":
            system_hive = SystemHive(reg_hive)
            computer_name = system_hive.get_computer_name()
            print(computer_name)

            last_shutdown_time = system_hive.get_last_shutdown()
            print(last_shutdown_time)
        

if __name__ == "__main__":
    main()
