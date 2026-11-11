
#> mgs:zombies/bonus/nuke
#
# @within	mgs:v5.4.2/zombies/powerups/activate/nuke
#

# Marked entities lose their attack damage at once, so those waiting in the loop can no longer hurt anyone.
execute as @e[tag=mgs.nukable] run function mgs:v5.4.2/zombies/bonus/nuke_mark_one

function mgs:v5.4.2/zombies/bonus/nuke_loop

