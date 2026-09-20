
#> mgs:v5.1.0/zombies/perks/tombstone_on_down
#
# @executed	as @e[type=player,sort=random] & at @s
#
# @within	mgs:v5.1.0/zombies/revive/on_down
#

# Tombstone is disabled solo (a solo bleed-out is game over — nothing to recover to)
execute store result score #ts_ingame mgs.data if entity @a[scores={mgs.zb.in_game=1}]
execute if score #ts_ingame mgs.data matches ..1 run return 0

# Snapshot which perks the owner had (restored on recovery)
scoreboard players operation @s mgs.zb.tsp.juggernog = @s mgs.zb.perk.juggernog
scoreboard players operation @s mgs.zb.tsp.speed_cola = @s mgs.zb.perk.speed_cola
scoreboard players operation @s mgs.zb.tsp.double_tap = @s mgs.zb.perk.double_tap
execute store success score @s mgs.zb.tsp.quick_revive if entity @s[tag=mgs.perk.quick_revive]
scoreboard players operation @s mgs.zb.tsp.mule_kick = @s mgs.zb.perk.mule_kick
scoreboard players operation @s mgs.zb.tsp.stamin_up = @s mgs.zb.perk.stamin_up
scoreboard players operation @s mgs.zb.tsp.phd_flopper = @s mgs.zb.perk.phd_flopper
scoreboard players operation @s mgs.zb.tsp.deadshot = @s mgs.zb.perk.deadshot
scoreboard players operation @s mgs.zb.tsp.timeslip = @s mgs.zb.perk.timeslip
scoreboard players operation @s mgs.zb.tsp.electric_cherry = @s mgs.zb.perk.electric_cherry
scoreboard players operation @s mgs.zb.tsp.tombstone = @s mgs.zb.perk.tombstone
scoreboard players operation @s mgs.zb.tsp.whos_who = @s mgs.zb.perk.whos_who
scoreboard players operation @s mgs.zb.tsp.dying_wish = @s mgs.zb.perk.dying_wish
scoreboard players operation @s mgs.zb.tsp.widows_wine = @s mgs.zb.perk.widows_wine

# Spawn the tombstone marker at the player, tag it with the owner's downed_id, then move to death spot
summon minecraft:item_display ~ ~ ~ {Tags:["mgs.tombstone","mgs.tombstone_new","mgs.gm_entity"],Glowing:true,billboard:"vertical",teleport_duration:1,item:{id:"minecraft:skeleton_skull",count:1},item_display:"ground",transformation:{left_rotation:[0f,0f,0f,1f],right_rotation:[0f,0f,0f,1f],translation:[0f,0.3f,0f],scale:[1.2f,1.2f,1.2f]}}
scoreboard players operation @n[tag=mgs.tombstone_new] mgs.zb.downed_id = @s mgs.zb.downed_id
scoreboard players set @n[tag=mgs.tombstone_new] mgs.zb.ts.state 0
scoreboard players set @n[tag=mgs.tombstone_new] mgs.zb.ts.timer 0
function mgs:v5.1.0/zombies/perks/tombstone_tp with storage mgs:temp
tag @e[tag=mgs.tombstone_new] remove mgs.tombstone_new

