""" The teddy bear and the move that follows: ascend, wait, descend and the arrival announce. """
# ruff: noqa: E501
# Imports
from stewbeet import Mem, write_versioned_function

from ....core.feedback import ZombiesFeedback
from ....helpers import MGS_TAG
from .shared import MB_CLOSED_TF, MOVE_ASCEND_TICKS, MOVE_DESCEND_TICKS, MOVE_TOTAL_TICKS, MOVE_WAIT_TICKS


# Functions
def write_mystery_box_move() -> None:
	ns: str = Mem.ctx.project_id
	version: str = Mem.ctx.project_version

	## Teddy bear result: box is about to move (Black Ops style). @s = the active box's display.
	write_versioned_function("zombies/mystery_box/show_bear_result", f"""
# Close this box's lid before it moves away
function {ns}:v{version}/zombies/mystery_box/close_lid

# Mark this display as the moving bear so the move animation only touches it (not other pulls)
tag @s add {ns}.mb_bear

# The other spots keep their grayed crates: only the destination's is cleared, and only once the
# destination is known (move_anim_transition). A spot the box never visits must never blink out.

# Replace display with teddy bear
loot replace entity @s contents loot {ns}:zombies/roaming_bear
data merge entity @s {{transformation:{{translation:[0f,1.25f,0f],scale:[0.75f,0.75f,0.75f]}}}}

# Refund this box's buyer (the moving box eats the pull, no weapon given)
scoreboard players operation #this_buyer {ns}.data = @s {ns}.mb.buyer
execute as @a[scores={{{ns}.zb.in_game=1}}] if score @s {ns}.mb.pid = #this_buyer {ns}.data run scoreboard players operation @s {ns}.zb.points += #zb_mystery_box_price {ns}.config

# Start move animation timer (this display is killed by the move at the ascend phase)
scoreboard players set #mb_move_timer {ns}.data {MOVE_TOTAL_TICKS}

tellraw @a[scores={{{ns}.zb.in_game=1}}] [{MGS_TAG},{{"text":"The Mystery Box is moving!","color":"yellow","bold":true}}]
{ZombiesFeedback.zb_sound('box_bye_bye')}
""")

	## Move animation tick dispatcher.
	# Timer phases, counting down from {MOVE_TOTAL_TICKS}=280:
	#   - bear visible (280..251): bear rises out of box (30 ticks)
	#   - ascend (250..171): chest + bear rise up (80 ticks)
	#   - wait (170..71): pause with no box visible (100 ticks = 5 seconds)
	#   - transition (70): pick new location, spawn descending chest
	#   - descend (69..1): chest descends at new location (69 ticks)
	#   - land (0): finalize

	ascend_start: int = MOVE_ASCEND_TICKS + MOVE_WAIT_TICKS + MOVE_DESCEND_TICKS + 1	# 251
	ascend_end: int = MOVE_WAIT_TICKS + MOVE_DESCEND_TICKS + 1						# 171
	transition: int = MOVE_DESCEND_TICKS							# 70
	descend_end: int = 1

	write_versioned_function("zombies/mystery_box/move_anim_tick", f"""
scoreboard players remove #mb_move_timer {ns}.data 1

# Bear phase: start ascend interpolation on chest + bear
execute if score #mb_move_timer {ns}.data matches {ascend_start} run function {ns}:v{version}/zombies/mystery_box/move_anim_start_ascend

# Ascend phase: move chest + bear upward (slow then fast)
execute if score #mb_move_timer {ns}.data matches {ascend_end}..{ascend_start} run function {ns}:v{version}/zombies/mystery_box/move_anim_ascend_step

# End of ascend: kill the moving bear + the old (non-temp) presence box only
execute if score #mb_move_timer {ns}.data matches {ascend_end - 1} run kill @e[tag={ns}.mb_bear]
execute if score #mb_move_timer {ns}.data matches {ascend_end - 1} run kill @e[tag={ns}.mb_presence,tag=!{ns}.mb_temp]
# If a Fire Sale had ended and that bear was the last in-progress display, finish temp cleanup now
execute if score #mb_move_timer {ns}.data matches {ascend_end - 1} if score #mb_fs_cleanup_pending {ns}.data matches 1 unless entity @e[tag={ns}.mb_display] run function {ns}:v{version}/zombies/mystery_box/fire_sale_cleanup

# Wait phase ({ascend_end - 1}..{transition + 1}): 5 seconds, no box visible

# Transition: pick new location, spawn descending chest
execute if score #mb_move_timer {ns}.data matches {transition} run function {ns}:v{version}/zombies/mystery_box/move_anim_transition

# Descend phase: chest descends at new location (fast then slow)
execute if score #mb_move_timer {ns}.data matches {descend_end}..{transition - 1} run function {ns}:v{version}/zombies/mystery_box/move_anim_descend_step

# Land: finalize
execute if score #mb_move_timer {ns}.data matches 0 run function {ns}:v{version}/zombies/mystery_box/move_anim_land
""")

	write_versioned_function("zombies/mystery_box/move_anim_start_ascend", f"""
# Enable smooth movement on the active chest (base + lid) and the bear display only
execute as @e[tag={ns}.mb_presence,tag=!{ns}.mb_temp] run data merge entity @s {{teleport_duration:5}}
execute as @e[tag={ns}.mb_bear] run data merge entity @s {{teleport_duration:5}}
execute as @n[tag={ns}.mystery_box_active] at @s run {ZombiesFeedback.zb_sound('box_disappear')}
""")

	# Ascend: slow first half, fast second half
	ascend_mid: int = ascend_end + MOVE_ASCEND_TICKS // 2	# 111
	write_versioned_function("zombies/mystery_box/move_anim_ascend_step", f"""
# Slow phase (first half): rise ~0.06 blocks/tick
execute if score #mb_move_timer {ns}.data matches {ascend_mid}..{ascend_start} as @e[tag={ns}.mb_presence,tag=!{ns}.mb_temp] at @s run tp @s ~ ~0.06 ~
execute if score #mb_move_timer {ns}.data matches {ascend_mid}..{ascend_start} as @e[tag={ns}.mb_bear] at @s run tp @s ~ ~0.06 ~

# Fast phase (second half): rise ~0.18 blocks/tick
execute if score #mb_move_timer {ns}.data matches {ascend_end}..{ascend_mid - 1} as @e[tag={ns}.mb_presence,tag=!{ns}.mb_temp] at @s run tp @s ~ ~0.18 ~
execute if score #mb_move_timer {ns}.data matches {ascend_end}..{ascend_mid - 1} as @e[tag={ns}.mb_bear] at @s run tp @s ~ ~0.18 ~

# Smoke particles at old location
execute at @n[tag={ns}.mystery_box_active] run particle minecraft:large_smoke ~ ~1 ~ 0.3 0.5 0.3 0.02 2 force @a[distance=..48]
""")

	write_versioned_function("zombies/mystery_box/move_anim_transition", f"""
# Pick new active position
function {ns}:v{version}/zombies/mystery_box/move_active_position

# Bring the new active box's interaction entity into reach (and hide the old one) BEFORE the chest
# is positioned relative to it below — otherwise the chest would spawn at the hidden -512 offset.
function {ns}:v{version}/zombies/mystery_box/sync_interaction_visibility

# The destination is the only spot losing its grayed crate, and only now that it is known — the
# arriving chest must not land on top of one. refresh_disabled rebuilds the whole set on landing.
execute as @n[tag={ns}.mystery_box_active] at @s run kill @e[tag={ns}.mb_disabled,distance=..3]

# Spawn new chest display (base + lid) above the new active position (height = 0.7 + descent total)
# Fast: 35t * 0.18 = 6.3 blocks, Slow: 34t * 0.06 = 2.04 blocks, Total = 8.34
execute as @n[tag={ns}.mystery_box_active] at @s positioned ~ ~7.54 ~ run summon minecraft:item_display ~ ~ ~ {{Tags:["{ns}.mb_presence","{ns}.mb_base","{ns}.gm_entity"],item_display:"fixed",billboard:"fixed",item:{{id:"minecraft:chest",count:1,components:{{"minecraft:item_model":"{ns}:mystery_box_base"}}}},transformation:{MB_CLOSED_TF},teleport_duration:5}}
execute as @n[tag={ns}.mystery_box_active] at @s positioned ~ ~7.54 ~ run summon minecraft:item_display ~ ~ ~ {{Tags:["{ns}.mb_presence","{ns}.mb_lid","{ns}.gm_entity"],item_display:"fixed",billboard:"fixed",item:{{id:"minecraft:chest",count:1,components:{{"minecraft:item_model":"{ns}:mystery_box_lid"}}}},transformation:{MB_CLOSED_TF},teleport_duration:5}}
execute as @n[tag={ns}.mystery_box_active] at @s as @e[tag={ns}.mb_presence,tag=!{ns}.mb_temp] run data modify entity @s Rotation set from entity @n[tag={ns}.mystery_box_active] Rotation

# Light beam particles at new location
execute at @n[tag={ns}.mystery_box_active] run particle minecraft:end_rod ~ ~3 ~ 0.1 2 0.1 0.05 20 force @a[distance=..64]
execute as @n[tag={ns}.mystery_box_active] at @s run {ZombiesFeedback.zb_sound('box_poof')}
""")

	# Descend: fast first half, slow second half (landing)
	descend_mid: int = MOVE_DESCEND_TICKS // 2		# 35
	write_versioned_function("zombies/mystery_box/move_anim_descend_step", f"""
# Fast phase (first half): descend ~0.18 blocks/tick
execute if score #mb_move_timer {ns}.data matches {descend_mid}..{transition - 1} as @e[tag={ns}.mb_presence,tag=!{ns}.mb_temp] at @s run tp @s ~ ~-0.18 ~

# Slow phase (second half, landing): descend ~0.06 blocks/tick
execute if score #mb_move_timer {ns}.data matches {descend_end}..{descend_mid - 1} as @e[tag={ns}.mb_presence,tag=!{ns}.mb_temp] at @s run tp @s ~ ~-0.06 ~

# Trailing particles
execute at @n[tag={ns}.mb_presence,tag=!{ns}.mb_temp] run particle minecraft:end_rod ~ ~-0.5 ~ 0.2 0.1 0.2 0.01 1 force @a[distance=..48]
""")

	write_versioned_function("zombies/mystery_box/move_anim_land", f"""
# Snap the descending chest (base + lid) to exact final position smoothly
execute as @n[tag={ns}.mystery_box_active] at @s as @e[tag={ns}.mb_presence,tag=!{ns}.mb_temp] run tp @s ~ ~-0.9 ~

# Reset move state
scoreboard players set #mb_move_timer {ns}.data 0
data remove storage {ns}:zombies mystery_box.result

# The old active spot is now inactive: (re)build the grayed disabled crates at every inactive spot
function {ns}:v{version}/zombies/mystery_box/refresh_disabled

# Resolve the new spot's editor-given name into mystery_box.current_name, unset when it has none
function {ns}:v{version}/zombies/mystery_box/read_location_name

# Announce arrival, naming the place when the map maker gave this spot one
execute unless data storage {ns}:zombies mystery_box.current_name run tellraw @a[scores={{{ns}.zb.in_game=1}}] [{MGS_TAG},{{"text":"The Mystery Box has arrived at a new location!","color":"yellow"}}]
execute if data storage {ns}:zombies mystery_box.current_name run tellraw @a[scores={{{ns}.zb.in_game=1}}] [{MGS_TAG},{{"text":"The Mystery Box has arrived at ","color":"yellow"}},{{"storage":"{ns}:zombies","nbt":"mystery_box.current_name","color":"gold","bold":true}},"!"]
execute as @n[tag={ns}.mystery_box_active] at @s run {ZombiesFeedback.zb_sound('box_land')}
""")

	## Look up the active box's location name. Split in two because the list index is dynamic:
	# the macro only moves NBT around, so no `text:` literal ever contains a macro argument, which
	# would otherwise mint a junk auto.lang_file key (see REFACTOR_PLAN gotchas).
	write_versioned_function("zombies/mystery_box/read_location_name", f"""
# names[] is 0-based, box ids are 1-based
data remove storage {ns}:zombies mystery_box.current_name
execute as @n[tag={ns}.mystery_box_active] run scoreboard players operation #mb_name_idx {ns}.data = @s {ns}.mb.box
scoreboard players remove #mb_name_idx {ns}.data 1
execute store result storage {ns}:temp _mb_name_idx.idx int 1 run scoreboard players get #mb_name_idx {ns}.data
function {ns}:v{version}/zombies/mystery_box/read_location_name_at with storage {ns}:temp _mb_name_idx

# An unnamed spot stores "", which must read the same as having no name at all
execute if data storage {ns}:zombies mystery_box{{current_name:""}} run data remove storage {ns}:zombies mystery_box.current_name
""")

	write_versioned_function("zombies/mystery_box/read_location_name_at", f"""
$data modify storage {ns}:zombies mystery_box.current_name set from storage {ns}:zombies mystery_box.names[$(idx)]
""")

