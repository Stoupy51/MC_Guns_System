""" Round-end free pickups, tearing a body down and respawning near the team. """
# Imports
from stewbeet import Mem, write_versioned_function

from ....helpers import MGS_TAG
from ....helpers.text import Text

# Constants
SPAWN_NEAR_BODY: int = 20
""" A player respawning lands on an unlocked player spawn within this many blocks of where they went down; otherwise on the nearest alive teammate. """


# Functions
def write_round_end_revives() -> None:
	ns: str = Mem.ctx.project_id
	version: str = Mem.ctx.project_version

	# Revive or respawn every spectating player at round end.
	write_versioned_function("zombies/revive/round_respawn", f"""
# A player still downed when the round ends is revived for free, keeping the loadout: the bleed timer never ran out.
# revive_complete never touches the hotbar; perks stay lost. Must run before the respawn below, which resets the loadout.
execute as @a[tag={ns}.downed_spectator,scores={{{ns}.zb.in_game=1}}] run function {ns}:v{version}/zombies/revive/revive_complete

# The rest bled out during the round, which costs the loadout.
execute as @a[scores={{{ns}.zb.in_game=1}},gamemode=spectator] run function {ns}:v{version}/zombies/revive/do_round_respawn
""")

	write_versioned_function("zombies/revive/do_round_respawn", f"""
# Still downed: tear that state down, or the mannequin, HUD and camera would be orphaned.
execute if entity @s[tag={ns}.downed_spectator] run function {ns}:v{version}/zombies/revive/clear_downed_state

spectate @s
gamemode adventure @s

function {ns}:v{version}/zombies/revive/respawn_near_player

# The stamina system owns the hunger bar.
scoreboard players set @s {ns}.stam_seen 0
effect give @s minecraft:instant_health 1 255 true

execute if score @s {ns}.zb.perk.juggernog matches 1.. run attribute @s minecraft:max_health base set 40
execute unless score @s {ns}.zb.perk.juggernog matches 1.. run attribute @s minecraft:max_health base set 20

function {ns}:v{version}/zombies/inventory/give_respawn_loadout
# Or Max Ammo hands the lost tactical back. Not in the loadout itself: a Who's Who revive restores the tactical too.
scoreboard players set @s {ns}.zb.tactical_type 0

# Tombstone: activate the marker and its 60 s recovery timer.
function {ns}:v{version}/zombies/perks/tombstone_on_respawn

# Run as the respawning player.
function {ns}:v{version}/shared/maps/call_script_at_base {{mode:"zombies",script:"respawn"}}

tellraw @a[scores={{{ns}.zb.in_game=1}}] [{MGS_TAG},{Text.player(ns, "@s", side="zb", color="green")},{{"text":" has respawned!","color":"gray"}}]
""")

	## Tear down the downed mannequin, HUD and camera of @s (by downed_id) and dismount.
	write_versioned_function("zombies/revive/clear_downed_state", f"""
scoreboard players operation #my_downed_id {ns}.data = @s {ns}.zb.downed_id
execute as @e[tag={ns}.downed_hud,predicate={ns}:v{version}/zombies/revive/downed_id_match] run kill @s
execute as @e[tag={ns}.downed_mannequin,predicate={ns}:v{version}/zombies/revive/downed_id_match] run kill @s
execute as @e[tag={ns}.downed_cam,predicate={ns}:v{version}/zombies/revive/downed_id_match] run kill @s
ride @s dismount
scoreboard players set @s {ns}.zb.downed 0
scoreboard players set @s {ns}.zb.revive_p 0
tag @s remove {ns}.downed_spectator
""")

	## Run as the player: where they went down. On the unlocked player spawn within SPAWN_NEAR_BODY blocks of that spot, else on the alive teammate nearest to it.
	write_versioned_function("zombies/revive/respawn_near_player", f"""
execute unless data entity @s LastDeathLocation run return run function {ns}:v{version}/zombies/revive/respawn_at_random_spawn

# The player is excluded from the teammates they join.
tag @s add {ns}.spawn_pending
data modify storage {ns}:temp _body set value {{}}
data modify storage {ns}:temp _body.dimension set from entity @s LastDeathLocation.dimension
execute store result storage {ns}:temp _body.x int 1 run data get entity @s LastDeathLocation.pos[0]
execute store result storage {ns}:temp _body.y int 1 run data get entity @s LastDeathLocation.pos[1]
execute store result storage {ns}:temp _body.z int 1 run data get entity @s LastDeathLocation.pos[2]
scoreboard players set #respawn_done {ns}.data 0
function {ns}:v{version}/zombies/revive/respawn_at_body with storage {ns}:temp _body
tag @s remove {ns}.spawn_pending
execute if score #respawn_done {ns}.data matches 0 run function {ns}:v{version}/zombies/revive/respawn_at_random_spawn
""")

	write_versioned_function("zombies/revive/respawn_at_body", f"""
$execute in $(dimension) positioned $(x) $(y) $(z) run function {ns}:v{version}/zombies/revive/respawn_from_body
""")

	## Run as the player, at the spot where they went down.
	write_versioned_function("zombies/revive/respawn_from_body", f"""
execute store success score #respawn_done {ns}.data run tag @n[tag={ns}.spawn_point,tag={ns}.spawn_zb_player,tag={ns}.spawn_unlocked,distance=..{SPAWN_NEAR_BODY}] add {ns}.spawn_candidate
execute if score #respawn_done {ns}.data matches 1 as @n[tag={ns}.spawn_candidate] run function {ns}:v{version}/shared/tp_to_spawn {{mode:"zombies"}}
tag @e[tag={ns}.spawn_candidate] remove {ns}.spawn_candidate
execute if score #respawn_done {ns}.data matches 1 run return 1

execute store success score #respawn_done {ns}.data if entity @p[scores={{{ns}.zb.in_game=1,{ns}.zb.downed=0}},gamemode=!spectator,tag=!{ns}.spawn_pending]
execute if score #respawn_done {ns}.data matches 1 run tp @s @p[scores={{{ns}.zb.in_game=1,{ns}.zb.downed=0}},gamemode=!spectator,tag=!{ns}.spawn_pending]
""")

	## At the unlocked player spawn nearest a random alive teammate.
	write_versioned_function("zombies/revive/respawn_at_random_spawn", f"""
tag @s add {ns}.spawn_pending
# #has_candidate stays 0 without an alive teammate: the `as @r` body never runs, so `store success` never writes.
scoreboard players set #has_candidate {ns}.data 0
execute as @r[scores={{{ns}.zb.in_game=1,{ns}.zb.downed=0}},gamemode=!spectator,limit=1] at @s store success score #has_candidate {ns}.data run tag @n[tag={ns}.spawn_point,tag={ns}.spawn_zb_player,tag={ns}.spawn_unlocked] add {ns}.spawn_candidate
# No alive teammate: the spawn nearest @s.
execute if score #has_candidate {ns}.data matches 0 run tag @n[tag={ns}.spawn_point,tag={ns}.spawn_zb_player,tag={ns}.spawn_unlocked] add {ns}.spawn_candidate
execute as @n[tag={ns}.spawn_candidate] run function {ns}:v{version}/shared/tp_to_spawn {{mode:"zombies"}}
tag @e[tag={ns}.spawn_candidate] remove {ns}.spawn_candidate
tag @a[tag={ns}.spawn_pending] remove {ns}.spawn_pending
""")

