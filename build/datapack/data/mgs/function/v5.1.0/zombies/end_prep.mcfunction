
#> mgs:v5.1.0/zombies/end_prep
#
# @within	mgs:v5.1.0/zombies/preload_complete 200t [ scheduled ]
#

execute unless data storage mgs:zombies game{state:"preparing"} run return fail
data modify storage mgs:zombies game.state set value "active"
execute as @a[scores={mgs.zb.in_game=1}] run attribute @s minecraft:movement_speed base reset
execute as @a[scores={mgs.zb.in_game=1}] run attribute @s minecraft:jump_strength base reset
effect clear @a[scores={mgs.zb.in_game=1}] darkness
effect clear @a[scores={mgs.zb.in_game=1}] blindness
effect clear @a[scores={mgs.zb.in_game=1}] night_vision

# Start round 1
function mgs:v5.1.0/zombies/start_round

# Call map start scripts (state is now active, chunks had time to load)
function mgs:v5.1.0/shared/maps/call_start_script_at_base

