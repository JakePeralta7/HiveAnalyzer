class Evidence:
    def __init__(self, timestamp, category, timestamp_description, description, finding, registry_path, source):

        # The timestamp that's relevant for the evidence
        self.timestamp = timestamp

        # Categorize the evidence (for example: 'General Information')
        self.category = category

        # Explains what the timestamp stands for (for example: 'First Execution')
        self.timestamp_description = timestamp_description

        # Description of the finding (for example: 'Computer Name')
        self.description = description

        # The data itself (for example: the computer's name)
        self.finding = finding

        # The path of the registry from which the evidence was extracted
        self.registry_path = registry_path

        # The hive file path from which the evidence was extracted
        self.source = source
