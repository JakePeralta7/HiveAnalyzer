class Evidence:
    def __init__(self, timestamp, timestamp_description, source, category, registry_path, description, finding):

        # The timestamp that's relevant for the evidence
        self.timestamp = timestamp

        # Explains what the timestamp stands for (for example: 'First Execution')
        self.timestamp_description = timestamp_description

        # The hive file path from which the evidence was extracted
        self.source = source

        # Categoriize the evidence (for example: 'General Information')
        self.category = category

        # The path of the registry from which the evidence was extracted
        self.registry_path = registry_path

        # Decsription of the finding (for example: 'Computer Name')
        self.description = description

        # The data itself (for example: the computer's name)
        self.finding = finding

    def __str__(self):
        return f"{self.timestamp}, {self.category}, {self.description}, {self.finding}"
