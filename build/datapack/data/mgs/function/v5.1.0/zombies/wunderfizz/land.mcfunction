
#> mgs:v5.1.0/zombies/wunderfizz/land
#
# @executed	as @e[type=item_display,tag=mgs.wunderfizz_orb] & at @s
#
# @within	mgs:v5.1.0/zombies/wunderfizz/orb_tick
#

# Roam pull: the machine is about to move — show the bear, refund the buyer, no perk
execute if score @s mgs.zb.wf.willmove matches 1 run return run function mgs:v5.1.0/zombies/wunderfizz/land_bear

execute if score @s mgs.zb.wf.perk matches 0 run data modify entity @s item set value {id:"minecraft:potion",count:1,components:{"minecraft:item_model":"mgs:perk_machine_juggernog"}}
execute if score @s mgs.zb.wf.perk matches 1 run data modify entity @s item set value {id:"minecraft:potion",count:1,components:{"minecraft:item_model":"mgs:perk_machine_speed_cola"}}
execute if score @s mgs.zb.wf.perk matches 2 run data modify entity @s item set value {id:"minecraft:potion",count:1,components:{"minecraft:item_model":"mgs:perk_machine_double_tap"}}
execute if score @s mgs.zb.wf.perk matches 3 run data modify entity @s item set value {id:"minecraft:potion",count:1,components:{"minecraft:item_model":"mgs:perk_machine_quick_revive"}}
execute if score @s mgs.zb.wf.perk matches 4 run data modify entity @s item set value {id:"minecraft:potion",count:1,components:{"minecraft:item_model":"mgs:perk_machine_mule_kick"}}
execute if score @s mgs.zb.wf.perk matches 5 run data modify entity @s item set value {id:"minecraft:potion",count:1,components:{"minecraft:item_model":"mgs:perk_machine_stamin_up"}}
execute if score @s mgs.zb.wf.perk matches 6 run data modify entity @s item set value {id:"minecraft:potion",count:1,components:{"minecraft:item_model":"mgs:perk_machine_phd_flopper"}}
execute if score @s mgs.zb.wf.perk matches 7 run data modify entity @s item set value {id:"minecraft:potion",count:1,components:{"minecraft:item_model":"mgs:perk_machine_deadshot"}}
execute if score @s mgs.zb.wf.perk matches 8 run data modify entity @s item set value {id:"minecraft:potion",count:1,components:{"minecraft:item_model":"mgs:perk_machine_timeslip"}}
execute if score @s mgs.zb.wf.perk matches 9 run data modify entity @s item set value {id:"minecraft:potion",count:1,components:{"minecraft:item_model":"mgs:perk_machine_electric_cherry"}}
execute if score @s mgs.zb.wf.perk matches 10 run data modify entity @s item set value {id:"minecraft:potion",count:1,components:{"minecraft:item_model":"mgs:perk_machine_tombstone"}}
execute if score @s mgs.zb.wf.perk matches 11 run data modify entity @s item set value {id:"minecraft:potion",count:1,components:{"minecraft:item_model":"mgs:perk_machine_whos_who"}}
execute if score @s mgs.zb.wf.perk matches 12 run data modify entity @s item set value {id:"minecraft:potion",count:1,components:{"minecraft:item_model":"mgs:perk_machine_dying_wish"}}
execute if score @s mgs.zb.wf.perk matches 13 run data modify entity @s item set value {id:"minecraft:potion",count:1,components:{"minecraft:item_model":"mgs:perk_machine_widows_wine"}}
particle minecraft:totem_of_undying ~ ~ ~ 0.3 0.4 0.3 0.2 10 force @a[distance=..48]
particle minecraft:electric_spark ~ ~ ~ 0.4 0.5 0.4 0.15 10 force @a[distance=..48]
playsound minecraft:block.beacon.deactivate ambient @a[scores={mgs.zb.in_game=1}] ~ ~ ~ 0.8 1.4
playsound minecraft:entity.lightning_bolt.impact ambient @a[scores={mgs.zb.in_game=1}] ~ ~ ~ 0.5 1.7
playsound minecraft:block.note_block.bit ambient @a[scores={mgs.zb.in_game=1}] ~ ~ ~ 0.6 0.9
scoreboard players operation #wf_b mgs.data = @s mgs.zb.wf.buyer
execute as @a[scores={mgs.zb.in_game=1}] if score @s mgs.zb.wf_pid = #wf_b mgs.data run tellraw @s [[{"text":"","color":"gold"},"[",{"translate":"mgs"},"] "],{"translate":"mgs.perk_ready","color":"gold"},{"translate":"mgs.right_click_der_wunderfizz_to_collect","color":"green","bold":true}]

