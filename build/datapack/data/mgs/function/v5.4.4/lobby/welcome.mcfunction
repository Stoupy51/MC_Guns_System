
#> mgs:v5.4.4/lobby/welcome
#
# @within	mgs:v5.4.4/dialog/close_then
#			mgs:v5.4.4/lobby/arrive
#

tellraw @s ["",[{"text":"","color":"gold"},"[",{"translate":"mgs","fallback":"MGS"},"] "],{"translate":"mgs.play","fallback":"Play: ","color":"gray"},{"text":"","color":"red","click_event":{"action":"run_command","command":"/trigger mgs.player.config set 1651"},"hover_event":{"action":"show_text","value":"Join the Multiplayer queue"},"extra":["[⚔ ",{"translate":"mgs.multiplayer","fallback":"Multiplayer"}," ",{"score":{"name":"#lv_mp_count","objective":"mgs.data"}},"]"]}," ",{"text":"","color":"dark_green","click_event":{"action":"run_command","command":"/trigger mgs.player.config set 1652"},"hover_event":{"action":"show_text","value":"Join the Zombies queue"},"extra":["[🧟 ",{"translate":"mgs.zombies","fallback":"Zombies"}," ",{"score":{"name":"#lv_zb_count","objective":"mgs.data"}},"]"]}," ",{"text":"","color":"gold","click_event":{"action":"run_command","command":"/trigger mgs.player.config set 1653"},"hover_event":{"action":"show_text","value":"Join the Missions queue"},"extra":["[🎯 ",{"translate":"mgs.missions","fallback":"Missions"}," ",{"score":{"name":"#lv_mi_count","objective":"mgs.data"}},"]"]}]
execute if score @s mgs.lobby.queue matches 1.. run tellraw @s ["",[{"text":"","color":"gold"},"[",{"translate":"mgs","fallback":"MGS"},"] "],{"translate":"mgs.you_stay_in_your_queue_for_the_next_game","fallback":"You stay in your queue for the next game. ","color":"gray"},{"text":"","color":"yellow","click_event":{"action":"run_command","command":"/trigger mgs.player.config set 1650"},"extra":["[🏠 ",{"translate":"mgs.leave_the_queue","fallback":"Leave the queue"},"]"]}]
tellraw @s ["",[{"text":"","color":"gold"},"[",{"translate":"mgs","fallback":"MGS"},"] "],{"translate":"mgs.menu_class_and_stats","fallback":"Menu, class and stats: ","color":"gray"},{"keybind":"key.quickActions","color":"yellow"}]

