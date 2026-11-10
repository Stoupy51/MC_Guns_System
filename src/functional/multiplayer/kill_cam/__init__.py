""" The final kill cam: when a player kill ends a match, every match player watches the final killer's chain again from their eyes.

The replay is a puppet show, not a recording of the world: one mannequin per other player, driven by recorded positions, rotations and poses.
`specs/004-multiplayer-kill-cam` holds the design.
"""
# Imports
from .chain import write_kill_cam_chain
from .playback import write_kill_cam_playback
from .record import write_kill_cam_recording


# Functions
def generate_kill_cam() -> None:
	write_kill_cam_recording()
	write_kill_cam_chain()
	write_kill_cam_playback()

