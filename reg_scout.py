
# Externals Imports
from regipy.registry import RegistryHive

# Internals Imports
from output import Output
from hives.security import SecurityHive
from hives.software import SoftwareHive
from hives.system import SystemHive
from hives.ntuser import NTUserHive


def main():

    output = Output(output_format="csv")
    reg_hive = RegistryHive(r"D:\Tools\KAPE\output\C\Windows\System32\config\SYSTEM")
    #reg_hive = RegistryHive(r"D:\Tools\KAPE\output\C\Users\Administrator\NTUSER.DAT")
    
    match reg_hive.hive_type:

        # Hanldes the SECURITY hive (located in the live registry in 'HKEY_LOCAL_MACHINE\SECURITY\')
        case "security":
            security_hive = SecurityHive(reg_hive, output)

        # Hanldes the SOFTWARE hive (located in the live registry in 'HKEY_LOCAL_MACHINE\SOFTWARE\')
        case "software":
            software_hive = SoftwareHive(reg_hive, output)
            print(software_hive.get_winlogon_shell())
            print(software_hive.get_operating_system())
            print(software_hive.detect_disabled_event_log())

        # Hanldes the SYSTEM hive (located in the live registry in 'HKEY_LOCAL_MACHINE\SYSTEM\')
        case "system":
            system_hive = SystemHive(reg_hive, output)
            system_hive.get_computer_name()
            system_hive.get_last_shutdown()

        # Hanldes the NTUSER.DAT hive (located in the live registry in 'HKEY_CURRENT_USER\' for the appropriate user)
        case "ntuser":
            ntuser_hive = NTUserHive(reg_hive, output)
            ntuser_hive.get_used_sysinternals()

        case _:
            print(f"'{reg_hive.hive_type}' didn't match any supported hive types")

    output.export()
        

if __name__ == "__main__":
    main()
