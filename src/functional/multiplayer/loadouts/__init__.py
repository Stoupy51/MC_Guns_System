
# Re-export constants from catalogs for backwards compatibility
from .actions import generate_actions
from .browsing import generate_browsing
from .catalogs import *
from .class_selection import *
from .editor import generate_editor
from .storage import generate_storage


def generate_custom_loadouts() -> None:
	generate_storage()
	generate_editor()
	generate_browsing()
	generate_actions()

