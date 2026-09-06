
#> mgs:v5.1.0/zombies/powerups/check_pap_taker
#
# @executed	as @p[scores={mgs.zb.in_game=1},gamemode=!spectator,distance=..1.5]
#
# @within	mgs:v5.1.0/zombies/powerups/do_pickup [ as @p[scores={mgs.zb.in_game=1},gamemode=!spectator,distance=..1.5] ]
#

execute store result score #pu_pap_sel mgs.data run data get entity @s SelectedItemSlot
execute if score #pu_pap_sel mgs.data matches 1 if items entity @s hotbar.1 *[custom_data~{mgs:{gun:true}}] run scoreboard players set #pu_pap_ok mgs.data 1
execute if score #pu_pap_sel mgs.data matches 2 if items entity @s hotbar.2 *[custom_data~{mgs:{gun:true}}] run scoreboard players set #pu_pap_ok mgs.data 1
execute if score #pu_pap_sel mgs.data matches 3 if items entity @s hotbar.3 *[custom_data~{mgs:{gun:true}}] run scoreboard players set #pu_pap_ok mgs.data 1
execute if score #pu_pap_ok mgs.data matches 0 run data modify storage smithed.actionbar:input message set value {json:["✦ ",{"translate":"mgs.free_pack_a_punch","color":"aqua"},{"text":" - ","color":"gray"},{"translate":"mgs.hold_a_weapon_to_take_it","color":"red"}],priority:"conditional",freeze:5}
execute if score #pu_pap_ok mgs.data matches 0 run function #smithed.actionbar:message

## sourceMappingURL=check_pap_taker.mcfunction.map
