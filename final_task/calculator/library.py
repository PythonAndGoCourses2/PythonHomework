class Library(dict):
    """Class is designed to work with modules."""
    def __init__(self, *modules: list):
        super().__init__()

        self['abs'] = abs
        self['round'] = round

        self.update(*modules)
    
    def update(self, *modules: list):
        """Adds functions and veriables from got module names to dictionary."""
        for module in modules:
            super().update(__import__(module).__dict__)