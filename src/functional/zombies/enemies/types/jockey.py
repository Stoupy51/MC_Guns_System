""" The chicken jockey round: every ordinary zombie spawn is an invisible baby zombie riding a chicken. """
# Imports
from stewbeet import Mem, write_versioned_function

# Constants
JOCKEY_FIRST_ROUND: int = 8
JOCKEY_EVERY: int = 10
""" A jockey round is every JOCKEY_EVERY rounds from JOCKEY_FIRST_ROUND, so it never lands on a multiple of 5, the special rounds. """


# Functions
def write_jockey() -> None:
	ns: str = Mem.ctx.project_id
	version: str = Mem.ctx.project_version

	## The chicken's movement_speed steers the pair (the rider uses its mount's move control), so the chicken is the enemy:
	## it carries zombie_round, the round's speed and the stuck rescue, and the rider only fights.
	jockey_nbt: str = (
		'{entity:"minecraft:chicken",jockey:"mount",nbt:{IsChickenJockey:1b},riders:[{entity:"minecraft:zombie",jockey:"rider",'
		'nbt:{IsBaby:1b,active_effects:[{id:"minecraft:invisibility",amplifier:0b,duration:-1,show_particles:0b,show_icon:0b}]}}]}'
	)

	## Run as the spawn marker with its compound in _mob.
	write_versioned_function("zombies/jockey/replace_mob", f"""
execute unless data storage {ns}:temp _mob{{entity:"zombie"}} unless data storage {ns}:temp _mob{{entity:"minecraft:zombie"}} run return 0
execute if data storage {ns}:temp _mob.nbt run return 0
execute if data storage {ns}:temp _mob.riders[0] run return 0
execute if data storage {ns}:temp _mob.gun run return 0
data modify storage {ns}:temp _mob merge value {jockey_nbt}
""")

	## Run as the rider, once built.
	write_versioned_function("zombies/jockey/as_rider", f"""
tag @s remove {ns}.zombie_round
tag @s add {ns}.zb_jockey
tag @s add {ns}.zb_jockey_rider
""")

	## Run as the chicken, once its rider is on: the marker must sit after the rider, or the first passenger is not a mob and nothing steers.
	write_versioned_function("zombies/jockey/seat_marker", f"""
execute on passengers if entity @s[type=minecraft:marker] run function {ns}:v{version}/zombies/jockey/reseat_marker
""")
	write_versioned_function("zombies/jockey/reseat_marker", f"""
ride @s dismount
ride @s mount @n[type=minecraft:chicken,tag={ns}.zb_new_root,distance=..2]
""")

	## Run as the part (chicken or rider) whose Health just reached 0, from its death-watch marker.
	write_versioned_function("zombies/jockey/link", f"""
tag @s add {ns}.zb_jockey_linked

# The last hit stamp of either part pays the kill's power-up roll.
scoreboard players set #zb_jk_hit {ns}.data 0
scoreboard players operation #zb_jk_hit {ns}.data = @s {ns}.zb.player_hit
execute if entity @s[tag={ns}.zb_jockey_rider] on vehicle run function {ns}:v{version}/zombies/jockey/kill_mate
execute unless entity @s[tag={ns}.zb_jockey_rider] on passengers if entity @s[tag={ns}.zb_jockey_rider] run function {ns}:v{version}/zombies/jockey/kill_mate
""")
	write_versioned_function("zombies/jockey/kill_mate", f"""
execute if entity @s[tag={ns}.zb_jockey_linked] run return 0
tag @s add {ns}.zb_jockey_linked
scoreboard players operation @s {ns}.zb.player_hit > #zb_jk_hit {ns}.data

# Unattributed: the player's kill count only grew for the part they hit.
kill @s
""")

	## Run as a dying chicken, before anything else: the rider and its marker leave with it.
	write_versioned_function("zombies/jockey/clear_rider", f"""
execute on passengers if entity @s[tag={ns}.zb_jockey_rider] run function {ns}:v{version}/zombies/jockey/remove_rider
""")
	write_versioned_function("zombies/jockey/remove_rider", """
execute on passengers if entity @s[type=minecraft:marker] run kill @s
tp @s ~ -10000 ~
""")

