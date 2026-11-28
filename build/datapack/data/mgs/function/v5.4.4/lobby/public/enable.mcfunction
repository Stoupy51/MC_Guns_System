
#> mgs:v5.4.4/lobby/public/enable
#
# @within	mgs:v5.4.4/dialog/close_then
#			dialog mgs:v5.4.4/config/global
#

execute unless data storage mgs:config lobby.dimension run return run tellraw @s [[{"text":"","color":"gold"},"[",{"translate":"mgs","fallback":"MGS"},"] "],{"translate":"mgs.set_the_lobby_first_with_set_lobby_here","fallback":"Set the lobby first, with Set Lobby Here.","color":"red"}]
scoreboard players set #public_lobby mgs.config 1
scoreboard players operation @a mgs.lobby.seen = #now mgs.lobby.seen
tellraw @s [[{"text":"","color":"gold"},"[",{"translate":"mgs","fallback":"MGS"},"] "],{"translate":"mgs.public_lobby_on_players_join_a_mode_from_the_menu_or_the_chat_vo","fallback":"Public lobby on: players join a mode from the menu or the chat, vote and play with no operator.","color":"green"}]

