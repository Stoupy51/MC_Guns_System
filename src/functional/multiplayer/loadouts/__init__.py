""" Custom loadouts: the editor, browsing them, and the actions on a saved one. """
# Imports
from .actions import generate_actions
from .browsing import generate_browsing
from .class_selection import generate_class_selection
from .editor import generate_editor
from .storage import generate_storage

__all__ = ["generate_class_selection", "generate_custom_loadouts"]


# Functions
def generate_custom_loadouts() -> None:
	generate_storage()
	generate_editor()
	generate_browsing()
	generate_actions()

