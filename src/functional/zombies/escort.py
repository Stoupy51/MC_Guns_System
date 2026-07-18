
# ruff: noqa: E501
# Zombies Escort System — wandering-trader pathfinding taxi for stuck zombies.
#
# Why the trader: zombie melee AI needs one full A* path to its target, bounded by the
# follow_range budget (region radius = follow_range+16, max nodes = follow_range*16, see
# PathNavigation.java). When the nearest player is far or the route is long/complex, the path
# fails and the zombie just strolls randomly ("stuck"). The wandering trader is the one vanilla
# mob with data-driven long-range navigation: its `wander_target` NBT (int array [X,Y,Z]) drives
# WanderToPositionGoal, which re-paths in 10-BLOCK SEGMENTS toward the target
# (WanderingTrader.java: while farther than 10, moveTo(pos + normalize(target-pos)*10)), so each
# path is tiny and always within budget — the trader can cross an arbitrarily large map.
#
# Mechanic: when the stuck detector fires, instead of the teleport rescue, summon an invisible,
# invulnerable, silent trader at the zombie, freeze the zombie (NoAI) and glue it onto the
# trader every tick while the trader walks toward the nearest player (wander_target refreshed
# every second). Once an alive player is within RELEASE_RADIUS blocks, the trader is removed and
# the zombie's own AI takes over (vanilla handles the short-range chase fine). Proximity alone
# is not enough: a player 3 blocks above through a floor is "close" but the zombie still can't
# path there, so release also requires line of sight (#bs.view:can_see_ata). If the trader
# can't make it either (stuck for {WATCHDOG_GIVE_UP}s or TTL expires), fall back to the old
# teleport rescue; the failure flag is cleared once the teleport lands so a future stuck
# timeout at the new position may try a trader again.
#
# Trader gotchas handled here (verified in minecraft_source_code):
# - WanderingTrader has AvoidEntityGoal(Zombie.class, 8 blocks) at priority 1, ABOVE
#   WanderToPositionGoal (priority 2), and zombies target AbstractVillager. Both run through
#   TargetingConditions.forCombat(), which fails when the entities are ALLIED — so all round
#   zombies and escort traders join the {ns}.horde team: the trader doesn't flee its own horde
#   and zombies don't eat the taxi.
# - WanderToPositionGoal.stop() nulls wander_target whenever the goal deactivates (reached
#   within 2 blocks, or preempted), hence the periodic re-set instead of set-once.
# - The goal walks at 0.35 * movement_speed (trader default 0.7 -> 0.245 effective); the trader's
#   base speed is set to zombie_speed / 0.35 at escort start so the taxi keeps round pacing.
# - DespawnDelay:0 = never despawns; Offers:{Recipes:[]} = right-click is a no-op; pre-applied
#   infinite invisibility also disables the trader's "drink invisibility potion at night" goal.
# - The zombie is glued EXACTLY onto the trader (same pos + rotation): the horde team has
#   collisionRule pushOtherTeams, so the overlapping zombie never pushes the trader off its path,
#   and the zombie always sits on a path-valid position (no wall/floor clipping when released).
# - Trader removal tp's it 1000 blocks straight down before the kill: the death poof particles
#   and the corpse happen where nobody can see them.
# - gamerule spawn_wandering_traders is turned off during games so no natural trader (not on the
#   team) wanders in, flees the horde, and gets chewed on.
from stewbeet import Mem, write_load_file, write_tag, write_versioned_function

