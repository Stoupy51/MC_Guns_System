
#> mgs:v5.1.0/zombies/perks/tombstone_on_revived
#
# @executed	at @s
#
# @within	mgs:v5.1.0/zombies/revive/revive_complete
#

kill @e[tag=mgs.tombstone,predicate=mgs:v5.1.0/zombies/revive/downed_id_match]
scoreboard players set @s mgs.zb.tsp.juggernog 0
scoreboard players set @s mgs.zb.tsp.speed_cola 0
scoreboard players set @s mgs.zb.tsp.double_tap 0
scoreboard players set @s mgs.zb.tsp.quick_revive 0
scoreboard players set @s mgs.zb.tsp.mule_kick 0
scoreboard players set @s mgs.zb.tsp.stamin_up 0
scoreboard players set @s mgs.zb.tsp.phd_flopper 0
scoreboard players set @s mgs.zb.tsp.deadshot 0
scoreboard players set @s mgs.zb.tsp.timeslip 0
scoreboard players set @s mgs.zb.tsp.electric_cherry 0
scoreboard players set @s mgs.zb.tsp.tombstone 0
scoreboard players set @s mgs.zb.tsp.whos_who 0
scoreboard players set @s mgs.zb.tsp.dying_wish 0
scoreboard players set @s mgs.zb.tsp.widows_wine 0

