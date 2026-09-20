
#> mgs:v5.1.0/zombies/wunderfizz/spin_cycle
#
# @executed	as @e[type=item_display,tag=mgs.wunderfizz_orb] & at @s
#
# @within	mgs:v5.1.0/zombies/wunderfizz/orb_tick
#

scoreboard players operation #wf_mod mgs.data = @s mgs.zb.wf.anim
scoreboard players operation #wf_mod mgs.data %= #3 mgs.data
execute unless score #wf_mod mgs.data matches 0 run return 0
execute store result score #wf_roll mgs.data run random value 0..13
execute if score #wf_roll mgs.data matches 0 run data modify entity @s item set value {id:"minecraft:potion",count:1,components:{"minecraft:item_model":"mgs:perk_machine_juggernog"}}
execute if score #wf_roll mgs.data matches 1 run data modify entity @s item set value {id:"minecraft:potion",count:1,components:{"minecraft:item_model":"mgs:perk_machine_speed_cola"}}
execute if score #wf_roll mgs.data matches 2 run data modify entity @s item set value {id:"minecraft:potion",count:1,components:{"minecraft:item_model":"mgs:perk_machine_double_tap"}}
execute if score #wf_roll mgs.data matches 3 run data modify entity @s item set value {id:"minecraft:potion",count:1,components:{"minecraft:item_model":"mgs:perk_machine_quick_revive"}}
execute if score #wf_roll mgs.data matches 4 run data modify entity @s item set value {id:"minecraft:potion",count:1,components:{"minecraft:item_model":"mgs:perk_machine_mule_kick"}}
execute if score #wf_roll mgs.data matches 5 run data modify entity @s item set value {id:"minecraft:potion",count:1,components:{"minecraft:item_model":"mgs:perk_machine_stamin_up"}}
execute if score #wf_roll mgs.data matches 6 run data modify entity @s item set value {id:"minecraft:potion",count:1,components:{"minecraft:item_model":"mgs:perk_machine_phd_flopper"}}
execute if score #wf_roll mgs.data matches 7 run data modify entity @s item set value {id:"minecraft:potion",count:1,components:{"minecraft:item_model":"mgs:perk_machine_deadshot"}}
execute if score #wf_roll mgs.data matches 8 run data modify entity @s item set value {id:"minecraft:potion",count:1,components:{"minecraft:item_model":"mgs:perk_machine_timeslip"}}
execute if score #wf_roll mgs.data matches 9 run data modify entity @s item set value {id:"minecraft:potion",count:1,components:{"minecraft:item_model":"mgs:perk_machine_electric_cherry"}}
execute if score #wf_roll mgs.data matches 10 run data modify entity @s item set value {id:"minecraft:potion",count:1,components:{"minecraft:item_model":"mgs:perk_machine_tombstone"}}
execute if score #wf_roll mgs.data matches 11 run data modify entity @s item set value {id:"minecraft:potion",count:1,components:{"minecraft:item_model":"mgs:perk_machine_whos_who"}}
execute if score #wf_roll mgs.data matches 12 run data modify entity @s item set value {id:"minecraft:potion",count:1,components:{"minecraft:item_model":"mgs:perk_machine_dying_wish"}}
execute if score #wf_roll mgs.data matches 13 run data modify entity @s item set value {id:"minecraft:potion",count:1,components:{"minecraft:item_model":"mgs:perk_machine_widows_wine"}}
# Electric spin feedback (vanilla sounds): a spark + a short conduit zap each cycle
particle minecraft:electric_spark ~ ~ ~ 0.25 0.3 0.25 0.05 3 force @a[distance=..32]
playsound minecraft:block.conduit.ambient.short ambient @a[scores={mgs.zb.in_game=1}] ~ ~ ~ 0.5 1.4

