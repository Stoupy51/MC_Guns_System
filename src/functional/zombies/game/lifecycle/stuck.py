""" Rescuing unreachable zombies and keeping players inside the map bounds. """
# Imports
from stewbeet import Mem, write_versioned_function

from ....helpers.probes import Probe


# Functions
def write_stuck_and_bounds() -> None:
	ns: str = Mem.ctx.project_id
	version: str = Mem.ctx.project_version

	write_versioned_function("zombies/stuck_zombie_check", f"""
# Run as a non-rising zombie_round, every 20 ticks on up to 24 random ones. Progress resets the timer.
# Timeout: 400 ticks without moving (100 once already rescued), 300 if it moves without getting closer.

# Distance bucket to the nearest alive player, 4 (very far) to 0 (adjacent).
scoreboard players set #cur_dist_bucket {ns}.data 4
execute if entity @a[scores={{{ns}.zb.in_game=1,{ns}.zb.downed=0}},gamemode=!spectator,distance=..96] run scoreboard players set #cur_dist_bucket {ns}.data 3
execute if entity @a[scores={{{ns}.zb.in_game=1,{ns}.zb.downed=0}},gamemode=!spectator,distance=..64] run scoreboard players set #cur_dist_bucket {ns}.data 2
execute if entity @a[scores={{{ns}.zb.in_game=1,{ns}.zb.downed=0}},gamemode=!spectator,distance=..32] run scoreboard players set #cur_dist_bucket {ns}.data 1
execute if entity @a[scores={{{ns}.zb.in_game=1,{ns}.zb.downed=0}},gamemode=!spectator,distance=..16] run scoreboard players set #cur_dist_bucket {ns}.data 0

execute store result score #cur_x {ns}.data run data get entity @s Pos[0]
execute store result score #cur_z {ns}.data run data get entity @s Pos[2]

# Progress: the bucket improved, or bucket 0 with the player visible. Without the line-of-sight test a player
# above or below a floor kept the zombie "not stuck" forever. XZ movement is not progress: a zombie attacking stands still.
scoreboard players set #stuck_progress {ns}.data 0
execute if score #cur_dist_bucket {ns}.data < @s {ns}.zb.stuck_dist run scoreboard players set #stuck_progress {ns}.data 1
scoreboard players set #zb_stuck_see {ns}.data 0
execute if score #cur_dist_bucket {ns}.data matches 0 positioned as @p[scores={{{ns}.zb.in_game=1,{ns}.zb.downed=0}},gamemode=!spectator,distance=..16] store result score #zb_stuck_see {ns}.data run function #bs.view:can_see_ata {{with:{{}}}}
execute if score #zb_stuck_see {ns}.data matches 1 run scoreboard players set #stuck_progress {ns}.data 1

# During a PaP-room lure, a zombie at the theatre centre is where it should be (see escort, lure mode).
execute if score #zb_lure {ns}.data matches 1 if entity @e[tag={ns}.lure_center,distance=..12] run scoreboard players set #stuck_progress {ns}.data 1

execute if score #stuck_progress {ns}.data matches 1 run scoreboard players operation @s {ns}.zb.stuck_dist = #cur_dist_bucket {ns}.data
execute if score #stuck_progress {ns}.data matches 1 run scoreboard players operation @s {ns}.zb.stuck_x = #cur_x {ns}.data
execute if score #stuck_progress {ns}.data matches 1 run scoreboard players operation @s {ns}.zb.stuck_z = #cur_z {ns}.data
execute if score #stuck_progress {ns}.data matches 1 run scoreboard players operation @s {ns}.zb.stuck_ticks = #total_tick {ns}.data
execute if score #stuck_progress {ns}.data matches 1 run tag @s remove {ns}.zb_rescued
execute if score #stuck_progress {ns}.data matches 1 run return 0

# Moved: XZ differs from the snapshot at the last progress (block precision).
scoreboard players set #stuck_moved {ns}.data 0
execute unless score #cur_x {ns}.data = @s {ns}.zb.stuck_x run scoreboard players set #stuck_moved {ns}.data 1
execute unless score #cur_z {ns}.data = @s {ns}.zb.stuck_z run scoreboard players set #stuck_moved {ns}.data 1
scoreboard players set #stuck_threshold {ns}.data 400
execute if score #stuck_moved {ns}.data matches 1 run scoreboard players set #stuck_threshold {ns}.data 300
execute if score #stuck_moved {ns}.data matches 0 if entity @s[tag={ns}.zb_rescued] run scoreboard players set #stuck_threshold {ns}.data 100

# With 2 zombies left the timeout drops to 5 s, so a hard-to-reach zombie is rescued quickly.
execute if score #zb_alive {ns}.data matches ..2 if score #stuck_threshold {ns}.data matches 101.. run scoreboard players set #stuck_threshold {ns}.data 100

scoreboard players operation #stuck_delta {ns}.data = #total_tick {ns}.data
scoreboard players operation #stuck_delta {ns}.data -= @s {ns}.zb.stuck_ticks
execute if score #stuck_delta {ns}.data >= #stuck_threshold {ns}.data run function {ns}:v{version}/zombies/on_stuck_zombie
""")

	write_versioned_function("zombies/on_stuck_zombie", f"""
# Run as the stuck zombie: move it to a spawn near a player instead of killing it, back onto walkable ground.

# Dogs use their own markers: a zombie spawn may sit where only walkers belong, or outside the play bounds.
execute unless entity @s[tag={ns}.zb_dog] run function {ns}:v{version}/zombies/tag_spawns_near_players
execute if entity @s[tag={ns}.zb_dog] run function {ns}:v{version}/zombies/tag_special_spawns_near_players

# Never the spawn it last used, unless it is the only candidate.
scoreboard players operation #zb_last_sid {ns}.data = @s {ns}.zb.spawn.sid
execute as @e[tag={ns}.zb_near] if score @s {ns}.zb.spawn.sid = #zb_last_sid {ns}.data run tag @s add {ns}.zb_near_prev
execute store result score #zb_near_alt {ns}.data if entity @e[tag={ns}.zb_near,tag=!{ns}.zb_near_prev]
execute if score #zb_near_alt {ns}.data matches 1.. run tag @e[tag={ns}.zb_near_prev] remove {ns}.zb_near
tag @e[tag={ns}.zb_near_prev] remove {ns}.zb_near_prev

# The spawn nearest the player, not the enemy: from the enemy, a stranded one bounced between the same two far spawns.
execute if score #zb_near_found {ns}.data matches 1.. at @p[scores={{{ns}.zb.in_game=1,{ns}.zb.downed=0}},gamemode=!spectator] run function {ns}:v{version}/zombies/rescue_tp
# Everyone downed: measure from the enemy instead.
execute if score #zb_near_found {ns}.data matches 1.. unless entity @p[scores={{{ns}.zb.in_game=1,{ns}.zb.downed=0}},gamemode=!spectator] run function {ns}:v{version}/zombies/rescue_tp
execute if score #zb_near_found {ns}.data matches 1.. run tag @s add {ns}.zb_rescued
tag @e[tag={ns}.zb_near] remove {ns}.zb_near

# After a teleport a past escort failure no longer applies, so a later stuck timeout gets a trader again.
execute if score #zb_near_found {ns}.data matches 1.. run tag @s remove {ns}.zb_escort_failed

# Fresh stuck window from the new position.
scoreboard players set @s {ns}.zb.stuck_dist 4
execute store result score @s {ns}.zb.stuck_x run data get entity @s Pos[0]
execute store result score @s {ns}.zb.stuck_z run data get entity @s Pos[2]
scoreboard players operation @s {ns}.zb.stuck_ticks = #total_tick {ns}.data
""")

	## Run as the stuck enemy, at the player it should end up near, so both selectors pick the same marker.
	write_versioned_function("zombies/rescue_tp", f"""
tp @s @n[tag={ns}.zb_near]
scoreboard players operation @s {ns}.zb.spawn.sid = @n[tag={ns}.zb_near] {ns}.zb.spawn.sid
""")

	## A player leaving the play area is eliminated with no mannequin and respawns at the next round end.
	## Uses the #bound_* scores from shared/load_bounds.
	write_versioned_function("zombies/check_bounds_player", f"""
{Probe.pos()}
execute store result score @s {ns}.mp.bx run data get storage {ns}:temp _probe_pos[0]
execute store result score @s {ns}.mp.by run data get storage {ns}:temp _probe_pos[1]
execute store result score @s {ns}.mp.bz run data get storage {ns}:temp _probe_pos[2]

execute if score @s {ns}.mp.bx < #bound_x1 {ns}.data run return run function {ns}:v{version}/zombies/revive/full_death
execute if score @s {ns}.mp.bx > #bound_x2 {ns}.data run return run function {ns}:v{version}/zombies/revive/full_death
execute if score @s {ns}.mp.by < #bound_y1 {ns}.data run return run function {ns}:v{version}/zombies/revive/full_death
execute if score @s {ns}.mp.by > #bound_y2 {ns}.data run return run function {ns}:v{version}/zombies/revive/full_death
execute if score @s {ns}.mp.bz < #bound_z1 {ns}.data run return run function {ns}:v{version}/zombies/revive/full_death
execute if score @s {ns}.mp.bz > #bound_z2 {ns}.data run return run function {ns}:v{version}/zombies/revive/full_death
""")

