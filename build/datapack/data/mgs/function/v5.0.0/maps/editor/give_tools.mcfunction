
#> mgs:v5.0.0/maps/editor/give_tools
#
# @within	mgs:v5.0.0/maps/editor/enter
#			mgs:v5.0.0/maps/editor/cycle_mode
#

# Destroy egg (always in hotbar.8)
item replace entity @s hotbar.8 with minecraft:bat_spawn_egg[minecraft:item_name={"translate": "mgs.destroy","color":"dark_red","italic":false,"bold":true},minecraft:item_model="minecraft:wither_skeleton_spawn_egg",minecraft:custom_data={mgs:{editor:true,type:"destroy"}},minecraft:entity_data={id:"minecraft:bat",NoAI:1b,Silent:1b,Invulnerable:1b,Tags:["mgs.new_element","mgs.element.destroy"]}]

# Mode switcher (always in hotbar.7)
item replace entity @s hotbar.7 with minecraft:warped_fungus_on_a_stick[minecraft:item_name={"translate": "mgs.switch_mode","color":"white","italic":false},minecraft:custom_data={mgs:{mode_switcher:true}}]

# Mode-specific eggs
execute if score @s mgs.mp.map_disp matches 0 run function mgs:v5.0.0/maps/editor/give_tools/multiplayer
execute if score @s mgs.mp.map_disp matches 1 run function mgs:v5.0.0/maps/editor/give_tools/zombies
execute if score @s mgs.mp.map_disp matches 2 run function mgs:v5.0.0/maps/editor/give_tools/missions

