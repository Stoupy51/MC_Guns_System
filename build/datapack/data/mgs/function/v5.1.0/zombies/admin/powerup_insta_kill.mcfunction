
#> mgs:v5.1.0/zombies/admin/powerup_insta_kill
#
# @within	???
#

execute unless data storage mgs:zombies game{state:"active"} run return run tellraw @s [[{"text":"","color":"gold"},"[",{"translate":"mgs"},"] "],{"translate":"mgs.no_zombies_game_is_active","color":"red"}]
tag @s[scores={mgs.zb.in_game=1},gamemode=!spectator] add mgs.pu_collecting
execute unless entity @a[tag=mgs.pu_collecting] run tag @a[scores={mgs.zb.in_game=1},gamemode=!spectator,limit=1] add mgs.pu_collecting
execute unless entity @a[tag=mgs.pu_collecting] run return run tellraw @s [[{"text":"","color":"gold"},"[",{"translate":"mgs"},"] "],{"translate":"mgs.no_living_player_in_the_game_to_receive_the_power_up","color":"red"}]
function mgs:v5.1.0/zombies/powerups/activate/insta_kill
tag @a[tag=mgs.pu_collecting] remove mgs.pu_collecting

