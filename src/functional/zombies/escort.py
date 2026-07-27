""" Wandering-trader pathfinding taxi for stuck zombies.

Zombie A* fails over long or complex routes (PathNavigation.java) and the zombie strolls randomly.
A trader's `wander_target` NBT drives WanderToPositionGoal, which re-paths in 10-block segments, so
it crosses any map. An escort is an invisible trader summoned at the zombie, with the zombie frozen
(NoAI) and glued to it until a player is close and visible.

Trader gotchas (verified in minecraft_source_code):
- AvoidEntityGoal(Zombie, 8) outranks WanderToPositionGoal and zombies target AbstractVillager;
  both fail for ALLIED entities, hence the shared horde team.
- WanderToPositionGoal.stop() nulls wander_target, so it is re-applied every second.
- The goal walks at 0.35 * movement_speed; trader base speed is zombie_speed / 0.35.
- DespawnDelay:0 never despawns, Offers:{Recipes:[]} makes right-click a no-op, and traders tp
  1000 blocks down before the kill so the death poof is invisible.
"""
# ruff: noqa: E501
from stewbeet import Mem, write_load_file, write_tag, write_versioned_function

MAX_ESCORTS: int = 16
""" Max simultaneous escorts; stuck zombies beyond this use the teleport rescue instead. """

ESCORT_TTL: int = 900
""" Escort lifetime in ticks before the teleport-rescue fallback. Hard cap only: a trader that is
itself stuck is caught much earlier by the watchdog. """

WATCHDOG_GIVE_UP: int = 5
""" Seconds without leaving the current block before the escort gives up early. """

PATHFINDING_RANGE: int = 96
""" Escort trader follow_range. The budget scales live with this attribute (Mob.java
onAttributeUpdated): max A* nodes = value*16, region radius = value+8. The default 16 cannot afford
stair detours, so a trader whose target is on another floor hugs the closest point below it. """

RELEASE_RADIUS: int = 10
""" Hand back to vanilla zombie AI once an alive player is within this radius AND visible. """

PAP_ROOM_RADIUS: int = 14
LURE_RELEASE: int = 8
""" PaP-room lure: when every alive player is within PAP_ROOM_RADIUS of a PaP machine, escorts aim
at the map-defined lure centre instead of a player, spreading the horde to the middle of the map.
The centre is opt-in via the #<ns>:zombies/setup_lure tag; a map that registers nothing stays
inert. A lured zombie is released within LURE_RELEASE of the centre marker. """

RELEASE_RADIUS_CLOSE: int = 6
""" Release unconditionally within this radius: vanilla AI handles it even around corners, and the
visibility check aims at the player's FEET, which slabs or stairs can fail forever. """

TRADER_REACH_GUARD: int = 6
""" Radius of the "a trader must never be right-clickable" safeguard. Do NOT lower: reach is the
minecraft:entity_interaction_range attribute, which zombies raises to 5 (game.py), so the vanilla 3
does not apply. Monkey-bomb traders are exempt; their eaten click is recovered by the
right_click_entity advancement (weapon/common.py). """

MONKEY_RELEASE: int = 4
""" A monkey-escorted zombie stops riding and HOLDS within this many blocks of the thrown monkey,
so zombies spread along their approach paths instead of stacking — well inside the 7-block blast. """