# Max simultaneous escorts; stuck zombies beyond this use the teleport rescue instead.
MAX_ESCORTS: int = 8
# Escort lifetime in ticks before giving up (45s; then teleport-rescue fallback). Hard cap only:
# a trader that is itself stuck is caught much earlier by the watchdog below.
ESCORT_TTL: int = 900
# Watchdog: seconds without leaving the current block before the escort gives up early
# (the trader can't path either -> straight to the teleport-rescue fallback).
WATCHDOG_GIVE_UP: int = 5
# Escort trader follow_range: the pathfinding budget scales LIVE with this attribute (Mob.java
# onAttributeUpdated): max A* nodes = value*16, search region radius = value+8. The default 16
# (256 nodes, 24 blocks) can't afford stair detours, so a trader whose target is on another
# floor just hugs the closest point below/above it. 96 = 1536 nodes / 104 blocks — the direct
# path used within 10 blocks of wander_target can then actually route through staircases.
PATHFINDING_RANGE: int = 96
# Hand back to vanilla zombie AI once an alive player is within this radius AND visible.
RELEASE_RADIUS: int = 10
# PaP-room lure (Kino-style QoL): when EVERY alive player is inside the PaP room (within
# PAP_ROOM_RADIUS of a PaP machine), escorts aim at the map-defined lure centre instead of a
# player, so the horde spreads to the middle of the map rather than piling at the PaP door. The
# centre is OPTIONAL and map-defined via the #<ns>:zombies/setup_lure function tag (see below):
# a map that registers nothing places no marker and the whole system stays inert. A lured zombie
# is released once it reaches within LURE_RELEASE of the centre marker.
PAP_ROOM_RADIUS: int = 14
LURE_RELEASE: int = 8
# Within this radius, release unconditionally (no line-of-sight needed): vanilla AI handles this
# range even around corners, and the visibility check aims at the player's FEET — slabs, stairs
# or a corner can fail it forever, leaving the taxi orbiting a player it already reached.
RELEASE_RADIUS_CLOSE: int = 6


def generate_zombies_escort() -> None:
	ns: str = Mem.ctx.project_id
	version: str = Mem.ctx.project_version

	# Nearest escort trader from the current execution position. Escorted zombies are glued to
	# their trader every tick, so "my" trader is always the nearest one within a couple blocks;
	# 8 blocks of slack covers lag spikes. If two escorts cross paths and momentarily swap
	# traders, both zombies still get dragged toward the nearest player — harmless.
	my_trader: str = f"@n[type=minecraft:wandering_trader,tag={ns}.zb_escort,distance=..8]"
	nearest_alive: str = f"@p[scores={{{ns}.zb.in_game=1,{ns}.zb.downed=0}},gamemode=!spectator]"

	write_load_file(f"""
# Escort TTL per escorted zombie (ticks left before the teleport-rescue fallback)
scoreboard objectives add {ns}.zb.escort_ttl dummy

# Live escort counter (gates the per-tick escorted-zombie scan)
scoreboard players add #zb_escort_count {ns}.data 0

# Horde alliance team: round zombies and escort traders are allied, so the trader's
# AvoidEntityGoal(Zombie) never fires (it flees at SPRINT speed otherwise!) and zombies never
# attack the taxi. Created at load, not game start, so a mid-game /reload can't leave it missing.
# pushOtherTeams = no pushing WITHIN the horde (the zombie overlaps its trader without shoving
# it off its path) while members still push players and everything else.
team add {ns}.horde
team modify {ns}.horde collisionRule pushOtherTeams
""")

	## Route stuck zombies to an escort BEFORE the teleport-rescue body in on_stuck_zombie
	## (game.py). Saturated escorts or a previously failed escort fall through to the teleport.
	write_versioned_function("zombies/on_stuck_zombie", f"""
# Prefer a wandering-trader escort over the teleport rescue below (see escort.py)
execute unless entity @s[tag={ns}.zb_escort_failed] if score #zb_escort_count {ns}.data matches ..{MAX_ESCORTS - 1} run return run function {ns}:v{version}/zombies/escort/start
""", prepend=True)

	## Start an escort. @s = stuck zombie, at @s.
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

# Trader base speed = zombie_speed / 0.35 (WanderToPositionGoal modifier) => same effective speed
execute store result storage {ns}:temp _escort.speed double 0.0028571 run attribute @s minecraft:movement_speed get 1000
execute as @n[tag={ns}.zb_escort_new] run function {ns}:v{version}/zombies/escort/set_trader_speed with storage {ns}:temp _escort

