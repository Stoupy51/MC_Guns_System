
#> mgs:v5.4.2/maps/editor/remove_duplicates
#
# @within	mgs:v5.4.2/dialog/close_then
#			mgs:v5.4.2/maps/editor/do_save
#

execute as @e[type=minecraft:marker,tag=mgs.element.red_spawn] at @s run function mgs:v5.4.2/maps/editor/dedupe/red_spawn
execute as @e[type=minecraft:marker,tag=mgs.element.blue_spawn] at @s run function mgs:v5.4.2/maps/editor/dedupe/blue_spawn
execute as @e[type=minecraft:marker,tag=mgs.element.general_spawn] at @s run function mgs:v5.4.2/maps/editor/dedupe/general_spawn
execute as @e[type=minecraft:marker,tag=mgs.element.out_of_bounds] at @s run function mgs:v5.4.2/maps/editor/dedupe/out_of_bounds
execute as @e[type=minecraft:marker,tag=mgs.element.boundary] at @s run function mgs:v5.4.2/maps/editor/dedupe/boundary
execute as @e[type=minecraft:marker,tag=mgs.element.search_and_destroy] at @s run function mgs:v5.4.2/maps/editor/dedupe/search_and_destroy
execute as @e[type=minecraft:marker,tag=mgs.element.domination] at @s run function mgs:v5.4.2/maps/editor/dedupe/domination
execute as @e[type=minecraft:marker,tag=mgs.element.hardpoint] at @s run function mgs:v5.4.2/maps/editor/dedupe/hardpoint
execute as @e[type=minecraft:marker,tag=mgs.element.start_command] at @s run function mgs:v5.4.2/maps/editor/dedupe/start_command
execute as @e[type=minecraft:marker,tag=mgs.element.respawn_command] at @s run function mgs:v5.4.2/maps/editor/dedupe/respawn_command
execute as @e[type=minecraft:marker,tag=mgs.element.mission_spawn] at @s run function mgs:v5.4.2/maps/editor/dedupe/mission_spawn
execute as @e[type=minecraft:marker,tag=mgs.element.enemy] at @s run function mgs:v5.4.2/maps/editor/dedupe/enemy
execute as @e[type=minecraft:marker,tag=mgs.element.zombie_spawn] at @s run function mgs:v5.4.2/maps/editor/dedupe/zombie_spawn
execute as @e[type=minecraft:marker,tag=mgs.element.player_spawn_zb] at @s run function mgs:v5.4.2/maps/editor/dedupe/player_spawn_zb
execute as @e[type=minecraft:marker,tag=mgs.element.special_spawn] at @s run function mgs:v5.4.2/maps/editor/dedupe/special_spawn
execute as @e[type=minecraft:marker,tag=mgs.element.wallbuy] at @s run function mgs:v5.4.2/maps/editor/dedupe/wallbuy
execute as @e[type=minecraft:marker,tag=mgs.element.door] at @s run function mgs:v5.4.2/maps/editor/dedupe/door
execute as @e[type=minecraft:marker,tag=mgs.element.trap] at @s run function mgs:v5.4.2/maps/editor/dedupe/trap
execute as @e[type=minecraft:marker,tag=mgs.element.perk_machine] at @s run function mgs:v5.4.2/maps/editor/dedupe/perk_machine
execute as @e[type=minecraft:marker,tag=mgs.element.wunderfizz] at @s run function mgs:v5.4.2/maps/editor/dedupe/wunderfizz
execute as @e[type=minecraft:marker,tag=mgs.element.pap_machine] at @s run function mgs:v5.4.2/maps/editor/dedupe/pap_machine
execute as @e[type=minecraft:marker,tag=mgs.element.mystery_box_pos] at @s run function mgs:v5.4.2/maps/editor/dedupe/mystery_box_pos
execute as @e[type=minecraft:marker,tag=mgs.element.power_switch] at @s run function mgs:v5.4.2/maps/editor/dedupe/power_switch
execute as @e[type=minecraft:marker,tag=mgs.element.barricade] at @s run function mgs:v5.4.2/maps/editor/dedupe/barricade
tag @e[type=minecraft:marker,tag=mgs.ed_keep] remove mgs.ed_keep
execute store result score #ed_dups mgs.data run kill @e[type=minecraft:marker,tag=mgs.ed_dup]
execute if score #ed_dups mgs.data matches 1.. run tellraw @a[tag=mgs.map_editor] [[{"text":"","color":"gold"},"[",{"translate":"mgs","fallback":"MGS"},"] "],{"score":{"name":"#ed_dups","objective":"mgs.data"},"color":"white"},{"translate":"mgs.duplicate_elements_removed_same_kind_block_and_values","fallback":" duplicate elements removed (same kind, block and values).","color":"yellow"}]

