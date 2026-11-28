
#> mgs:v5.4.4/lobby/controls/place
#
# @within	mgs:v5.4.4/dialog/close_then
#			dialog mgs:v5.4.4/config/global
#

kill @e[type=minecraft:text_display,tag=mgs.lobby_controls]
summon minecraft:text_display ~ ~1.5 ~ {Tags:["mgs.lobby_controls"],billboard:"vertical",alignment:"left",line_width:400,text:["",{"translate":"mgs.controls","fallback":"Controls","color":"gold","bold":true},"\n",{"keybind":"key.use","color":"yellow"},"  ",{"translate":"mgs.shoot_throw_a_grenade","fallback":"Shoot, throw a grenade","color":"white"},"\n",{"keybind":"key.sneak","color":"yellow"},"  ",{"translate":"mgs.aim_down_sights","fallback":"Aim down sights","color":"white"},"\n",{"keybind":"key.attack","color":"yellow"},{"text":" or ","color":"gray"},{"keybind":"key.swapOffhand","color":"yellow"},"  ",{"translate":"mgs.reload","fallback":"Reload","color":"white"},"\n",{"keybind":"key.drop","color":"yellow"},"  ",{"translate":"mgs.switch_fire_mode","fallback":"Switch fire mode","color":"white"},"\n",{"keybind":"key.sprint","color":"yellow"},"  ",{"translate":"mgs.sprint_it_uses_stamina","fallback":"Sprint, it uses stamina","color":"white"},"\n",{"keybind":"key.sneak","color":"yellow"},"  ",{"translate":"mgs.plant_or_defuse_at_a_bomb_site","fallback":"Plant or defuse at a bomb site","color":"white"},"\n",{"keybind":"key.use","color":"yellow"},"  ",{"translate":"mgs.buy_at_a_wall_weapon_or_a_machine_zombies","fallback":"Buy at a wall weapon or a machine (Zombies)","color":"white"},"\n",{"keybind":"key.sneak","color":"yellow"},"  ",{"translate":"mgs.repair_a_barricade_zombies","fallback":"Repair a barricade (Zombies)","color":"white"},"\n",{"keybind":"key.quickActions","color":"yellow"},"  ",{"translate":"mgs.menu_play_class_stats","fallback":"Menu: play, class, stats","color":"white"}]}
tellraw @s [[{"text":"","color":"gold"},"[",{"translate":"mgs","fallback":"MGS"},"] "],{"translate":"mgs.controls_display_placed_where_you_stand","fallback":"Controls display placed where you stand.","color":"green"}]

