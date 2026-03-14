
#> mgs:v5.0.0/maps/editor/give_tools
#
# @within	mgs:v5.0.0/maps/editor/enter
#			mgs:v5.0.0/maps/editor/save_only
#

# Destroy egg (always in hotbar.8)
item replace entity @s hotbar.8 with minecraft:bat_spawn_egg[minecraft:item_name=[{"text":"✘ ","color":"dark_red","italic":false,"bold":true}, {"translate":"mgs.destroy"}],minecraft:item_model="minecraft:wither_skeleton_spawn_egg",minecraft:custom_data={mgs:{editor:true,type:"destroy"}},minecraft:entity_data={id:"minecraft:bat",NoAI:1b,Silent:1b,Invulnerable:1b,Tags:["mgs.new_element","mgs.element.destroy"]}]

# Utility eggs (bottom-right of inventory)
item replace entity @s inventory.26 with minecraft:bat_spawn_egg[minecraft:item_name=[{"text":"💾 ","color":"green","italic":false,"bold":true}, {"translate":"mgs.save_exit"}],minecraft:item_model="minecraft:turtle_spawn_egg",minecraft:custom_data={mgs:{editor:true,type:"editor_save_exit"}},minecraft:entity_data={id:"minecraft:bat",NoAI:1b,Silent:1b,Invulnerable:1b,Tags:["mgs.new_element","mgs.element.editor_save_exit"]}]
item replace entity @s inventory.25 with minecraft:bat_spawn_egg[minecraft:item_name=[{"text":"✘ ","color":"red","italic":false,"bold":true}, {"translate":"mgs.exit"}],minecraft:item_model="minecraft:ghast_spawn_egg",minecraft:custom_data={mgs:{editor:true,type:"editor_exit"}},minecraft:entity_data={id:"minecraft:bat",NoAI:1b,Silent:1b,Invulnerable:1b,Tags:["mgs.new_element","mgs.element.editor_exit"]}]
item replace entity @s inventory.24 with minecraft:bat_spawn_egg[minecraft:item_name=[{"text":"💾 ","color":"aqua","italic":false,"bold":true}, {"translate":"mgs.save"}],minecraft:item_model="minecraft:axolotl_spawn_egg",minecraft:custom_data={mgs:{editor:true,type:"editor_save"}},minecraft:entity_data={id:"minecraft:bat",NoAI:1b,Silent:1b,Invulnerable:1b,Tags:["mgs.new_element","mgs.element.editor_save"]}]

# Mode-specific eggs
execute if score @s mgs.mp.map_disp matches 0 run function mgs:v5.0.0/maps/editor/give_tools/multiplayer
execute if score @s mgs.mp.map_disp matches 1 run function mgs:v5.0.0/maps/editor/give_tools/zombies
execute if score @s mgs.mp.map_disp matches 2 run function mgs:v5.0.0/maps/editor/give_tools/missions

