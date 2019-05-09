"""
Exceptions for the importer module.
"""


class ModuleImportErrors(ModuleNotFoundError):
    """"""

    def __init__(self, module_names):
        super().__init__()
        self.modules_names = module_names

    def __str__(self):

        return f"no module named {', '.join(self.modules_names)}"
