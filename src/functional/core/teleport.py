
# Shared teleport macro
from ..generator import McfunctionGenerator


class SharedTeleport(McfunctionGenerator):
	""" Writes the shared teleport-to-position macro used across modes. """

	def generate(self) -> None:
		## Teleport to position (macro)
		## Usage: function shared/tp_to_position with storage {ns}:temp _tp
		self.func("shared/tp_to_position", "$tp @s $(x) $(y) $(z)")


def write_shared_teleport_functions() -> None:
	""" Module-level entry point (preserved signature); delegates to :class:`SharedTeleport`. """
	SharedTeleport()()