def generate_zombies_escort() -> None:
	ns: str = Mem.ctx.project_id
	version: str = Mem.ctx.project_version

	# Escorted zombies are glued to their trader every tick, so "mine" is always the nearest one
	my_trader: str = f"@n[type=minecraft:wandering_trader,tag={ns}.zb_escort,distance=..8]"
	my_trader_monkey: str = f"@n[type=minecraft:wandering_trader,tag={ns}.zb_escort,tag={ns}.zb_escort_monkey,distance=..8]"
	nearest_alive: str = f"@p[scores={{{ns}.zb.in_game=1,{ns}.zb.downed=0}},gamemode=!spectator]"

	write_load_file(f"""
# Escort TTL per escorted zombie (ticks left before the teleport-rescue fallback)
scoreboard objectives add {ns}.zb.escort_ttl dummy

# Live escort counter (gates the per-tick escorted-zombie scan)
scoreboard players add #zb_escort_count {ns}.data 0

# One-shot target mode for the NEXT escort/start, consumed (reset to 0) inside start:
# 0 = aim at the nearest player (stuck rescue / PaP lure), 1 = aim at a thrown monkey bomb.
scoreboard players add #zb_escort_mode {ns}.data 0

# Horde alliance team: round zombies and escort traders are allied, so the trader's
# AvoidEntityGoal(Zombie) never fires (it flees at SPRINT speed otherwise!) and zombies never
# attack the taxi. Created at load, not game start, so a mid-game /reload can't leave it missing.
# pushOtherTeams = no pushing WITHIN the horde (the zombie overlaps its trader without shoving
# it off its path) while members still push players and everything else.
team add {ns}.horde
team modify {ns}.horde collisionRule pushOtherTeams
""")

	# Route stuck zombies to an escort before the teleport-rescue body in on_stuck_zombie (game.py)
	write_versioned_function("zombies/on_stuck_zombie", f"""
# Prefer a wandering-trader escort over the teleport rescue below (see escort.py).
# Dogs are excluded: the escort freezes its passenger with `data modify entity @s NoAI`, and every
# NBT write on a wolf runs readAdditionalSaveData -> setTame(false,true) -> MAX_HEALTH base reset
# to 8 (TamableAnimal/Wolf). A dog dragged by a taxi arrives at 8 HP, dying to anything it touches.
# They also don't need one — they outrun the trader, so the direct teleport below is strictly better.
execute unless entity @s[tag={ns}.zb_dog] unless entity @s[tag={ns}.zb_escort_failed] if score #zb_escort_count {ns}.data matches ..{MAX_ESCORTS - 1} run return run function {ns}:v{version}/zombies/escort/start
""", prepend=True)

	# Start an escort (@s = stuck zombie, at @s)
	write_versioned_function("zombies/escort/start", f"""
# Freeze the zombie: the trader does the walking from here, the zombie is dragged behind it.
# The team join is normally redundant (round.py joins every zombie at summon) but covers
# zombies summoned before a mid-game /reload introduced the team.
tag @s add {ns}.zb_escorted
team join {ns}.horde @s
data modify entity @s NoAI set value 1b
scoreboard players set @s {ns}.zb.escort_ttl {ESCORT_TTL}

# Watchdog init: stuck_x/z/ticks are repurposed while escorted (block snapshot + still counter);
# detach re-initializes them for the normal stuck detection
execute store result score @s {ns}.zb.stuck_x run data get entity @s Pos[0]
execute store result score @s {ns}.zb.stuck_z run data get entity @s Pos[2]
scoreboard players set @s {ns}.zb.stuck_ticks 0

# Invisible pathfinding taxi (see escort.py header for every NBT choice)
summon minecraft:wandering_trader ~ ~ ~ {{Tags:["{ns}.zb_escort","{ns}.gm_entity","{ns}.zb_escort_new","global.ignore","global.ignore.kill"],Silent:1b,Invulnerable:1b,PersistenceRequired:1b,DespawnDelay:0,CanPickUpLoot:0b,DeathLootTable:"minecraft:empty",Offers:{{Recipes:[]}},active_effects:[{{id:"minecraft:invisibility",duration:-1,show_particles:0b}}]}}

# Allied with the horde so its AvoidEntityGoal(Zombie) never fires and zombies never target it
team join {ns}.horde @n[tag={ns}.zb_escort_new]

# Trader base speed = zombie_speed / 0.35 (WanderToPositionGoal modifier) => same effective speed.
# BASE get, not effective: a barrier-frozen zombie's {ns}:freeze modifier (-1024) would read negative
# and clamp the taxi to 0 speed; a just-detached zombie's Speed I would read 20% high.
execute store result storage {ns}:temp _escort.speed double 0.0028571 run attribute @s minecraft:movement_speed base get 1000
execute as @n[tag={ns}.zb_escort_new] run function {ns}:v{version}/zombies/escort/set_trader_speed with storage {ns}:temp _escort

# Big pathfinding budget so it can afford stair detours instead of camping below the player
# (see PATHFINDING_RANGE in escort.py; the command triggers the live budget recompute)
execute as @n[tag={ns}.zb_escort_new] run attribute @s minecraft:follow_range base set {PATHFINDING_RANGE}

# Monkey-bomb escorts (monkey_bomb.py) target the thrown monkey instead of a player: flag the
# trader so retarget routes to retarget_monkey. #zb_escort_mode is the caller's one-shot signal.
execute if score #zb_escort_mode {ns}.data matches 1 run tag @n[tag={ns}.zb_escort_new] add {ns}.zb_escort_monkey
scoreboard players set #zb_escort_mode {ns}.data 0

# Aim it at its target immediately (nearest player, PaP-room lure, or thrown monkey per the flag)
execute as @n[tag={ns}.zb_escort_new] at @s run function {ns}:v{version}/zombies/escort/retarget

tag @n[tag={ns}.zb_escort_new] remove {ns}.zb_escort_new
scoreboard players add #zb_escort_count {ns}.data 1
""")

	write_versioned_function("zombies/escort/set_trader_speed", """
$attribute @s minecraft:movement_speed base set $(speed)
""")

	# Refresh wander_target every second (the goal clears it whenever it deactivates)
	write_versioned_function("zombies/escort/retarget", f"""
# Monkey-bomb lure (monkey_bomb.py): aim at the nearest thrown monkey — takes priority over both
# the PaP lure and player targeting while the trader carries the {ns}.zb_escort_monkey flag.
execute if entity @s[tag={ns}.zb_escort_monkey] run return run function {ns}:v{version}/zombies/escort/retarget_monkey

# PaP-room lure active: aim at the theatre centre marker instead of a player (see escort.py)
execute if score #zb_lure {ns}.data matches 1 if entity @e[tag={ns}.lure_center] run return run function {ns}:v{version}/zombies/escort/retarget_lure
execute store result storage {ns}:temp _escort.x int 1 run data get entity {nearest_alive} Pos[0]
execute store result storage {ns}:temp _escort.y int 1 run data get entity {nearest_alive} Pos[1]
execute store result storage {ns}:temp _escort.z int 1 run data get entity {nearest_alive} Pos[2]
function {ns}:v{version}/zombies/escort/set_wander_target with storage {ns}:temp _escort
""")

	# Aim the trader at the theatre centre marker (@s = trader, at @s)
	write_versioned_function("zombies/escort/retarget_lure", f"""
execute store result storage {ns}:temp _escort.x int 1 run data get entity @n[tag={ns}.lure_center] Pos[0]
execute store result storage {ns}:temp _escort.y int 1 run data get entity @n[tag={ns}.lure_center] Pos[1]
execute store result storage {ns}:temp _escort.z int 1 run data get entity @n[tag={ns}.lure_center] Pos[2]
function {ns}:v{version}/zombies/escort/set_wander_target with storage {ns}:temp _escort
""")

	# Aim the trader at the nearest thrown monkey; a detonation mid-call just keeps the old heading
	write_versioned_function("zombies/escort/retarget_monkey", f"""
execute store result storage {ns}:temp _escort.x int 1 run data get entity @n[tag={ns}.monkey_bomb] Pos[0]
execute store result storage {ns}:temp _escort.y int 1 run data get entity @n[tag={ns}.monkey_bomb] Pos[1]
execute store result storage {ns}:temp _escort.z int 1 run data get entity @n[tag={ns}.monkey_bomb] Pos[2]
function {ns}:v{version}/zombies/escort/set_wander_target with storage {ns}:temp _escort
""")

	# Redirect a running escort to a monkey (@s = escorted zombie); idempotent, reverts on its own
	write_versioned_function("zombies/escort/redirect_to_monkey", f"""
tag {my_trader} add {ns}.zb_escort_monkey
""")

	write_versioned_function("zombies/escort/set_wander_target", """
$data modify entity @s wander_target set value [I;$(x),$(y),$(z)]
""")

	# Per-tick escort logic (@s = escorted zombie, at @s = the trader's last-tick position)
	write_versioned_function("zombies/escort/zombie_tick", f"""
# Trader gone (killed externally)? Unfreeze; normal stuck detection takes over again
execute unless entity {my_trader} run return run function {ns}:v{version}/zombies/escort/detach

# Glue the zombie exactly onto the trader (same position AND rotation): always a path-valid
# spot, and the horde's pushOtherTeams collision rule keeps the overlap from pushing the trader
execute at {my_trader} run tp @s ~ ~ ~ ~ ~

# Monkey-bomb lure (monkey_bomb.py): while the trader is flagged, this escort pulls the zombie to
# a thrown monkey. Drop the flag once every monkey is gone (revert to a normal player escort);
# otherwise ride toward the monkey and release on arrival, ignoring the player releases below.
execute if entity {my_trader_monkey} unless entity @e[tag={ns}.monkey_bomb] run tag {my_trader} remove {ns}.zb_escort_monkey
execute if entity {my_trader_monkey} run return run function {ns}:v{version}/zombies/escort/monkey_ride

# PaP-room lure active: release once the zombie reaches the theatre centre (no player will be
# nearby there to trigger the player-based releases below)
execute if score #zb_lure {ns}.data matches 1 if entity @e[tag={ns}.lure_center,distance=..{LURE_RELEASE}] run return run function {ns}:v{version}/zombies/escort/release

# Point-blank → release NOW, no line-of-sight needed: the visibility check below aims at the
# player's feet and corner/slab geometry can fail it forever while the taxi orbits the player
execute if entity @p[scores={{{ns}.zb.in_game=1,{ns}.zb.downed=0}},gamemode=!spectator,distance=..{RELEASE_RADIUS_CLOSE}] run return run function {ns}:v{version}/zombies/escort/release

# Hand off to vanilla AI once a player is close AND in the zombie's line of sight: a player
# 3 blocks above through a floor is "close" but the zombie still can't path there — keep riding
scoreboard players set #zb_esc_see {ns}.data 0
execute positioned as @p[scores={{{ns}.zb.in_game=1,{ns}.zb.downed=0}},gamemode=!spectator,distance=..{RELEASE_RADIUS}] store result score #zb_esc_see {ns}.data run function #bs.view:can_see_ata {{with:{{}}}}
execute if score #zb_esc_see {ns}.data matches 1 run return run function {ns}:v{version}/zombies/escort/release

# Ride tail: TTL fallback + periodic retarget/watchdog (shared with the monkey-bomb ride below)
function {ns}:v{version}/zombies/escort/escort_tail
""")

	# Shared "keep riding" tail: TTL countdown plus the once-a-second retarget and watchdog
	write_versioned_function("zombies/escort/escort_tail", f"""
# TTL countdown; the trader could not reach its target in time -> teleport-rescue fallback
scoreboard players remove @s {ns}.zb.escort_ttl 1
execute if score @s {ns}.zb.escort_ttl matches ..0 run return run function {ns}:v{version}/zombies/escort/give_up

# Re-aim the trader at its target every second (retarget picks player / PaP lure / monkey)
scoreboard players operation #zb_esc_mod {ns}.data = @s {ns}.zb.escort_ttl
scoreboard players operation #zb_esc_mod {ns}.data %= #20 {ns}.data
execute if score #zb_esc_mod {ns}.data matches 0 as {my_trader} at @s run function {ns}:v{version}/zombies/escort/retarget

# Watchdog every second: a trader that can't move is caught in {WATCHDOG_GIVE_UP}s, not {ESCORT_TTL // 20}s
execute if score #zb_esc_mod {ns}.data matches 0 run function {ns}:v{version}/zombies/escort/watchdog
""")

	# Monkey ride: HOLD on arrival rather than release, since the monkey has no aggro of its own
	write_versioned_function("zombies/escort/monkey_ride", f"""
execute if entity @e[tag={ns}.monkey_bomb,distance=..{MONKEY_RELEASE}] run return run function {ns}:v{version}/zombies/escort/monkey_hold
function {ns}:v{version}/zombies/escort/escort_tail
""")

	# Gathered at the monkey: no escort_tail, since standing still here is the goal, not a fault
	write_versioned_function("zombies/escort/monkey_hold", f"""
scoreboard players set @s {ns}.zb.escort_ttl {ESCORT_TTL}
scoreboard players set @s {ns}.zb.stuck_ticks 0
""")

	# Early give-up for a stuck trader; while escorted, stuck_x/z hold last second's block snapshot
	write_versioned_function("zombies/escort/watchdog", f"""
execute store result score #zb_esc_x {ns}.data run data get entity @s Pos[0]
execute store result score #zb_esc_z {ns}.data run data get entity @s Pos[2]
scoreboard players set #zb_esc_moved {ns}.data 0
execute unless score #zb_esc_x {ns}.data = @s {ns}.zb.stuck_x run scoreboard players set #zb_esc_moved {ns}.data 1
execute unless score #zb_esc_z {ns}.data = @s {ns}.zb.stuck_z run scoreboard players set #zb_esc_moved {ns}.data 1
scoreboard players operation @s {ns}.zb.stuck_x = #zb_esc_x {ns}.data
scoreboard players operation @s {ns}.zb.stuck_z = #zb_esc_z {ns}.data

# Moved a block since last second: reset the still counter and keep escorting
execute if score #zb_esc_moved {ns}.data matches 1 run return run scoreboard players set @s {ns}.zb.stuck_ticks 0

# Still in the same block: the trader is stuck too -> teleport-rescue fallback
scoreboard players add @s {ns}.zb.stuck_ticks 1
execute if score @s {ns}.zb.stuck_ticks matches {WATCHDOG_GIVE_UP}.. run function {ns}:v{version}/zombies/escort/give_up
""")

	# End the escort and restore the zombie's AI; the trader is the caller's problem
	write_versioned_function("zombies/escort/detach", f"""
tag @s remove {ns}.zb_escorted
data modify entity @s NoAI set value 0b
scoreboard players remove #zb_escort_count {ns}.data 1

# Kickstart vanilla AI. A zombie fresh off NoAI won't re-scan for a target for up to ~0.5s
# (NearestAttackableTargetGoal's mustSee re-scan interval) and looks braindead standing still.
# Turn it to face the nearest player and clear its NoActionTime so the goal selector re-evaluates
# immediately, then a brief speed nudge so it lunges the instant it acquires the target instead
# of pausing. (NoActionTime being high after the frozen transport is what stalls the first scan.)
data modify entity @s NoActionTime set value 0
execute at @s facing entity {nearest_alive} eyes run tp @s ~ ~ ~ ~ ~
effect give @s minecraft:speed 2 0 true

# Fresh stuck-tracking window from wherever the escort left the zombie
scoreboard players set @s {ns}.zb.stuck_dist 4
execute store result score @s {ns}.zb.stuck_x run data get entity @s Pos[0]
execute store result score @s {ns}.zb.stuck_z run data get entity @s Pos[2]
scoreboard players operation @s {ns}.zb.stuck_ticks = #total_tick {ns}.data
""")

	# Successful delivery: a player is within RELEASE_RADIUS and visible (@s = zombie)
	write_versioned_function("zombies/escort/release", f"""
execute as {my_trader} run function {ns}:v{version}/zombies/escort/discard_trader
function {ns}:v{version}/zombies/escort/detach
""")

	# Remove a trader with zero visible feedback (@s = trader)
	write_versioned_function("zombies/escort/discard_trader", """
tp @s ~ ~-1000 ~
kill @s
""")

	# The trader could not path either; the failure flag routes THIS call to the teleport rescue
	write_versioned_function("zombies/escort/give_up", f"""
# A MONKEY escort must never fall through to the teleport rescue
execute if entity {my_trader_monkey} run return run function {ns}:v{version}/zombies/escort/monkey_hold

tag @s add {ns}.zb_escort_failed
execute as {my_trader} run function {ns}:v{version}/zombies/escort/discard_trader
function {ns}:v{version}/zombies/escort/detach
function {ns}:v{version}/zombies/on_stuck_zombie
""")

	# Escorted zombie killed mid-transit: discard its taxi this tick, not on the 2s sweep
	write_versioned_function("zombies/on_zombie_dying", f"""
# Escorted zombie died: remove its escort trader immediately (escort.py)
execute if entity @s[tag={ns}.zb_escorted] at @s run function {ns}:v{version}/zombies/escort/on_escorted_killed
""", prepend=True)

	# No detach: the zombie is being removed anyway, so just drop the bookkeeping and the trader
	write_versioned_function("zombies/escort/on_escorted_killed", f"""
tag @s remove {ns}.zb_escorted
scoreboard players remove #zb_escort_count {ns}.data 1
execute as {my_trader} run function {ns}:v{version}/zombies/escort/discard_trader
""")

	# End an escort from the TRADER's context; shared by the reach safeguard and barriers.py
	write_versioned_function("zombies/escort/end_at_trader", f"""
execute as @e[tag={ns}.zb_escorted,distance=..8,limit=1,sort=nearest] run function {ns}:v{version}/zombies/escort/detach
function {ns}:v{version}/zombies/escort/discard_trader
""")

	# Hook the escort loop into the zombies game tick (count-gated: zero cost with no escort)
	write_versioned_function("zombies/game_tick", f"""
# Escort system (escort.py): drag escorted zombies behind their pathfinding traders
execute if score #zb_escort_count {ns}.data matches 1.. as @e[tag={ns}.zb_escorted] at @s run function {ns}:v{version}/zombies/escort/zombie_tick

# Interaction safeguard (count-INDEPENDENT, every tick)
execute as @e[type=minecraft:wandering_trader,tag={ns}.zb_escort,tag=!{ns}.zb_escort_monkey] at @s if entity @p[scores={{{ns}.zb.in_game=1,{ns}.zb.downed=0}},gamemode=!spectator,distance=..{TRADER_REACH_GUARD}] run function {ns}:v{version}/zombies/escort/end_at_trader

# Every 2s: resync the escort counter from reality
scoreboard players operation #zb_esc_sweep {ns}.data = #total_tick {ns}.data
scoreboard players operation #zb_esc_sweep {ns}.data %= #40 {ns}.data
execute if score #zb_esc_sweep {ns}.data matches 0 store result score #zb_escort_count {ns}.data if entity @e[tag={ns}.zb_escorted]
execute if score #zb_esc_sweep {ns}.data matches 0 as @e[type=minecraft:wandering_trader,tag={ns}.zb_escort] at @s unless entity @e[tag={ns}.zb_escorted,distance=..8] run function {ns}:v{version}/zombies/escort/discard_trader

# PaP-room lure: recompute lure state every 2s (inert unless the map defined a lure centre)
execute if score #zb_esc_sweep {ns}.data matches 20 if score #zb_pap_has {ns}.data matches 1 run function {ns}:v{version}/zombies/escort/update_lure
""")

	# PaP-room lure
	write_tag("zombies/setup_lure", Mem.ctx.data[ns].function_tags, [])
	write_versioned_function("zombies/escort/setup_lure_center", f"""
kill @e[tag={ns}.lure_center]

# Let the map place its lure centre marker, run positioned at the map base
execute store result storage {ns}:temp _base.x int 1 run scoreboard players get #gm_base_x {ns}.data
execute store result storage {ns}:temp _base.y int 1 run scoreboard players get #gm_base_y {ns}.data
execute store result storage {ns}:temp _base.z int 1 run scoreboard players get #gm_base_z {ns}.data
data modify storage {ns}:temp _base.fn set value "#{ns}:zombies/setup_lure"
function {ns}:v{version}/shared/call_at_base with storage {ns}:temp _base

# Enable the lure only if the map actually placed a centre marker (its opt-in)
scoreboard players set #zb_pap_has {ns}.data 0
execute if entity @e[tag={ns}.lure_center] run scoreboard players set #zb_pap_has {ns}.data 1
scoreboard players set #zb_lure {ns}.data 0
""")

	# Lure is on only when at least one player is alive and every alive player is in the PaP room
	write_versioned_function("zombies/escort/update_lure", f"""
execute store result score #zb_lure_alive {ns}.data if entity @a[scores={{{ns}.zb.in_game=1,{ns}.zb.downed=0}},gamemode=!spectator]
scoreboard players set #zb_lure_inpap {ns}.data 0
execute as @a[scores={{{ns}.zb.in_game=1,{ns}.zb.downed=0}},gamemode=!spectator] at @s if entity @e[type=minecraft:interaction,tag={ns}.pap_machine,distance=..{PAP_ROOM_RADIUS}] run scoreboard players add #zb_lure_inpap {ns}.data 1

scoreboard players set #zb_lure {ns}.data 0
execute if score #zb_lure_alive {ns}.data matches 1.. if score #zb_lure_inpap {ns}.data = #zb_lure_alive {ns}.data run scoreboard players set #zb_lure {ns}.data 1

# Start center-bound escorts on a few stray zombies while luring (cap-gated; the retarget in
# escort/start reads #zb_lure and aims at the centre marker)
execute if score #zb_lure {ns}.data matches 1 if score #zb_escort_count {ns}.data matches ..{MAX_ESCORTS - 1} as @e[tag={ns}.zombie_round,tag=!{ns}.zb_rising,tag=!{ns}.zb_escorted,tag=!{ns}.zb_escort_failed,limit=2,sort=random] at @s unless entity @e[tag={ns}.lure_center,distance=..16] run function {ns}:v{version}/zombies/escort/start
""")

	# Place the map's lure center at preload, once base coords are loaded
	write_versioned_function("zombies/preload_complete", f"""
# PaP-room lure setup (escort.py)
function {ns}:v{version}/zombies/escort/setup_lure_center
""")

	write_versioned_function("zombies/start", f"""
# Escort system (escort.py)
scoreboard players set #zb_escort_count {ns}.data 0
scoreboard players set #zb_escort_mode {ns}.data 0
scoreboard players set #zb_lure {ns}.data 0
gamerule spawn_wandering_traders false
gamerule spawn_mobs false
""")

	# Traders themselves are killed with the gm_entity sweep in game.py's stop
	write_versioned_function("zombies/stop", f"""
# Escort cleanup (escort.py); the traders themselves die with the {ns}.gm_entity kill above
scoreboard players set #zb_escort_count {ns}.data 0
""")

