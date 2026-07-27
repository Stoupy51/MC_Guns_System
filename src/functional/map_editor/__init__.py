""" Map editor, generic across multiplayer, missions and zombies.

Provides an in-game editor with mode switching for placing map elements.

Elements are placed via spawn eggs detected by advancement (item_used_on_block).
Markers in the world represent elements during editing; storage is written on save. """
# Imports
from .config import write_editor_config
from .coord_stick import write_coord_stick
from .destroy import write_editor_destroy
from .displays import write_editor_displays
from .doors import write_editor_doors
from .enter import write_editor_enter
from .exit import write_editor_exit
from .handlers import write_editor_handlers
from .menu import write_editor_menu
from .place import write_editor_place
from .save import write_editor_save
from .summon import write_editor_summon
from .tick import write_editor_tick
from .tools import write_editor_tools
from .zb_config import write_editor_zb_config


# Functions
def generate_map_editor() -> None:
	write_editor_menu()
	write_editor_enter()
	write_editor_summon()
	write_editor_tools()
	write_editor_place()
	write_editor_handlers()
	write_editor_destroy()
	write_editor_config()
	write_editor_zb_config()
	write_editor_doors()
	write_editor_save()
	write_editor_exit()
	write_editor_displays()
	write_editor_tick()
	write_coord_stick()

