
#> mgs:v5.1.0/zombies/whos_who/bleed_out
#
# @executed	as @a[tag=mgs.ww_active,scores={mgs.zb.in_game=1}]
#
# @within	mgs:v5.1.0/zombies/whos_who/owner_tick
#

scoreboard players set @s mgs.zb.wwp.juggernog 0
scoreboard players set @s mgs.zb.wwp.speed_cola 0
scoreboard players set @s mgs.zb.wwp.double_tap 0
scoreboard players set @s mgs.zb.wwp.quick_revive 0
scoreboard players set @s mgs.zb.wwp.mule_kick 0
scoreboard players set @s mgs.zb.wwp.stamin_up 0
scoreboard players set @s mgs.zb.wwp.phd_flopper 0
scoreboard players set @s mgs.zb.wwp.deadshot 0
scoreboard players set @s mgs.zb.wwp.timeslip 0
scoreboard players set @s mgs.zb.wwp.electric_cherry 0
scoreboard players set @s mgs.zb.wwp.tombstone 0
scoreboard players set @s mgs.zb.wwp.whos_who 0
scoreboard players set @s mgs.zb.wwp.dying_wish 0
scoreboard players set @s mgs.zb.wwp.widows_wine 0
execute store result storage mgs:temp _ww_id.id int 1 run scoreboard players get @s mgs.zb.downed_id
function mgs:v5.1.0/zombies/whos_who/drop_inv with storage mgs:temp _ww_id
tag @s remove mgs.ww_active
scoreboard players set @s mgs.zb.ww.bleed 0
scoreboard players set @s mgs.zb.ww.rev 0
function mgs:v5.1.0/zombies/whos_who/despawn_body

title @s title ["☠"]
title @s subtitle [{"translate":"mgs.your_body_bled_out_fight_on_with_your_pistol","color":"gray"}]
tellraw @a[scores={mgs.zb.in_game=1}] [[{"text":"","color":"gold"},"[",{"translate":"mgs"},"] "],{"selector":"@s","color":"dark_aqua"},[{"text":"'","color":"gray"}, {"translate":"mgs.s_body_bled_out"}]]

