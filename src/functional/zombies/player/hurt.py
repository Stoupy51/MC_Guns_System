""" Zombies damage handling for players, including knockback and perk passives. """
# Imports
from stewbeet import Mem, write_advancement, write_versioned_function


# Functions
def generate_hurt_player() -> None:
	ns: str = Mem.ctx.project_id
	version: str = Mem.ctx.project_version

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

	write_versioned_function("zombies/hurt_player/on_hurt", f"""
# Revoked first, so it can trigger again.
advancement revoke @s only {ns}:v{version}/zombies/hurt_player
execute unless data storage {ns}:zombies game{{state:"active"}} run return fail
execute unless score @s {ns}.zb.in_game matches 1.. run return fail

# Counters the small upward knockback.
function {ns}:v{version}/zombies/hurt_player/launch_downward

# Budgeted per player (see vocals). `unless` rather than a return: the passives below run on every hit.
execute unless score @s {ns}.zb.vox_attack > #total_tick {ns}.data run function {ns}:v{version}/zombies/vocals/attack

execute if score @s {ns}.special.widows_wine matches 1 run function {ns}:v{version}/zombies/perks/widows_on_hurt
""")

	write_versioned_function("zombies/hurt_player/launch_downward", r"""
# Counters the small upward knockback.
scoreboard players set $x player_motion.api.launch 0
scoreboard players set $y player_motion.api.launch -5000
scoreboard players set $z player_motion.api.launch 0
function player_motion:api/launch_xyz
""")

