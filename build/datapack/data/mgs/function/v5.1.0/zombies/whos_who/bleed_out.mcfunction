
#> mgs:v5.1.0/zombies/whos_who/bleed_out
#
# @executed	at @s
#
# @within	mgs:v5.1.0/zombies/whos_who/owner_tick
#

function mgs:v5.1.0/zombies/whos_who/forfeit
title @s times 0 60 20
title @s title ["☠"]
title @s subtitle [{"translate":"mgs.your_body_bled_out_fight_on_with_your_pistol","color":"gray"}]
tellraw @a[scores={mgs.zb.in_game=1}] [[{"text":"","color":"gold"},"[",{"translate":"mgs"},"] "],["",{"text":"[","color":"dark_gray"},{"score":{"name":"@s","objective":"mgs.zb.xp_level"},"color":"gold"},{"text":"] ","color":"dark_gray"},{"selector":"@s","color":"dark_aqua"}],[{"text":"'","color":"gray"}, {"translate":"mgs.s_body_bled_out"}]]

