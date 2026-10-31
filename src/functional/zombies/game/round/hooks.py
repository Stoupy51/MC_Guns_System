""" Game tick hooks and the bulk-kill cleanup. """
# Imports
from stewbeet import Mem, write_tag, write_versioned_function


# Functions
def write_round_hooks() -> None:
	ns: str = Mem.ctx.project_id
	version: str = Mem.ctx.project_version

	write_versioned_function("zombies/game_tick", f"""
# Before vanilla death particles.
function {ns}:v{version}/zombies/death_watch_tick

execute if score #zb_next_round {ns}.data matches 1.. run scoreboard players remove #zb_next_round {ns}.data 1
execute if score #zb_next_round {ns}.data matches 0 if score #zb_to_spawn {ns}.data matches ..-1 run function {ns}:v{version}/zombies/start_round

# Recovers a round that stopped advancing (see watchdog_tick).
function {ns}:v{version}/zombies/watchdog_tick

# Once a second, at most one aura zombie (types/aura is unique).
execute if score #zb_tick_mod {ns}.data matches 0 as @e[type=minecraft:zombie,tag={ns}.zb_aura,limit=1] at @s run function {ns}:v{version}/zombies/aura_tick

# Not gated on #zb_portal_pending: a portal orphaned by a desynced counter would never tick, strike or die.
execute as @e[type=minecraft:marker,tag={ns}.zb_portal] at @s run function {ns}:v{version}/zombies/portal_tick

# Wolves, bees, golems and other neutral mobs hunt nothing without an anger target. `angry_at` alone is enough (setTarget
# runs from it on reload); AngerTime does nothing, the saved anger_end_time outranks it. #zb_tick_mod is total_tick % 20.
execute if score #zb_tick_mod {ns}.data matches 0 as @e[type=#{ns}:v{version}/zombies/neutral,tag={ns}.zombie_round,tag=!{ns}.zb_rising] at @s unless data entity @s angry_at run data modify entity @s angry_at set from entity @p[scores={{{ns}.zb.in_game=1}},gamemode=!spectator,gamemode=!creative] UUID

# Each player's cooldown is refreshed by horde_ambient from the zombie count near them; it also owns the sprint channel.
scoreboard players remove @a[scores={{{ns}.zb.in_game=1,{ns}.zb.horde_cd=1..}}] {ns}.zb.horde_cd 1
execute as @a[scores={{{ns}.zb.in_game=1,{ns}.zb.horde_cd=..0}},gamemode=!spectator] at @s run function {ns}:v{version}/zombies/horde_ambient
""")

	# The mobs that only attack once angered; every other one picks its target on its own.
	write_tag(f"{ns}:v{version}/zombies/neutral", Mem.ctx.data.entity_type_tags, [
		"minecraft:wolf", "minecraft:bee", "minecraft:iron_golem", "minecraft:polar_bear", "minecraft:enderman", "minecraft:zombified_piglin",
	])

	write_versioned_function("zombies/stop", f"""
kill @e[type=minecraft:marker,tag={ns}.death_watch]

# zombies_entity cleanup removes the portals, but the counter must be zeroed or the next game's round would never complete.
kill @e[type=minecraft:marker,tag={ns}.zb_portal]
scoreboard players set #zb_portal_pending {ns}.data 0
""")

