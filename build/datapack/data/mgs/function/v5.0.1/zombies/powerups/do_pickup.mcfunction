
#> mgs:v5.0.1/zombies/powerups/do_pickup
#
# @executed	as @e[tag=mgs.pu_item] & at @s
#
# @within	mgs:v5.0.1/zombies/powerups/entity_tick
#

# Tag the nearest eligible player as the collector for this activation
tag @p[scores={mgs.zb.in_game=1},gamemode=!spectator,distance=..1.5,tag=!mgs.pu_collecting] add mgs.pu_collecting

# If no alive player collected, a downed player crawled their mannequin over it: credit them.
execute unless entity @a[tag=mgs.pu_collecting] if entity @e[tag=mgs.downed_mannequin,distance=..1.5] run function mgs:v5.0.1/zombies/powerups/pickup_downed_collector

# Store power-up type before killing the entity
scoreboard players operation #pu_type_pickup mgs.data = @s mgs.zb.pu.type

# Kill the text display first (we still have a valid position)
kill @n[tag=mgs.pu_text,distance=..3]

# Grab cue
execute as @a[scores={mgs.zb.in_game=1}] at @s run playsound mgs:zombies/powerups/item/grab ambient @s ~ ~ ~ 0.4 1.0

# Activate the power-up effect (collector tag is still active here)
function mgs:v5.0.1/zombies/powerups/dispatch_activate

# Kill this power-up item entity
kill @s

# Clean up the collector tag so other pickups can proceed
tag @a[tag=mgs.pu_collecting] remove mgs.pu_collecting