# Big pathfinding budget so it can afford stair detours instead of camping below the player
# (see PATHFINDING_RANGE in escort.py; the command triggers the live budget recompute)
execute as @n[tag={ns}.zb_escort_new] run attribute @s minecraft:follow_range base set {PATHFINDING_RANGE}

# Aim it at the nearest alive player immediately
execute as @n[tag={ns}.zb_escort_new] at @s run function {ns}:v{version}/zombies/escort/retarget

tag @n[tag={ns}.zb_escort_new] remove {ns}.zb_escort_new
scoreboard players add #zb_escort_count {ns}.data 1
""")

	write_versioned_function("zombies/escort/set_trader_speed", """
$attribute @s minecraft:movement_speed base set $(speed)
""")

	## Refresh wander_target to the nearest alive player's block position. @s = trader, at @s.
	## WanderToPositionGoal clears the target whenever it deactivates, so this is re-applied
	## every second rather than set once. If nobody is targetable (everyone downed), the data
	## gets fail and the trader keeps its previous heading until the TTL fallback.
	write_versioned_function("zombies/escort/retarget", f"""
# PaP-room lure active: aim at the theatre centre marker instead of a player (see escort.py)
execute if score #zb_lure {ns}.data matches 1 if entity @e[tag={ns}.lure_center] run return run function {ns}:v{version}/zombies/escort/retarget_lure
execute store result storage {ns}:temp _escort.x int 1 run data get entity {nearest_alive} Pos[0]
execute store result storage {ns}:temp _escort.y int 1 run data get entity {nearest_alive} Pos[1]
execute store result storage {ns}:temp _escort.z int 1 run data get entity {nearest_alive} Pos[2]
function {ns}:v{version}/zombies/escort/set_wander_target with storage {ns}:temp _escort
""")

	## Aim the trader at the theatre centre marker (PaP-room lure). @s = trader, at @s.
	write_versioned_function("zombies/escort/retarget_lure", f"""
execute store result storage {ns}:temp _escort.x int 1 run data get entity @n[tag={ns}.lure_center] Pos[0]
execute store result storage {ns}:temp _escort.y int 1 run data get entity @n[tag={ns}.lure_center] Pos[1]
execute store result storage {ns}:temp _escort.z int 1 run data get entity @n[tag={ns}.lure_center] Pos[2]
function {ns}:v{version}/zombies/escort/set_wander_target with storage {ns}:temp _escort
""")

	write_versioned_function("zombies/escort/set_wander_target", """
$data modify entity @s wander_target set value [I;$(x),$(y),$(z)]
""")

	## Per-tick escort logic. @s = escorted zombie, at @s (position from BEFORE this tick's glue,
	## i.e. the trader's last-tick position — close enough for all distance checks here).
	write_versioned_function("zombies/escort/zombie_tick", f"""
# Trader gone (killed externally)? Unfreeze; normal stuck detection takes over again
execute unless entity {my_trader} run return run function {ns}:v{version}/zombies/escort/detach

# Glue the zombie exactly onto the trader (same position AND rotation): always a path-valid
# spot, and the horde's pushOtherTeams collision rule keeps the overlap from pushing the trader
execute at {my_trader} run tp @s ~ ~ ~ ~ ~

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

# TTL countdown; the trader could not reach anyone in time -> teleport-rescue fallback
scoreboard players remove @s {ns}.zb.escort_ttl 1
execute if score @s {ns}.zb.escort_ttl matches ..0 run return run function {ns}:v{version}/zombies/escort/give_up

# Re-aim the trader at the nearest alive player every second
scoreboard players operation #zb_esc_mod {ns}.data = @s {ns}.zb.escort_ttl
scoreboard players operation #zb_esc_mod {ns}.data %= #20 {ns}.data
execute if score #zb_esc_mod {ns}.data matches 0 as {my_trader} at @s run function {ns}:v{version}/zombies/escort/retarget

