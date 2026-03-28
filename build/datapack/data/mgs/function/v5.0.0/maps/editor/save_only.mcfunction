
#> mgs:v5.0.0/maps/editor/save_only
#
# @executed	as @p[tag=mgs.map_editor,distance=..6,sort=nearest]
#
# @within	mgs:v5.0.0/maps/editor/process_element [ as @p[tag=mgs.map_editor,distance=..6,sort=nearest] ]
#

# Only process if in editor mode
execute unless score @s mgs.mp.map_edit matches 1 run return fail

# Do the actual save
function mgs:v5.0.0/maps/editor/do_save

# Re-give tools (since save clears + re-gives via advancement revoke)
function mgs:v5.0.0/maps/editor/give_tools

tellraw @s [[{"text":"","color":"gold"},"[",{"translate":"mgs"},"] "],{"translate":"mgs.map_saved","color":"green"}]

