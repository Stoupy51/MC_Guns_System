""" The teddy bear and the move that follows: ascend, wait, descend and the arrival announce. """
# Imports
from stewbeet import Mem, write_versioned_function

from ....core.feedback import ZombiesFeedback
from ....helpers import MGS_TAG
from .shared import (
	INTERACTION_LIFT,
	MOVE_ASCEND_TICKS,
	MOVE_DESCEND_TICKS,
	MOVE_TOTAL_TICKS,
	MOVE_WAIT_TICKS,
	PULL_DROP,
	box_offset,
	box_transformation,
	per_roll,
)


# Functions
def write_mystery_box_move() -> None:
	ns: str = Mem.ctx.project_id
	version: str = Mem.ctx.project_version

	## Teddy bear: the box moves (Black Ops style). Run as the active box's display.
	write_versioned_function("zombies/mystery_box/show_bear_result", f"""
function {ns}:v{version}/zombies/mystery_box/close_lid

# Only the display tagged mb_bear moves, so other pulls are untouched.
tag @s add {ns}.mb_bear

# Only the destination's grayed crate goes, once it is known (move_anim_transition).

loot replace entity @s contents loot {ns}:zombies/roaming_bear
{per_roll(lambda roll: f"data merge entity @s {{transformation:{box_transformation(roll, (0.0, 1.25 - PULL_DROP, 0.0), scale=0.75)}}}")}

# The moving box eats the pull: refund the buyer.
scoreboard players operation #this_buyer {ns}.data = @s {ns}.mb.buyer
execute as @a[scores={{{ns}.zb.in_game=1}}] if score @s {ns}.mb.pid = #this_buyer {ns}.data run scoreboard players operation @s {ns}.zb.points += #zb_mystery_box_price {ns}.config

# The move kills this display during the ascend phase.
scoreboard players set #mb_move_timer {ns}.data {MOVE_TOTAL_TICKS}

tellraw @a[scores={{{ns}.zb.in_game=1}}] [{MGS_TAG},{{"text":"The Mystery Box is moving!","color":"yellow","bold":true}}]
{ZombiesFeedback.zb_sound('box_bye_bye')}
""")

	## Countdown from {MOVE_TOTAL_TICKS} (280): bear rises 280-251, chest and bear ascend 250-171, 5 s with no box 170-71,
	## new location at 70, chest descends 69-1, lands at 0.

	ascend_start: int = MOVE_ASCEND_TICKS + MOVE_WAIT_TICKS + MOVE_DESCEND_TICKS + 1
	ascend_end: int = MOVE_WAIT_TICKS + MOVE_DESCEND_TICKS + 1
	transition: int = MOVE_DESCEND_TICKS
	descend_end: int = 1

	write_versioned_function("zombies/mystery_box/move_anim_tick", f"""
scoreboard players remove #mb_move_timer {ns}.data 1

execute if score #mb_move_timer {ns}.data matches {ascend_start} run function {ns}:v{version}/zombies/mystery_box/move_anim_start_ascend

# Slow, then fast.
execute if score #mb_move_timer {ns}.data matches {ascend_end}..{ascend_start} run function {ns}:v{version}/zombies/mystery_box/move_anim_ascend_step

# Only the moving bear and the old box, not the temporary Fire Sale boxes.
execute if score #mb_move_timer {ns}.data matches {ascend_end - 1} run kill @e[tag={ns}.mb_bear]
execute if score #mb_move_timer {ns}.data matches {ascend_end - 1} run kill @e[tag={ns}.mb_presence,tag=!{ns}.mb_temp]
# A Fire Sale that ended while this bear was the last pull finishes its cleanup now.
execute if score #mb_move_timer {ns}.data matches {ascend_end - 1} if score #mb_fs_cleanup_pending {ns}.data matches 1 unless entity @e[tag={ns}.mb_display] run function {ns}:v{version}/zombies/mystery_box/fire_sale_cleanup

execute if score #mb_move_timer {ns}.data matches {transition} run function {ns}:v{version}/zombies/mystery_box/move_anim_transition

# Fast, then slow.
execute if score #mb_move_timer {ns}.data matches {descend_end}..{transition - 1} run function {ns}:v{version}/zombies/mystery_box/move_anim_descend_step

execute if score #mb_move_timer {ns}.data matches 0 run function {ns}:v{version}/zombies/mystery_box/move_anim_land
""")

	write_versioned_function("zombies/mystery_box/move_anim_start_ascend", f"""
# Smooth movement on the active chest (base and lid) and the bear only.
execute as @e[tag={ns}.mb_presence,tag=!{ns}.mb_temp] run data merge entity @s {{teleport_duration:5}}
execute as @e[tag={ns}.mb_bear] run data merge entity @s {{teleport_duration:5}}
execute as @n[tag={ns}.mystery_box_active] at @s run {ZombiesFeedback.zb_sound('box_disappear')}
""")

	# Up and down along the box's own up, which is down for a box upside down.
	ascend_mid: int = ascend_end + MOVE_ASCEND_TICKS // 2
	for name, step in (("rise_slow", 0.06), ("rise_fast", 0.18), ("sink_fast", -0.18), ("sink_slow", -0.06)):
		write_versioned_function(f"zombies/mystery_box/{name}", per_roll(lambda roll, step=step: f"tp @s {box_offset(roll, 0.0, step, 0.0)}"))
	moving: str = f"@e[tag={ns}.mb_presence,tag=!{ns}.mb_temp]"
	write_versioned_function("zombies/mystery_box/move_anim_ascend_step", f"""
execute if score #mb_move_timer {ns}.data matches {ascend_mid}..{ascend_start} as {moving} at @s run function {ns}:v{version}/zombies/mystery_box/rise_slow
execute if score #mb_move_timer {ns}.data matches {ascend_mid}..{ascend_start} as @e[tag={ns}.mb_bear] at @s run function {ns}:v{version}/zombies/mystery_box/rise_slow

execute if score #mb_move_timer {ns}.data matches {ascend_end}..{ascend_mid - 1} as {moving} at @s run function {ns}:v{version}/zombies/mystery_box/rise_fast
execute if score #mb_move_timer {ns}.data matches {ascend_end}..{ascend_mid - 1} as @e[tag={ns}.mb_bear] at @s run function {ns}:v{version}/zombies/mystery_box/rise_fast

execute at @n[tag={ns}.mystery_box_active] run particle minecraft:large_smoke ~ ~1 ~ 0.3 0.5 0.3 0.02 2 force @a[distance=..48]
""")

	# Height 0.1 + descent: 35 ticks x 0.18 + 34 ticks x 0.06 = 8.44 blocks above the new box's centre, along its up.
	descent: float = 0.1 + (MOVE_DESCEND_TICKS // 2) * 0.18 + (MOVE_DESCEND_TICKS - MOVE_DESCEND_TICKS // 2 - 1) * 0.06
	write_versioned_function("zombies/mystery_box/move_anim_transition", f"""
function {ns}:v{version}/zombies/mystery_box/move_active_position

# Before placing the chest, or it would spawn at the hidden -512 offset.
function {ns}:v{version}/zombies/mystery_box/sync_interaction_visibility

# The arriving chest must not land on a grayed crate; refresh_disabled rebuilds the set on landing.
execute as @n[tag={ns}.mystery_box_active] at @s run kill @e[tag={ns}.mb_disabled,distance=..3]

execute as @n[tag={ns}.mystery_box_active] at @s positioned ~ ~-{INTERACTION_LIFT} ~ run function {ns}:v{version}/zombies/mystery_box/summon_descending
execute as {moving} run data merge entity @s {{teleport_duration:5}}

execute at @n[tag={ns}.mystery_box_active] run particle minecraft:end_rod ~ ~3 ~ 0.1 2 0.1 0.05 20 force @a[distance=..64]
execute as @n[tag={ns}.mystery_box_active] at @s run {ZombiesFeedback.zb_sound('box_poof')}
""")
	## Run as the new active box interaction, at its centre.
	write_versioned_function("zombies/mystery_box/summon_descending", per_roll(lambda roll: (
		f'execute positioned {box_offset(roll, 0.0, round(descent, 2), 0.0)} run function {ns}:v{version}/zombies/mystery_box/summon_presence {{extra_tags:""}}'
	)))

	descend_mid: int = MOVE_DESCEND_TICKS // 2
	write_versioned_function("zombies/mystery_box/move_anim_descend_step", f"""
execute if score #mb_move_timer {ns}.data matches {descend_mid}..{transition - 1} as {moving} at @s run function {ns}:v{version}/zombies/mystery_box/sink_fast

execute if score #mb_move_timer {ns}.data matches {descend_end}..{descend_mid - 1} as {moving} at @s run function {ns}:v{version}/zombies/mystery_box/sink_slow

execute at @n[tag={ns}.mb_presence,tag=!{ns}.mb_temp] run particle minecraft:end_rod ~ ~-0.5 ~ 0.2 0.1 0.2 0.01 1 force @a[distance=..48]
""")

	write_versioned_function("zombies/mystery_box/move_anim_land", f"""
execute as @n[tag={ns}.mystery_box_active] at @s positioned ~ ~-{INTERACTION_LIFT} ~ as {moving} run tp @s ~ ~ ~

scoreboard players set #mb_move_timer {ns}.data 0
data remove storage {ns}:zombies mystery_box.result

# The old spot is now inactive: rebuild the grayed crates at every inactive spot.
function {ns}:v{version}/zombies/mystery_box/refresh_disabled

# Unset when the spot has no name.
function {ns}:v{version}/zombies/mystery_box/read_location_name

execute unless data storage {ns}:zombies mystery_box.current_name run tellraw @a[scores={{{ns}.zb.in_game=1}}] [{MGS_TAG},{{"text":"The Mystery Box has arrived at a new location!","color":"yellow"}}]
execute if data storage {ns}:zombies mystery_box.current_name run tellraw @a[scores={{{ns}.zb.in_game=1}}] [{MGS_TAG},{{"text":"The Mystery Box has arrived at ","color":"yellow"}},{{"storage":"{ns}:zombies","nbt":"mystery_box.current_name","color":"gold","bold":true}},"!"]
execute as @n[tag={ns}.mystery_box_active] at @s run {ZombiesFeedback.zb_sound('box_land')}
""")

	## Two functions because the list index is dynamic. The macro only moves NBT, so no `text:` literal holds a macro argument
	## (that would mint a junk auto.lang_file key).
	write_versioned_function("zombies/mystery_box/read_location_name", f"""
# names[] is 0-based, box ids 1-based.
data remove storage {ns}:zombies mystery_box.current_name
execute as @n[tag={ns}.mystery_box_active] run scoreboard players operation #mb_name_idx {ns}.data = @s {ns}.mb.box
scoreboard players remove #mb_name_idx {ns}.data 1
execute store result storage {ns}:temp _mb_name_idx.idx int 1 run scoreboard players get #mb_name_idx {ns}.data
function {ns}:v{version}/zombies/mystery_box/read_location_name_at with storage {ns}:temp _mb_name_idx

# An empty name counts as no name.
execute if data storage {ns}:zombies mystery_box{{current_name:""}} run data remove storage {ns}:zombies mystery_box.current_name
""")

	write_versioned_function("zombies/mystery_box/read_location_name_at", f"""
$data modify storage {ns}:zombies mystery_box.current_name set from storage {ns}:zombies mystery_box.names[$(idx)]
""")