# Watchdog every second: a trader that can't move is caught in {WATCHDOG_GIVE_UP}s, not {ESCORT_TTL // 20}s
execute if score #zb_esc_mod {ns}.data matches 0 run function {ns}:v{version}/zombies/escort/watchdog
""")

	## Early give-up for a trader that is itself stuck. @s = escorted zombie (glued to the
	## trader, so its block position tracks the trader's). While escorted, zb.stuck_x/z hold the
	## block snapshot from one second ago and zb.stuck_ticks counts consecutive still seconds.
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

	## End the escort and restore the zombie's own AI. @s = escorted zombie.
	## Does NOT remove the trader — callers that still have one handle it themselves.
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

	## Successful delivery: a player is within {RELEASE_RADIUS} blocks and visible. @s = zombie.
	write_versioned_function("zombies/escort/release", f"""
execute as {my_trader} run function {ns}:v{version}/zombies/escort/discard_trader
function {ns}:v{version}/zombies/escort/detach
""")

	## Remove a trader with zero visible feedback: the death poof particles and 1-tick corpse
	## happen 1000 blocks underground. @s = trader.
	write_versioned_function("zombies/escort/discard_trader", """
tp @s ~ ~-1000 ~
kill @s
""")

	## The trader could not path either (watchdog still for {WATCHDOG_GIVE_UP}s, or TTL expired).
	## @s = zombie, at @s. Flagging zb_escort_failed makes on_stuck_zombie skip straight to the
	## teleport body; the teleport clears the flag again once it lands (game.py), so it only
	## routes THIS call — escorts may retry from the new position later.
	write_versioned_function("zombies/escort/give_up", f"""
tag @s add {ns}.zb_escort_failed
execute as {my_trader} run function {ns}:v{version}/zombies/escort/discard_trader
function {ns}:v{version}/zombies/escort/detach
function {ns}:v{version}/zombies/on_stuck_zombie
""")

	## Escorted zombie killed mid-transit: discard its taxi THIS tick instead of leaving an
	## orphaned trader wandering around for up to 2s until the game_tick sweep catches it.
	## Runs inside on_zombie_dying (round.py) before the zombie is tp'd away, so the dying
	## zombie is still glued to its trader and the nearest-trader selector resolves.
	write_versioned_function("zombies/on_zombie_dying", f"""
# Escorted zombie died: remove its escort trader immediately (escort.py)
execute if entity @s[tag={ns}.zb_escorted] at @s run function {ns}:v{version}/zombies/escort/on_escorted_killed
""", prepend=True)

	## @s = dying escorted zombie, at @s. No detach: the zombie is being removed anyway, just
	## drop it from the escort bookkeeping and delete the trader.
	write_versioned_function("zombies/escort/on_escorted_killed", f"""
tag @s remove {ns}.zb_escorted
scoreboard players remove #zb_escort_count {ns}.data 1
execute as {my_trader} run function {ns}:v{version}/zombies/escort/discard_trader
""")

	## Trader too close to a player: the escort trader is invisible but still RIGHT-CLICKABLE, and a
	## trader with empty offers returns InteractionResult.CONSUME — eating the player's click (so
	## ADS/fire silently fails) while it stands in their face. WanderingTrader force-clamps itself to
	## adult on every NBT load (readAdditionalSaveData: setAge(max(0, age))), so the usual "make it a
	## baby to disable mobInteract" trick is impossible; the only reliable defense is to never let a
	## trader be within reach. @s = trader, at @s. Player interaction reach is ~3 blocks, so a
	## {RELEASE_RADIUS_CLOSE}-block guard leaves margin even with the trader's <1 block/tick movement.
	write_versioned_function("zombies/escort/discard_near_player", f"""
function {ns}:v{version}/zombies/escort/end_at_trader
""")

	## End an escort from the TRADER's context (@s = trader, at @s): unfreeze the glued zombie so
	## vanilla AI takes over, then remove the trader. Shared by the interaction safeguard and the
	## barrier hand-off (barriers.py) so both end an escort the same way.
	write_versioned_function("zombies/escort/end_at_trader", f"""
execute as @e[tag={ns}.zb_escorted,distance=..8,limit=1,sort=nearest] run function {ns}:v{version}/zombies/escort/detach
function {ns}:v{version}/zombies/escort/discard_trader
""")

	## Hook the escort loop into the zombies game tick (count-gated: zero cost with no escort)
	write_versioned_function("zombies/game_tick", f"""
