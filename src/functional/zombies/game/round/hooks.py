""" Game tick hooks and the bulk-kill cleanup. """
# ruff: noqa: E501
# Imports
from stewbeet import Mem, write_versioned_function


# Functions
def write_round_hooks() -> None:
	ns: str = Mem.ctx.project_id
	version: str = Mem.ctx.project_version

	## Hook death watch + horde ambience into the main zombies game tick
	write_versioned_function("zombies/game_tick", f"""
# Intercept dying zombies before vanilla death particles are emitted.
function {ns}:v{version}/zombies/death_watch_tick

# Freeze watchdog: auto-recover a round that has stopped advancing (see watchdog_tick).
function {ns}:v{version}/zombies/watchdog_tick

# Dog spawn portals: 1.5s of sparks, then the bolt. Gated on the round kind, NOT on
# #zb_dog_pending — a portal orphaned by a desynced counter would then never tick, never strike and
# never die, which is the freeze the resync in game_tick pairs with this to rule out.
execute if score #zb_dog_round {ns}.data matches 1 as @e[tag={ns}.dog_portal] at @s run function {ns}:v{version}/zombies/dog_portal_tick

# Safety net: a dog that missed its scaling call is a vanilla 8-HP wolf, which reads as a bug
# (one-punch kills) rather than as a difficulty setting. types/dog is idempotent and tags what it
# scales, so this costs one tag-filtered scan and normally matches nothing.
execute if score #zb_dog_round {ns}.data matches 1 as @e[tag={ns}.zb_dog,tag=!{ns}.zb_scaled] run function {ns}:v{version}/zombies/types/dog

# Wolves are neutral mobs and hunt nothing without an anger target. Writing `angry_at` alone is
# enough (the game calls setTarget() from it on reload, then sustains the timer); writing AngerTime
# does nothing, as the always-saved `anger_end_time` outranks it. The `unless data` guard means a
# dog already locked on costs a read and no write. #zb_tick_mod is total_tick % 20 from earlier.
execute if score #zb_dog_round {ns}.data matches 1 if score #zb_tick_mod {ns}.data matches 0 as @e[tag={ns}.zb_dog,tag=!{ns}.zb_rising] at @s unless data entity @s angry_at run data modify entity @s angry_at set from entity @p[scores={{{ns}.zb.in_game=1}},gamemode=!spectator,gamemode=!creative] UUID

# Managed horde ambience: each player runs their own cooldown, refreshed by horde_ambient from the
# zombie count near THEM, so a player being chased hears a near-continuous horde while someone alone
# in a cleared room hears the occasional distant groan. horde_ambient also owns the sprint-scream
# channel, so this is the only tick entry point for the whole ambient side of enemies/vocals.py.
# Skipped on dog rounds: dogs aren't summoned Silent, so their own growls are the ambience.
scoreboard players remove @a[scores={{{ns}.zb.in_game=1,{ns}.zb.horde_cd=1..}}] {ns}.zb.horde_cd 1
execute if score #zb_dog_round {ns}.data matches 0 as @a[scores={{{ns}.zb.in_game=1,{ns}.zb.horde_cd=..0}},gamemode=!spectator] at @s run function {ns}:v{version}/zombies/horde_ambient
""")

	## Cleanup for round/end bulk-kill paths
	write_versioned_function("zombies/stop", f"""
kill @e[type=minecraft:marker,tag={ns}.death_watch]

# Portals are gm_entity so the bulk cleanup already removes them; the counter they feed has to be
# zeroed by hand or a stale value would block the next game's round completion forever.
kill @e[type=minecraft:marker,tag={ns}.dog_portal]
scoreboard players set #zb_dog_pending {ns}.data 0
""")

