
# Externals Imports
from regipy.registry import RegistryHive
from construct.core import ConstError
from os import walk
import logging

# Internals Imports
from HiveAnalyzer.output import Output
from HiveAnalyzer.hives.security import SecurityHive
from HiveAnalyzer.hives.software import SoftwareHive
from HiveAnalyzer.hives.system import SystemHive
from HiveAnalyzer.hives.ntuser import NTUserHive
from HiveAnalyzer.findings_config_handler import FindingsConfigHandler
from HiveAnalyzer.constants import BANNER


logger = logging.getLogger(__name__)


def handle_registry_hive(reg_hive_path, reg_hive, output, fc_handler):
    match reg_hive.hive_type:

        # Handles the SECURITY hive (located in the live registry in 'HKEY_LOCAL_MACHINE\SECURITY\')
        case "security":
            current_findings_config = fc_handler.finding_configs[reg_hive.hive_type]
            security_hive = SecurityHive(reg_hive_path, reg_hive, output, current_findings_config)

        # Handles the SOFTWARE hive (located in the live registry in 'HKEY_LOCAL_MACHINE\SOFTWARE\')
        case "software":
            current_findings_config = fc_handler.finding_configs[reg_hive.hive_type]
            software_hive = SoftwareHive(reg_hive_path, reg_hive, output, current_findings_config)

        # Handles the SYSTEM hive (located in the live registry in 'HKEY_LOCAL_MACHINE\SYSTEM\')
        case "system":
            current_findings_config = fc_handler.finding_configs[reg_hive.hive_type]
            system_hive = SystemHive(reg_hive_path, reg_hive, output, current_findings_config)

        # Handles the NTUSER.DAT hive (located in the live registry in 'HKEY_CURRENT_USER\' for the appropriate user)
        case "ntuser":
            current_findings_config = fc_handler.finding_configs[reg_hive.hive_type]
            ntuser_hive = NTUserHive(reg_hive_path, reg_hive, output, current_findings_config)

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
    fc_handler = FindingsConfigHandler()

    logging.basicConfig(
        filename='test.log',
        level=logging.INFO,
        format='%(asctime)s %(levelname)s [%(name)s.%(funcName)s:%(lineno)d] %(message)s',
        datefmt='%Y-%m-%d %H:%M:%S',
        encoding='utf-8'
    )

    logging.info("hive_analyzer execution started")
    logging.info(BANNER)
    
    output = Output(output_format="csv", output_path="zibi.csv")

    artifacts_dir = r"C:\Users\flare\Documents\output"
    for dir_path, dir_names, file_names in walk(artifacts_dir):
        for file_name in file_names:
            current_file_path = fr"{dir_path}\{file_name}"
            try:
                reg_hive = RegistryHive(current_file_path)
                output = handle_registry_hive(current_file_path, reg_hive, output, fc_handler)
            except ConstError:
                continue

    output.export()