# Escort system (escort.py): drag escorted zombies behind their pathfinding traders
execute if score #zb_escort_count {ns}.data matches 1.. as @e[tag={ns}.zb_escorted] at @s run function {ns}:v{version}/zombies/escort/zombie_tick

# Interaction safeguard (count-INDEPENDENT, every tick): if the escort counter ever drifts, the
# gated loop above stops running and a trader can walk into a player and become right-clickable.
# This ungated pass over the (usually empty) trader set discards any trader that gets within reach
# of an alive player regardless of the counter, so an interactable trader can never linger.
execute as @e[type=minecraft:wandering_trader,tag={ns}.zb_escort] at @s if entity @p[scores={{{ns}.zb.in_game=1,{ns}.zb.downed=0}},gamemode=!spectator,distance=..{RELEASE_RADIUS_CLOSE}] run function {ns}:v{version}/zombies/escort/discard_near_player

# Every 2s: resync the escort counter from reality — start/detach keep it accurate in between,
# but any drift (e.g. an escorted zombie dying the same tick its trader vanishes) would wedge
# the max-escort gate shut forever, silently disabling all future escorts. Then discard
# orphaned traders whose escorted zombie died mid-transit (shot, nuked...) — the resync above
# already dropped those escorts from the count.
scoreboard players operation #zb_esc_sweep {ns}.data = #total_tick {ns}.data
scoreboard players operation #zb_esc_sweep {ns}.data %= #40 {ns}.data
execute if score #zb_esc_sweep {ns}.data matches 0 store result score #zb_escort_count {ns}.data if entity @e[tag={ns}.zb_escorted]
execute if score #zb_esc_sweep {ns}.data matches 0 as @e[type=minecraft:wandering_trader,tag={ns}.zb_escort] at @s unless entity @e[tag={ns}.zb_escorted,distance=..8] run function {ns}:v{version}/zombies/escort/discard_trader

# PaP-room lure: recompute lure state every 2s (inert unless the map defined a lure centre)
execute if score #zb_esc_sweep {ns}.data matches 20 if score #zb_pap_has {ns}.data matches 1 run function {ns}:v{version}/zombies/escort/update_lure
""")

	## ── PaP-room lure ──────────────────────────────────────────────────────────────────────────
	## The lure centre (the point the horde gathers at while everyone hides in the PaP room) is
	## defined by the MAP, not derived: a map opts in by registering a function into the
	## #{ns}:zombies/setup_lure tag that summons a {ns}.lure_center marker. That tag is run once
	## positioned at the map base (so registered functions can use relative coords like ~-49 ~-3 ~0).
	## Entirely OPTIONAL — a map that registers nothing leaves no marker and the lure stays off.
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

	## Recomputed each second: lure is on only when at least one player is alive and EVERY alive
	## player is inside the PaP room. While on, proactively escort a couple of stray zombies (far
	## from the centre, not already escorted) toward it — bounded by the normal escort cap.
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

	## Place the map's lure center at preload (base coords are loaded by then) — see escort.py.
	write_versioned_function("zombies/preload_complete", f"""
# PaP-room lure setup (escort.py)
function {ns}:v{version}/zombies/escort/setup_lure_center
""")

	## Game start: no natural traders wandering into the map (they'd flee the horde, being
	## teamless). The horde team itself is created in the load file above.
	write_versioned_function("zombies/start", f"""
# Escort system (escort.py)
scoreboard players set #zb_escort_count {ns}.data 0
scoreboard players set #zb_lure {ns}.data 0
gamerule spawn_wandering_traders false
""")

	## Game stop: traders themselves are killed with {ns}.gm_entity in game.py's stop
	write_versioned_function("zombies/stop", f"""
# Escort cleanup (escort.py); the traders themselves die with the {ns}.gm_entity kill above
scoreboard players set #zb_escort_count {ns}.data 0
gamerule spawn_wandering_traders true
""")

