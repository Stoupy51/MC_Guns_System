""" Block tag definitions written at build time. """
# Imports
from .materials import write_material_tags
from .raycast import write_raycast_tags
from .sounds import write_sound_tags
from .surfaces import write_surface_tags
from .world import write_world_tags


# Functions
def main() -> None:
	write_raycast_tags()
	write_material_tags()
	write_surface_tags()
	write_world_tags()
	write_sound_tags()

