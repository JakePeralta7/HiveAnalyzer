
# Internal Imports
from evidence import Evidence


class Output:
    def __init__(self, output_format="csv"):
        self.output_format = output_format
        self.evidence_list = []

    def file_evidence(self, timestamp, timestamp_description, source, category, registry_path, description, finding):
        evidence = Evidence(timestamp, timestamp_description, source, category, registry_path, description, finding)
        self.evidence_list.append(evidence)
    
    def export(self, file_path=None):
        for evidence in self.evidence_list:
            print(str(evidence))
