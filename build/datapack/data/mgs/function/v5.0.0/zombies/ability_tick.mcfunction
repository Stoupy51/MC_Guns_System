
#> mgs:v5.0.0/zombies/ability_tick
#
# @within	mgs:v5.0.0/zombies/game_tick
#

# Coward: TP to spawn when under 50% health (10 HP out of 20), cooldown not active
execute as @a[scores={mgs.zb.in_game=1,mgs.zb.ability=1,mgs.zb.ability_cd=0},gamemode=!spectator] at @s run function mgs:v5.0.0/zombies/perks/check_coward

