""" Game tick hooks and the bulk-kill cleanup. """
# Imports
from stewbeet import Mem, write_versioned_function


# Functions
def write_round_hooks() -> None:
	ns: str = Mem.ctx.project_id
	version: str = Mem.ctx.project_version

	write_versioned_function("zombies/game_tick", f"""
# Before vanilla death particles.
function {ns}:v{version}/zombies/death_watch_tick

# Recovers a round that stopped advancing (see watchdog_tick).
function {ns}:v{version}/zombies/watchdog_tick

# Gated on the round kind, not #zb_dog_pending: a portal orphaned by a desynced counter would never tick, strike or die.
execute if score #zb_dog_round {ns}.data matches 1 as @e[type=minecraft:marker,tag={ns}.dog_portal] at @s run function {ns}:v{version}/zombies/dog_portal_tick

# A dog that missed its scaling is a vanilla 8 HP wolf. types/dog tags what it scales, so this normally matches nothing.
execute if score #zb_dog_round {ns}.data matches 1 as @e[type=minecraft:wolf,tag={ns}.zb_dog,tag=!{ns}.zb_scaled] run function {ns}:v{version}/zombies/types/dog

# Wolves hunt nothing without an anger target. `angry_at` alone is enough (setTarget runs from it on reload);
# AngerTime does nothing, the saved anger_end_time outranks it. #zb_tick_mod is total_tick % 20.
execute if score #zb_dog_round {ns}.data matches 1 if score #zb_tick_mod {ns}.data matches 0 as @e[type=minecraft:wolf,tag={ns}.zb_dog,tag=!{ns}.zb_rising] at @s unless data entity @s angry_at run data modify entity @s angry_at set from entity @p[scores={{{ns}.zb.in_game=1}},gamemode=!spectator,gamemode=!creative] UUID

# Each player's cooldown is refreshed by horde_ambient from the zombie count near them; it also owns the sprint channel.
# Skipped on dog rounds: dogs are not Silent, their growls are the ambience.
scoreboard players remove @a[scores={{{ns}.zb.in_game=1,{ns}.zb.horde_cd=1..}}] {ns}.zb.horde_cd 1
execute if score #zb_dog_round {ns}.data matches 0 as @a[scores={{{ns}.zb.in_game=1,{ns}.zb.horde_cd=..0}},gamemode=!spectator] at @s run function {ns}:v{version}/zombies/horde_ambient
""")

	write_versioned_function("zombies/stop", f"""
kill @e[type=minecraft:marker,tag={ns}.death_watch]

# gm_entity cleanup removes the portals, but the counter must be zeroed or the next game's round would never complete.
kill @e[type=minecraft:marker,tag={ns}.dog_portal]
scoreboard players set #zb_dog_pending {ns}.data 0
""")

