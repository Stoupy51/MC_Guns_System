
#> mgs:v5.1.0/zombies/refresh_sidebar
#
# @within	mgs:v5.1.0/zombies/game_tick
#			mgs:v5.1.0/zombies/create_sidebar
#			mgs:v5.1.0/zombies/start_round
#

# game_tick recomputes #zb_alive every tick.
scoreboard players operation #zb_total mgs.data = #zb_alive mgs.data
scoreboard players operation #zb_total mgs.data += #zb_to_spawn mgs.data
execute if score #zb_total mgs.data matches ..-1 run scoreboard players set #zb_total mgs.data 0

data modify storage mgs:temp zb_sb set value [[{translate:"mgs.round",color:"red"},{score:{name:"#zb_round",objective:"mgs.data"},color:"gold"}],[{translate:"mgs.zombies",color:"red"},{score:{name:"#zb_total",objective:"mgs.data"},color:"gold"}]," "]

scoreboard players set @a mgs.zb.sb_rank 0
tag @a remove mgs.zb_sb_cand
tag @a[scores={mgs.zb.in_game=1}] add mgs.zb_sb_cand
function mgs:v5.1.0/zombies/sidebar_rank_players

function mgs:v5.1.0/zombies/build_sidebar with storage mgs:temp

