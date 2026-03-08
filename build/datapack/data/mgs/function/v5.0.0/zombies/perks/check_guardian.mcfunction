
#> mgs:v5.0.0/zombies/perks/check_guardian
#
# @within	mgs:v5.0.0/zombies/start_round
#

# Check guardian ability for all players with it ready
execute as @a[scores={mgs.zb.in_game=1,mgs.zb.ability=2,mgs.zb.ability_cd=0},gamemode=!spectator] at @s run function mgs:v5.0.0/zombies/perks/trigger_guardian

