""" Zombies damage handling for players, including knockback and perk passives. """
# Imports
from stewbeet import Mem, write_advancement, write_versioned_function


# Functions
def generate_hurt_player() -> None:
	ns: str = Mem.ctx.project_id
	version: str = Mem.ctx.project_version

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
	write_versioned_function("zombies/hurt_player/on_hurt", f"""
# Revoke advancement and stop if the player is not in the zombies game
advancement revoke @s only {ns}:v{version}/zombies/hurt_player
execute unless data storage {ns}:zombies game{{state:"active"}} run return fail
execute unless score @s {ns}.zb.in_game matches 1.. run return fail

# Launch player downward to counter the slight jump boost from knockback.
function {ns}:v{version}/zombies/hurt_player/launch_downward

# Melee grunt from whatever just hit us, budgeted per player (see enemies/vocals.py). Gated with
# `unless` rather than an early return, because the perk passives below still have to run on every hit.
execute unless score @s {ns}.zb.vox_attack > #total_tick {ns}.data run function {ns}:v{version}/zombies/vocals/attack

# Widow's Wine passive: consume a web grenade and burst webbing around the hurt owner.
execute if score @s {ns}.special.widows_wine matches 1 run function {ns}:v{version}/zombies/perks/widows_on_hurt
""")

	# Function to apply downward motion to the player
	write_versioned_function("zombies/hurt_player/launch_downward", r"""
# Launch player downward to counter the slight jump boost from knockback.
scoreboard players set $x player_motion.api.launch 0
scoreboard players set $y player_motion.api.launch -5000
scoreboard players set $z player_motion.api.launch 0
function player_motion:api/launch_xyz
""")

