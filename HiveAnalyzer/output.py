
# External Imports
from csv import DictWriter
import logging

# Internal Imports
from HiveAnalyzer.evidence import Evidence


logger = logging.getLogger(__name__)


class Output:
    def __init__(self, output_format="csv", output_path="test.csv"):
        self.output_format = output_format
        self.output_path = output_path
        self.evidence_list = []

    def file_evidence(self, timestamp, category, timestamp_desc, description, finding, registry_path, source):
        evidence = Evidence(timestamp, category, timestamp_desc, description, finding, registry_path, source)
        self.evidence_list.append(evidence)
    
    def export(self):
        match self.output_format:
            case "csv":
                with open(self.output_path, 'w', newline='') as csvfile:
                    fieldnames = ["timestamp", "category", "timestamp_desc", "description", "finding", "registry_path",
                                  "source"]
                    writer = DictWriter(csvfile, fieldnames=fieldnames)
                    writer.writeheader()
                    for current_evidence in self.evidence_list:
                        current_evidence_dict = current_evidence.__dict__
                        writer.writerow(current_evidence_dict)
        print(f"output was successfully exported to '{self.output_path}'")
