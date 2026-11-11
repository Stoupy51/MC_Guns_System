
#> mgs:v5.4.2/zombies/revive/bleed_out
#
# @within	mgs:v5.4.2/dialog/close_then
#			mgs:v5.4.2/zombies/revive/downed_tick
#

function mgs:v5.4.2/zombies/revive/stay_down
title @s times 0 60 20
title @s title ["☠"]
title @s subtitle [{"translate":"mgs.you_bled_out_respawning_next_round","fallback":"You bled out. Respawning next round...","color":"gray"}]
tellraw @a[scores={mgs.zb.in_game=1}] [[{"text":"","color":"gold"},"[",{"translate":"mgs","fallback":"MGS"},"] "],["",{"text":"[","color":"dark_gray"},{"score":{"name":"@s","objective":"mgs.zb.xp_level"},"color":"gold"},{"text":"] ","color":"dark_gray"},{"selector":"@s","color":"dark_red"}],[{"text":" ","color":"gray"}, {"translate":"mgs.has_bled_out","fallback":"has bled out."}]]

