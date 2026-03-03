
# Re-export constants from catalogs for backwards compatibility
from .actions import generate_actions
from .browsing import generate_browsing
from .catalogs import (  # noqa: F401
	EQUIPMENT_PRESETS,
	PRIMARY_WEAPONS,
	SECONDARY_WEAPONS,
	TRIG_DELETE_BASE,
	TRIG_EDITOR_START,
	TRIG_EQUIPMENT_BASE,
	TRIG_FAVORITE_BASE,
	TRIG_LIKE_BASE,
	TRIG_MARKETPLACE,
	TRIG_MY_LOADOUTS,
	TRIG_PRIMARY_BASE,
	TRIG_PRIMARY_SCOPE_BASE,
	TRIG_SAVE_PRIVATE,
	TRIG_SAVE_PUBLIC,
	TRIG_SECONDARY_BASE,
	TRIG_SECONDARY_NONE,
	TRIG_SECONDARY_SCOPE_BASE,
	TRIG_SELECT_BASE,
	TRIG_SET_DEFAULT_BASE,
	TRIG_TOGGLE_VIS_BASE,
	TRIG_UNSET_DEFAULT,
)
from .class_selection import generate_class_selection
from .editor import generate_editor
from .storage import generate_storage


def generate_custom_loadouts() -> None:
	generate_storage()
	generate_editor()
	generate_browsing()
	generate_actions()


__all__ = [
	# TRIG_* constants re-exported for backwards compatibility
	"TRIG_DELETE_BASE",
	"TRIG_EDITOR_START",
	"TRIG_EQUIPMENT_BASE",
	"TRIG_FAVORITE_BASE",
	"TRIG_LIKE_BASE",
	"TRIG_MARKETPLACE",
	"TRIG_MY_LOADOUTS",
	"TRIG_PRIMARY_BASE",
	"TRIG_PRIMARY_SCOPE_BASE",
	"TRIG_SAVE_PRIVATE",
	"TRIG_SAVE_PUBLIC",
	"TRIG_SECONDARY_BASE",
	"TRIG_SECONDARY_NONE",
	"TRIG_SECONDARY_SCOPE_BASE",
	"TRIG_SELECT_BASE",
	"TRIG_SET_DEFAULT_BASE",
	"TRIG_TOGGLE_VIS_BASE",
	"TRIG_UNSET_DEFAULT",
	"generate_class_selection",
	"generate_custom_loadouts",
]
