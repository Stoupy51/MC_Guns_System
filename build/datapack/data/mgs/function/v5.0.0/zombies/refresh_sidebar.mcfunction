
#> mgs:v5.0.0/zombies/refresh_sidebar
#
# @within	mgs:v5.0.0/zombies/start_round
#			mgs:v5.0.0/zombies/game_tick
#			mgs:v5.0.0/zombies/create_sidebar
#

# Count alive zombies
execute store result score #_zb_alive mgs.data if entity @e[tag=mgs.zombie_round]
scoreboard players operation #_zb_total mgs.data = #_zb_alive mgs.data
scoreboard players operation #_zb_total mgs.data += #zb_to_spawn mgs.data

function #bs.sidebar:create {objective:"mgs.zb_sidebar",display_name:{text:"🧟 Zombies",color:"dark_green",bold:true},contents:[{translate: "mgs.round",extra:[{score:{name:"#zb_round",objective:"mgs.data"},color:"gold"}],color:"red"},{translate: "mgs.zombies",extra:[{score:{name:"#_zb_total",objective:"mgs.data"},color:"red"}],color:"gray"}," "]}

