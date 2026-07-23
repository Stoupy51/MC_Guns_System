
#> mgs:v5.1.0/zombies/perks/tombstone_collect
#
# @executed	as @a[distance=..2,gamemode=!spectator,scores={mgs.zb.in_game=1,mgs.zb.downed=0}]
#
# @within	mgs:v5.1.0/zombies/perks/tombstone_marker_tick [ as @a[distance=..2,gamemode=!spectator,scores={mgs.zb.in_game=1,mgs.zb.downed=0}] ]
#

# Restore perks (Tombstone excluded) and re-apply their effects silently
execute if score @s mgs.zb.tsp.juggernog matches 1 run scoreboard players set @s mgs.zb.perk.juggernog 1
execute if score @s mgs.zb.tsp.juggernog matches 1 run function mgs:v5.1.0/zombies/perks/reapply/juggernog
execute if score @s mgs.zb.tsp.speed_cola matches 1 run scoreboard players set @s mgs.zb.perk.speed_cola 1
execute if score @s mgs.zb.tsp.speed_cola matches 1 run function mgs:v5.1.0/zombies/perks/reapply/speed_cola
execute if score @s mgs.zb.tsp.double_tap matches 1 run scoreboard players set @s mgs.zb.perk.double_tap 1
execute if score @s mgs.zb.tsp.double_tap matches 1 run function mgs:v5.1.0/zombies/perks/reapply/double_tap
execute if score @s mgs.zb.tsp.quick_revive matches 1 run scoreboard players set @s mgs.zb.perk.quick_revive 1
execute if score @s mgs.zb.tsp.quick_revive matches 1 run function mgs:v5.1.0/zombies/perks/reapply/quick_revive
execute if score @s mgs.zb.tsp.mule_kick matches 1 run scoreboard players set @s mgs.zb.perk.mule_kick 1
execute if score @s mgs.zb.tsp.stamin_up matches 1 run scoreboard players set @s mgs.zb.perk.stamin_up 1
execute if score @s mgs.zb.tsp.stamin_up matches 1 run function mgs:v5.1.0/zombies/perks/reapply/stamin_up
execute if score @s mgs.zb.tsp.phd_flopper matches 1 run scoreboard players set @s mgs.zb.perk.phd_flopper 1
execute if score @s mgs.zb.tsp.phd_flopper matches 1 run function mgs:v5.1.0/zombies/perks/reapply/phd_flopper
execute if score @s mgs.zb.tsp.deadshot matches 1 run scoreboard players set @s mgs.zb.perk.deadshot 1
execute if score @s mgs.zb.tsp.deadshot matches 1 run function mgs:v5.1.0/zombies/perks/reapply/deadshot
execute if score @s mgs.zb.tsp.timeslip matches 1 run scoreboard players set @s mgs.zb.perk.timeslip 1
execute if score @s mgs.zb.tsp.timeslip matches 1 run function mgs:v5.1.0/zombies/perks/reapply/timeslip
execute if score @s mgs.zb.tsp.electric_cherry matches 1 run scoreboard players set @s mgs.zb.perk.electric_cherry 1
execute if score @s mgs.zb.tsp.electric_cherry matches 1 run function mgs:v5.1.0/zombies/perks/reapply/electric_cherry
execute if score @s mgs.zb.tsp.whos_who matches 1 run scoreboard players set @s mgs.zb.perk.whos_who 1
execute if score @s mgs.zb.tsp.dying_wish matches 1 run scoreboard players set @s mgs.zb.perk.dying_wish 1
execute if score @s mgs.zb.tsp.widows_wine matches 1 run scoreboard players set @s mgs.zb.perk.widows_wine 1
execute if score @s mgs.zb.tsp.widows_wine matches 1 run function mgs:v5.1.0/zombies/perks/reapply/widows_wine

# Restore max health for the restored Juggernog state
execute if score @s mgs.zb.perk.juggernog matches 1.. run attribute @s minecraft:max_health base set 40

# Restore the snapshotted inventory (weapons/mags/grenades) into the exact original slots via the
# shared restore system (players can't be data-modified), then drop the snapshot
execute store result storage mgs:temp _ts_id.id int 1 run scoreboard players get @s mgs.zb.downed_id
function mgs:v5.1.0/zombies/perks/tombstone_load_snapshot with storage mgs:temp _ts_id
function mgs:v5.1.0/zombies/inventory/restore_inventory

# Rebuild the perk display items now that ownership is restored
function mgs:v5.1.0/zombies/inventory/refresh_perk_items

# Clear the snapshot scores and despawn the marker (id-matched)
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
scoreboard players operation #my_downed_id mgs.data = @s mgs.zb.downed_id
kill @e[tag=mgs.tombstone,predicate=mgs:v5.1.0/zombies/revive/downed_id_match]

# Feedback
title @s times 5 40 15
title @s title ["🪦"]
title @s subtitle [{"translate":"mgs.gear_recovered","color":"green"}]
playsound minecraft:block.respawn_anchor.charge player @a[distance=..24] ~ ~ ~ 1 1.2
tellraw @a[scores={mgs.zb.in_game=1}] [[{"text":"","color":"gold"},"[",{"translate":"mgs"},"] "],{"selector":"@s","color":"green"},{"translate":"mgs.recovered_their_gear_from_a_tombstone","color":"gray"}]

