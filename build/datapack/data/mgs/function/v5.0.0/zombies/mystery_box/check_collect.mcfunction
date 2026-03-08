
#> mgs:v5.0.0/zombies/mystery_box/check_collect
#
# @within	mgs:v5.0.0/zombies/game_tick
#

# Only check if result is ready
execute unless data storage mgs:zombies mystery_box{ready:true} run return 0

# Check if active box was interacted with again
execute as @e[tag=mgs.mystery_box_active] unless data entity @s interaction.player run return 0
data remove entity @s interaction

# Give the weapon to the nearest in-game player
execute at @e[tag=mgs.mystery_box_active,limit=1] as @p[distance=..3,scores={mgs.zb.in_game=1}] run function mgs:v5.0.0/zombies/mystery_box/collect

