
# Shared teleport macro
from stewbeet import write_versioned_function


def write_shared_teleport_functions() -> None:
		## Teleport to position (macro)
		## Usage: function shared/tp_to_position with storage {ns}:temp _tp
		write_versioned_function("shared/tp_to_position", "$tp @s $(x) $(y) $(z)")
