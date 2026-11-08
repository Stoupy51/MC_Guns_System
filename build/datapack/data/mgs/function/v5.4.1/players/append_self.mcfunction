
#> mgs:v5.4.1/players/append_self
#
# @within	mgs:v5.4.1/dialog/close_then
#			mgs:v5.4.1/players/list_multiplayer [ as @a ]
#			mgs:v5.4.1/players/list_zombies [ as @a ]
#			mgs:v5.4.1/players/list_missions [ as @a ]
#			mgs:v5.4.1/maps/editor/invite [ as @a ]
#

data modify storage mgs:temp _plr_entry set value {color:"gray",name:"???"}
execute store result storage mgs:temp _plr_entry.id int 1 run scoreboard players get @s bs.id
execute if data storage mgs:temp {_plr_mode:"multiplayer"} if score @s mgs.mp.team matches 1 run data modify storage mgs:temp _plr_entry.color set value "red"
execute if data storage mgs:temp {_plr_mode:"multiplayer"} if score @s mgs.mp.team matches 2 run data modify storage mgs:temp _plr_entry.color set value "blue"
execute if data storage mgs:temp {_plr_mode:"zombies"} if score @s mgs.zb.in_game matches 1 run data modify storage mgs:temp _plr_entry.color set value "green"
execute if data storage mgs:temp {_plr_mode:"missions"} if score @s mgs.mi.in_game matches 1 run data modify storage mgs:temp _plr_entry.color set value "green"

function mgs:v5.4.1/players/read_name
data modify storage mgs:temp _plr_entry.name set from storage mgs:temp _name

data modify storage mgs:temp _plr_iter append from storage mgs:temp _plr_entry

