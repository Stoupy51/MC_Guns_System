
#> mgs:v5.0.0/zombies/mystery_box/check_use
#
# @within	mgs:v5.0.0/zombies/game_tick
#

# Check if any player interacted with the active mystery box
execute as @e[tag=mgs.mystery_box_active] if data entity @s interaction.player run function mgs:v5.0.0/zombies/mystery_box/on_interact

