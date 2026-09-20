
#> mgs:zombies/bonus/nuke
#
# @executed	at @s
#
# @within	mgs:v5.1.0/zombies/powerups/activate/nuke
#

# Mark every nukable entity: tagged for the kill loop and stripped of its attack damage right away,
# so the ones waiting their turn in the loop can no longer hurt anybody.
execute as @e[tag=mgs.nukable] run function mgs:v5.1.0/zombies/bonus/nuke_mark_one

# Start kill loop (1 entity per tick)
function mgs:v5.1.0/zombies/bonus/nuke_loop

