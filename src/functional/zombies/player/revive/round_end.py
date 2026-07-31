""" Round-end free pickups, tearing a body down and respawning near the team. """
# ruff: noqa: E501
# Imports
from stewbeet import Mem, write_versioned_function

from ....helpers import MGS_TAG
from ....helpers.text import Text
from .shared import ROUND_END_PICKUP_RANGE


# Functions
def write_round_end_revives() -> None:
	ns: str = Mem.ctx.project_id
	version: str = Mem.ctx.project_version

	# Round end respawn: revive all spectating (bled-out) players
	write_versioned_function("zombies/revive/round_respawn", f"""
# Free pickup first: a player still DOWNED when the round ended, with a live teammate standing within
# {ROUND_END_PICKUP_RANGE} blocks of their body, is revived instead of respawned — they keep their guns.
# Must run before the respawn pass below, which would otherwise wipe them back to the starting loadout.
execute as @a[tag={ns}.downed_spectator,scores={{{ns}.zb.in_game=1}}] run function {ns}:v{version}/zombies/revive/round_end_pickup

# Respawn every remaining spectator (bled out, or downed with nobody close enough)
execute as @a[scores={{{ns}.zb.in_game=1}},gamemode=spectator] run function {ns}:v{version}/zombies/revive/do_round_respawn
""")

	## Round-end free pickup for one still-downed player (@s = the downed spectator).
	## Reviving through revive_complete is what keeps the inventory: it only restores state and teleports, and never touches the hotbar (unlike do_round_respawn -> give_respawn_loadout).
	## Perks stay lost, exactly like any other revive.
	write_versioned_function("zombies/revive/round_end_pickup", f"""
# Is a live (non-downed) teammate standing within {ROUND_END_PICKUP_RANGE} blocks of MY body?
scoreboard players operation #my_downed_id {ns}.data = @s {ns}.zb.downed_id
scoreboard players set #rv_pickup {ns}.data 0
execute as @e[type=minecraft:mannequin,tag={ns}.downed_mannequin,predicate={ns}:v{version}/zombies/revive/downed_id_match] at @s if entity @a[scores={{{ns}.zb.in_game=1,{ns}.zb.downed=0}},gamemode=!spectator,distance=..{ROUND_END_PICKUP_RANGE}] run scoreboard players set #rv_pickup {ns}.data 1
execute if score #rv_pickup {ns}.data matches 0 run return 0

# Picked up by the end of the round: full revive, inventory untouched
function {ns}:v{version}/zombies/revive/revive_complete
""")

	write_versioned_function("zombies/revive/do_round_respawn", f"""
# If this player was still DOWNED (mannequin alive) when the round ended, fully tear that state
# down first — otherwise their mannequin/HUD/camera would be orphaned and they'd stay "downed".
execute if entity @s[tag={ns}.downed_spectator] run function {ns}:v{version}/zombies/revive/clear_downed_state

# Restore adventure mode
spectate @s
gamemode adventure @s

# Teleport to a player spawn near a random alive teammate
function {ns}:v{version}/zombies/revive/respawn_near_player

# Heal and reset stamina to full (the stamina system owns the hunger bar)
scoreboard players set @s {ns}.stam_seen 0
effect give @s minecraft:instant_health 1 255 true

# Restore max health (check for Juggernog perk)
execute if score @s {ns}.zb.perk.juggernog matches 1.. run attribute @s minecraft:max_health base set 40
execute unless score @s {ns}.zb.perk.juggernog matches 1.. run attribute @s minecraft:max_health base set 20

# Re-give starting weapon on respawn
function {ns}:v{version}/zombies/inventory/give_respawn_loadout

# Tombstone: if this player bled out with a Tombstone marker, activate it + start the 60s recovery timer
function {ns}:v{version}/zombies/perks/tombstone_on_respawn

# Call map respawn script (executed as the respawning player)
function {ns}:v{version}/shared/maps/call_script_at_base {{script:"respawn"}}

# Announce
tellraw @a[scores={{{ns}.zb.in_game=1}}] [{MGS_TAG},{Text.player(ns, "@s", side="zb", color="green")},{{"text":" has respawned!","color":"gray"}}]
""")

	## Fully tear down @s's downed mannequin/HUD/camera (matched by downed_id) and dismount.
	## Used when a still-downed player is force-revived at round end.
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

	## Teleport @s to the unlocked player spawn nearest to a random alive teammate (so respawned players rejoin near the action rather than at an arbitrary spawn).
	write_versioned_function("zombies/revive/respawn_near_player", f"""
tag @s add {ns}.spawn_pending
# #has_candidate stays 0 if there is no alive teammate (the `as @r` body never runs, so its
# `store success` never writes); the success flag then replaces a global @e existence scan.
scoreboard players set #has_candidate {ns}.data 0
execute as @r[scores={{{ns}.zb.in_game=1,{ns}.zb.downed=0}},gamemode=!spectator,limit=1] at @s store success score #has_candidate {ns}.data run tag @n[tag={ns}.spawn_point,tag={ns}.spawn_zb_player,tag={ns}.spawn_unlocked] add {ns}.spawn_candidate
# Fallback: if no alive teammate, use the unlocked player spawn nearest to @s
execute if score #has_candidate {ns}.data matches 0 run tag @n[tag={ns}.spawn_point,tag={ns}.spawn_zb_player,tag={ns}.spawn_unlocked] add {ns}.spawn_candidate
execute as @n[tag={ns}.spawn_candidate] run function {ns}:v{version}/shared/tp_to_spawn {{mode:"zombies"}}
tag @e[tag={ns}.spawn_candidate] remove {ns}.spawn_candidate
tag @a[tag={ns}.spawn_pending] remove {ns}.spawn_pending
""")

