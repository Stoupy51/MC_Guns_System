
# Imports
from stewbeet import Mem, write_advancement, write_versioned_function
from ..generator import McfunctionGenerator


class HurtPlayerGenerator(McfunctionGenerator):
    """ Generates the hurtplayer datapack functions. """

    def generate(self) -> None:
    	ns: str = self.ns
    	version: str = self.version

        # Advancement triggered when the player is hurt
    	write_advancement(f"{ns}:v{version}/zombies/hurt_player", {
    		"criteria": {
    			"requirement": {
    				"trigger": "minecraft:entity_hurt_player",
    			}
    		},
    		"rewards": {
    			"function": f"{ns}:v{version}/zombies/hurt_player/on_hurt",
    		},
    	})

    	# Function to apply downward motion to the player
    	self.func("zombies/hurt_player/on_hurt", f"""
# Revoke advancement and stop if the player is not in the zombies game
advancement revoke @s only {ns}:v{version}/zombies/hurt_player
execute unless data storage {ns}:zombies game{{state:"active"}} run return fail
execute unless score @s {ns}.zb.in_game matches 1.. run return fail

# Launch player downward to counter the slight jump boost from knockback.
function {ns}:v{version}/zombies/hurt_player/launch_downward
""")

    	# Function to apply downward motion to the player
    	self.func("zombies/hurt_player/launch_downward", r"""
# Launch player downward to counter the slight jump boost from knockback.
scoreboard players set $x player_motion.api.launch 0
scoreboard players set $y player_motion.api.launch -5000
scoreboard players set $z player_motion.api.launch 0
function player_motion:api/launch_xyz
""")


def generate_hurt_player() -> None:
	""" Module-level entry (preserved signature); delegates to :class:`HurtPlayerGenerator`. """
	HurtPlayerGenerator()()


