
# Externals Imports
from regipy.registry import RegistryHive
from construct.core import ConstError
from os import walk

# Internals Imports
from output import Output
from hives.security import SecurityHive
from hives.software import SoftwareHive
from hives.system import SystemHive
from hives.ntuser import NTUserHive


def handle_registry_hive(reg_hive_path, reg_hive, output):
    match reg_hive.hive_type:

        # Handles the SECURITY hive (located in the live registry in 'HKEY_LOCAL_MACHINE\SECURITY\')
        case "security":
            security_hive = SecurityHive(reg_hive_path, reg_hive, output)

        # Handles the SOFTWARE hive (located in the live registry in 'HKEY_LOCAL_MACHINE\SOFTWARE\')
        case "software":
            software_hive = SoftwareHive(reg_hive_path, reg_hive, output)
            software_hive.get_winlogon_shell()
            software_hive.get_operating_system()
            software_hive.detect_disabled_event_log()

        # Handles the SYSTEM hive (located in the live registry in 'HKEY_LOCAL_MACHINE\SYSTEM\')
        case "system":
            system_hive = SystemHive(reg_hive_path, reg_hive, output)
            system_hive.get_computer_name()
            system_hive.get_last_shutdown()

        # Handles the NTUSER.DAT hive (located in the live registry in 'HKEY_CURRENT_USER\' for the appropriate user)
        case "ntuser":
            ntuser_hive = NTUserHive(reg_hive_path, reg_hive, output)
            ntuser_hive.get_used_sysinternals()

        case "usrclass":
            pass

        case "amcache":
            pass

        case "sam":
            pass

        # Handles instances where couldn't identify
        case None:
            pass

        case _:
            print(f"'{reg_hive.hive_type}' didn't match any supported hive types")

    return output


def main():

    output = Output(output_format="csv", output_path="zibi.csv")

    artifacts_dir = r"C:\Users\flare\Documents\output"
    for dir_path, dir_names, file_names in walk(artifacts_dir):
        for file_name in file_names:
            current_file_path = fr"{dir_path}\{file_name}"
            try:
                reg_hive = RegistryHive(current_file_path)
                output = handle_registry_hive(current_file_path, reg_hive, output)
            except ConstError:
                continue

    output.export()


if __name__ == "__main__":
    main()
