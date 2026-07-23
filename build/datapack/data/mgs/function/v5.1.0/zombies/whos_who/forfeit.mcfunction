
#> mgs:v5.1.0/zombies/whos_who/forfeit
#
# @executed	at @s
#
# @within	mgs:v5.1.0/zombies/whos_who/bleed_out
#			mgs:v5.1.0/zombies/revive/on_down
#			mgs:v5.1.0/zombies/revive/full_death
#

scoreboard players operation #my_downed_id mgs.data = @s mgs.zb.ww.id
function mgs:v5.1.0/zombies/revive/hide_body
execute store result storage mgs:temp _ww_id.id int 1 run scoreboard players get @s mgs.zb.ww.id
function mgs:v5.1.0/zombies/whos_who/discard_snapshot with storage mgs:temp _ww_id
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
tag @s remove mgs.ww_active
scoreboard players set @s mgs.zb.ww.id 0
scoreboard players set @s mgs.zb.bleed 0
scoreboard players set @s mgs.zb.revive_p 0

