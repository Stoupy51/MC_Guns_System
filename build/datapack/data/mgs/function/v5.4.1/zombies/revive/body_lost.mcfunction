
#> mgs:v5.4.1/zombies/revive/body_lost
#
# @within	mgs:v5.4.1/dialog/close_then
#			mgs:v5.4.1/zombies/revive/downed_tick
#

function mgs:v5.4.1/zombies/revive/stay_down
title @s times 0 60 20
title @s title ["☠"]
title @s subtitle [{"translate":"mgs.your_body_left_the_map_respawning_next_round","fallback":"Your body left the map. Respawning next round...","color":"gray"}]
tellraw @a[scores={mgs.zb.in_game=1}] [[{"text":"","color":"gold"},"[",{"translate":"mgs","fallback":"MGS"},"] "],["",{"text":"[","color":"dark_gray"},{"score":{"name":"@s","objective":"mgs.zb.xp_level"},"color":"gold"},{"text":"] ","color":"dark_gray"},{"selector":"@s","color":"dark_red"}],[{"text":"'","color":"gray"}, {"translate":"mgs.s_body_left_the_map","fallback":"s body left the map."}]]

