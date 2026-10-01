""" Custom loadout editor, a CoD-style hub.

The editor opens on a hub listing every category (guns, magazines, grenades, perks) with the current selection on each button and the Pick-10 points at the top.
A row opens a short submenu (primary: gun, scope, camo) that returns to the hub when done.
Rows whose prerequisite is missing (magazines without their gun, saving without a primary) are grayed out as "Unavailable".

Points are never deducted or refunded step by step: editor/recompute_points derives the cost from the current state.
Every change goes through a snapshot and commit check that reverts and denies when the budget would be exceeded.
"""
# Imports
from .camos import write_editor_camos
from .dialogs import write_editor_dialog_base
from .equipment import write_editor_equipment
from .hub import write_editor_hub
from .mags import write_editor_mags
from .perks import write_editor_perks
from .save import write_editor_save
from .scopes import write_editor_scopes
from .state import write_editor_state
from .weapons import write_editor_weapons


# Functions
def generate_editor() -> None:
	write_editor_state()
	write_editor_hub()
	write_editor_dialog_base()
	write_editor_weapons()
	write_editor_scopes()
	write_editor_camos()
	write_editor_mags()
	write_editor_equipment()
	write_editor_perks()
	write_editor_save()

