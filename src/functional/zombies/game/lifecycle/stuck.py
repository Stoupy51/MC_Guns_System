""" Rescuing unreachable zombies and keeping players inside the map bounds. """
# ruff: noqa: E501
# Imports
from stewbeet import Mem, write_versioned_function


# Functions
def write_stuck_and_bounds() -> None:
	ns: str = Mem.ctx.project_id
	version: str = Mem.ctx.project_version

	# Stuck Zombie Check.
	write_versioned_function("zombies/stuck_zombie_check", f"""
# @s = zombie_round entity (non-rising), run every 20 ticks on up to 24 random zombies
# Progress = distance bucket improved (or a player in melee range is VISIBLE). Resets the timer.
# Timeout depends on HOW the zombie is stuck:
# - hasn't moved at all: 400t (20s), only 100t (5s) once it has already been rescued
# - moved since last progress but not getting closer to a player: 300t (15s)

# Compute distance bucket to nearest alive player (4=very far, 0=adjacent)
scoreboard players set #cur_dist_bucket {ns}.data 4
execute if entity @a[scores={{{ns}.zb.in_game=1,{ns}.zb.downed=0}},gamemode=!spectator,distance=..96] run scoreboard players set #cur_dist_bucket {ns}.data 3
execute if entity @a[scores={{{ns}.zb.in_game=1,{ns}.zb.downed=0}},gamemode=!spectator,distance=..64] run scoreboard players set #cur_dist_bucket {ns}.data 2
execute if entity @a[scores={{{ns}.zb.in_game=1,{ns}.zb.downed=0}},gamemode=!spectator,distance=..32] run scoreboard players set #cur_dist_bucket {ns}.data 1
execute if entity @a[scores={{{ns}.zb.in_game=1,{ns}.zb.downed=0}},gamemode=!spectator,distance=..16] run scoreboard players set #cur_dist_bucket {ns}.data 0

# Compute current XZ position
execute store result score #cur_x {ns}.data run data get entity @s Pos[0]
execute store result score #cur_z {ns}.data run data get entity @s Pos[2]

# Detect any progress: bucket improved, OR bucket == 0 AND the nearby player is actually
# VISIBLE (real melee range). Proximity alone is not enough: a player a few blocks above or
# below through a floor kept the zombie permanently "not stuck" while it could never reach
# them — the LOS gate lets the timer run so the escort picks it up (see escort.py).
# XZ movement is NOT checked: a zombie attacking at close range stands still legitimately
scoreboard players set #stuck_progress {ns}.data 0
execute if score #cur_dist_bucket {ns}.data < @s {ns}.zb.stuck_dist run scoreboard players set #stuck_progress {ns}.data 1
scoreboard players set #zb_stuck_see {ns}.data 0
execute if score #cur_dist_bucket {ns}.data matches 0 positioned as @p[scores={{{ns}.zb.in_game=1,{ns}.zb.downed=0}},gamemode=!spectator,distance=..16] store result score #zb_stuck_see {ns}.data run function #bs.view:can_see_ata {{with:{{}}}}
execute if score #zb_stuck_see {ns}.data matches 1 run scoreboard players set #stuck_progress {ns}.data 1

# During a PaP-room lure, a zombie that has reached the theatre centre is exactly where we want it
# (all players are hiding in the PaP room). Count that as progress so the stuck-rescue doesn't drag
# it back to the PaP door (see escort.py lure mode).
execute if score #zb_lure {ns}.data matches 1 if entity @e[tag={ns}.lure_center,distance=..12] run scoreboard players set #stuck_progress {ns}.data 1

# If progress: update all stored values, reset timestamp, and clear the rescued flag
execute if score #stuck_progress {ns}.data matches 1 run scoreboard players operation @s {ns}.zb.stuck_dist = #cur_dist_bucket {ns}.data
execute if score #stuck_progress {ns}.data matches 1 run scoreboard players operation @s {ns}.zb.stuck_x = #cur_x {ns}.data
execute if score #stuck_progress {ns}.data matches 1 run scoreboard players operation @s {ns}.zb.stuck_z = #cur_z {ns}.data
execute if score #stuck_progress {ns}.data matches 1 run scoreboard players operation @s {ns}.zb.stuck_ticks = #total_tick {ns}.data
execute if score #stuck_progress {ns}.data matches 1 run tag @s remove {ns}.zb_rescued
execute if score #stuck_progress {ns}.data matches 1 run return 0

# No progress: pick the timeout for this stuck mode
# Moved = XZ differs from the snapshot taken at the last progress (block precision)
scoreboard players set #stuck_moved {ns}.data 0
execute unless score #cur_x {ns}.data = @s {ns}.zb.stuck_x run scoreboard players set #stuck_moved {ns}.data 1
execute unless score #cur_z {ns}.data = @s {ns}.zb.stuck_z run scoreboard players set #stuck_moved {ns}.data 1
scoreboard players set #stuck_threshold {ns}.data 400
execute if score #stuck_moved {ns}.data matches 1 run scoreboard players set #stuck_threshold {ns}.data 300
execute if score #stuck_moved {ns}.data matches 0 if entity @s[tag={ns}.zb_rescued] run scoreboard players set #stuck_threshold {ns}.data 100

# Down to the last couple of zombies: cut the stuck timeout to 5s so a single hard-to-reach zombie
# is escorted/teleported to the players quickly instead of dragging the round on (round 10+ complaint).
execute if score #zb_alive {ns}.data matches ..2 if score #stuck_threshold {ns}.data matches 101.. run scoreboard players set #stuck_threshold {ns}.data 100

# Compute elapsed ticks since last progress; respawn once the timeout is reached
scoreboard players operation #stuck_delta {ns}.data = #total_tick {ns}.data
scoreboard players operation #stuck_delta {ns}.data -= @s {ns}.zb.stuck_ticks
execute if score #stuck_delta {ns}.data >= #stuck_threshold {ns}.data run function {ns}:v{version}/zombies/on_stuck_zombie
""")

	write_versioned_function("zombies/on_stuck_zombie", f"""
# @s = stuck zombie — teleport it to a zombie spawn point near a player instead of killing it
# (keeps the horde intact and drops it back onto walkable navmesh so it can path again).

# Build the rescue pool via the shared spawn-proximity tagger (same 32 -> 64 -> any unlocked
# selection the round spawner uses). #zb_near_found is 0 iff nothing was tagged, so the teleport
# gate below needs no global @e existence scan. Dogs draw from their own markers: a zombie spawn can
# sit somewhere only a walker is meant to come from, and it may not even be inside the play bounds.
execute unless entity @s[tag={ns}.zb_dog] run function {ns}:v{version}/zombies/tag_spawns_near_players
execute if entity @s[tag={ns}.zb_dog] run function {ns}:v{version}/zombies/tag_special_spawns_near_players

# Never rescue to the spawn point this zombie last used (initial spawn or previous rescue),
# unless it is the only candidate left.
scoreboard players operation #zb_last_sid {ns}.data = @s {ns}.zb.spawn.sid
execute as @e[tag={ns}.zb_near] if score @s {ns}.zb.spawn.sid = #zb_last_sid {ns}.data run tag @s add {ns}.zb_near_prev
execute store result score #zb_near_alt {ns}.data if entity @e[tag={ns}.zb_near,tag=!{ns}.zb_near_prev]
execute if score #zb_near_alt {ns}.data matches 1.. run tag @e[tag={ns}.zb_near_prev] remove {ns}.zb_near
tag @e[tag={ns}.zb_near_prev] remove {ns}.zb_near_prev

# Teleport to the rescue spawn nearest the PLAYER, not the one nearest the stuck enemy. Picking
# from @s meant an enemy stranded far from everyone kept choosing the markers closest to itself,
# and the anti-reuse rule above then bounced it between the same two distant spawns indefinitely.
execute if score #zb_near_found {ns}.data matches 1.. at @p[scores={{{ns}.zb.in_game=1,{ns}.zb.downed=0}},gamemode=!spectator] run function {ns}:v{version}/zombies/rescue_tp
# Everyone downed: no player to measure from, so fall back to the enemy's own position.
execute if score #zb_near_found {ns}.data matches 1.. unless entity @p[scores={{{ns}.zb.in_game=1,{ns}.zb.downed=0}},gamemode=!spectator] run function {ns}:v{version}/zombies/rescue_tp
execute if score #zb_near_found {ns}.data matches 1.. run tag @s add {ns}.zb_rescued
tag @e[tag={ns}.zb_near] remove {ns}.zb_near

# The teleport moved the zombie somewhere new, so a past escort failure no longer applies:
# clear the flag so a future stuck timeout gets a trader again. It only needs to survive long
# enough to route the give_up -> on_stuck_zombie call past the escort router (see escort.py).
execute if score #zb_near_found {ns}.data matches 1.. run tag @s remove {ns}.zb_escort_failed

# Reset stuck tracking from the new position so it gets a fresh window
scoreboard players set @s {ns}.zb.stuck_dist 4
execute store result score @s {ns}.zb.stuck_x run data get entity @s Pos[0]
execute store result score @s {ns}.zb.stuck_z run data get entity @s Pos[2]
scoreboard players operation @s {ns}.zb.stuck_ticks = #total_tick {ns}.data
""")

	## @s = the stuck enemy, execution POSITION = the player it should end up near (see caller).
	## Both selectors resolve from that position, so they agree on which marker was chosen.
	write_versioned_function("zombies/rescue_tp", f"""
tp @s @n[tag={ns}.zb_near]
scoreboard players operation @s {ns}.zb.spawn.sid = @n[tag={ns}.zb_near] {ns}.zb.spawn.sid
""")

	## Player boundary check (zombies): unlike zombies (out_of_world damage -> down + mannequin), a player leaving the play area is a TOTAL elimination with no mannequin, respawning at the next round end.
	## Uses the same #bound_* scores loaded by shared/load_bounds.
	write_versioned_function("zombies/check_bounds_player", f"""
data modify storage {ns}:temp _player_pos set from entity @s Pos
execute store result score @s {ns}.mp.bx run data get storage {ns}:temp _player_pos[0]
execute store result score @s {ns}.mp.by run data get storage {ns}:temp _player_pos[1]
execute store result score @s {ns}.mp.bz run data get storage {ns}:temp _player_pos[2]

execute if score @s {ns}.mp.bx < #bound_x1 {ns}.data run return run function {ns}:v{version}/zombies/revive/full_death
execute if score @s {ns}.mp.bx > #bound_x2 {ns}.data run return run function {ns}:v{version}/zombies/revive/full_death
execute if score @s {ns}.mp.by < #bound_y1 {ns}.data run return run function {ns}:v{version}/zombies/revive/full_death
execute if score @s {ns}.mp.by > #bound_y2 {ns}.data run return run function {ns}:v{version}/zombies/revive/full_death
execute if score @s {ns}.mp.bz < #bound_z1 {ns}.data run return run function {ns}:v{version}/zombies/revive/full_death
execute if score @s {ns}.mp.bz > #bound_z2 {ns}.data run return run function {ns}:v{version}/zombies/revive/full_death
""")

