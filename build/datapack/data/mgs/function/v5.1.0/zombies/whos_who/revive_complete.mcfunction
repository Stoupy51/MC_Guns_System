
#> mgs:v5.1.0/zombies/whos_who/revive_complete
#
# @executed	at @s
#
# @within	mgs:v5.1.0/zombies/whos_who/owner_tick
#

execute if score @s mgs.zb.wwp.juggernog matches 1 run scoreboard players set @s mgs.zb.perk.juggernog 1
execute if score @s mgs.zb.wwp.juggernog matches 1 run function mgs:v5.1.0/zombies/perks/reapply/juggernog
execute if score @s mgs.zb.wwp.speed_cola matches 1 run scoreboard players set @s mgs.zb.perk.speed_cola 1
execute if score @s mgs.zb.wwp.speed_cola matches 1 run function mgs:v5.1.0/zombies/perks/reapply/speed_cola
execute if score @s mgs.zb.wwp.double_tap matches 1 run scoreboard players set @s mgs.zb.perk.double_tap 1
execute if score @s mgs.zb.wwp.double_tap matches 1 run function mgs:v5.1.0/zombies/perks/reapply/double_tap
execute if score @s mgs.zb.wwp.quick_revive matches 1 run scoreboard players set @s mgs.zb.perk.quick_revive 1
execute if score @s mgs.zb.wwp.quick_revive matches 1 run function mgs:v5.1.0/zombies/perks/reapply/quick_revive
execute if score @s mgs.zb.wwp.mule_kick matches 1 run scoreboard players set @s mgs.zb.perk.mule_kick 1
execute if score @s mgs.zb.wwp.stamin_up matches 1 run scoreboard players set @s mgs.zb.perk.stamin_up 1
execute if score @s mgs.zb.wwp.stamin_up matches 1 run function mgs:v5.1.0/zombies/perks/reapply/stamin_up
execute if score @s mgs.zb.wwp.phd_flopper matches 1 run scoreboard players set @s mgs.zb.perk.phd_flopper 1
execute if score @s mgs.zb.wwp.phd_flopper matches 1 run function mgs:v5.1.0/zombies/perks/reapply/phd_flopper
execute if score @s mgs.zb.wwp.deadshot matches 1 run scoreboard players set @s mgs.zb.perk.deadshot 1
execute if score @s mgs.zb.wwp.deadshot matches 1 run function mgs:v5.1.0/zombies/perks/reapply/deadshot
execute if score @s mgs.zb.wwp.timeslip matches 1 run scoreboard players set @s mgs.zb.perk.timeslip 1
execute if score @s mgs.zb.wwp.timeslip matches 1 run function mgs:v5.1.0/zombies/perks/reapply/timeslip
execute if score @s mgs.zb.wwp.electric_cherry matches 1 run scoreboard players set @s mgs.zb.perk.electric_cherry 1
execute if score @s mgs.zb.wwp.electric_cherry matches 1 run function mgs:v5.1.0/zombies/perks/reapply/electric_cherry
execute if score @s mgs.zb.wwp.tombstone matches 1 run scoreboard players set @s mgs.zb.perk.tombstone 1
execute if score @s mgs.zb.wwp.dying_wish matches 1 run scoreboard players set @s mgs.zb.perk.dying_wish 1
execute if score @s mgs.zb.wwp.widows_wine matches 1 run scoreboard players set @s mgs.zb.perk.widows_wine 1
execute if score @s mgs.zb.wwp.widows_wine matches 1 run function mgs:v5.1.0/zombies/perks/reapply/widows_wine
execute if score @s mgs.zb.perk.juggernog matches 1.. run attribute @s minecraft:max_health base set 40

# Restore the snapshotted inventory into the exact original slots (players can't be data-modified,
# so this goes through the shared inventory/restore_inventory system)
execute store result storage mgs:temp _ww_id.id int 1 run scoreboard players get @s mgs.zb.ww.id
function mgs:v5.1.0/zombies/whos_who/load_snapshot with storage mgs:temp _ww_id
function mgs:v5.1.0/zombies/inventory/restore_inventory
function mgs:v5.1.0/zombies/inventory/refresh_perk_items
effect give @s minecraft:instant_health 1 255 true

# Remove the body and clear doppelganger state + snapshot
scoreboard players operation #my_downed_id mgs.data = @s mgs.zb.ww.id
function mgs:v5.1.0/zombies/revive/hide_body
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

title @s times 5 40 15
title @s title ["❤"]
title @s subtitle [{"translate":"mgs.body_revived_you_are_whole_again","color":"green"}]
tellraw @a[scores={mgs.zb.in_game=1}] [[{"text":"","color":"gold"},"[",{"translate":"mgs"},"] "],{"selector":"@s","color":"green"},{"translate":"mgs.s_body_was_revived_they_are_whole_again","color":"gray"}]
function mgs:v5.1.0/zombies/feedback/sound_success

