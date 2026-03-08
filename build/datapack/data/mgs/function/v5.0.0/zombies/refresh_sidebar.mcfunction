
#> mgs:v5.0.0/zombies/refresh_sidebar
#
# @within	mgs:v5.0.0/zombies/game_tick
#			mgs:v5.0.0/zombies/start_round
#			mgs:v5.0.0/zombies/create_sidebar
#

# Count alive zombies
execute store result score #_zb_alive mgs.data if entity @e[tag=mgs.zombie_round]
scoreboard players operation #_zb_total mgs.data = #_zb_alive mgs.data
scoreboard players operation #_zb_total mgs.data += #zb_to_spawn mgs.data
execute if score #_zb_total mgs.data matches ..-1 run scoreboard players set #_zb_total mgs.data 0

# Initialize sidebar contents
data modify storage mgs:temp zb_sb set value [{translate: "mgs.round",extra:[{score:{name:"#zb_round",objective:"mgs.data"},color:"gold"}],color:"red"},{translate: "mgs.zombies",extra:[{score:{name:"#_zb_total",objective:"mgs.data"},color:"red"}],color:"gray"}," "]

# Rank players for sidebar display
scoreboard players set @a mgs.zb.sb_rank 0
tag @a[scores={mgs.zb.in_game=1}] add mgs.zb_sb_cand
function mgs:v5.0.0/zombies/sidebar_rank_players

# Build sidebar via macro
function mgs:v5.0.0/zombies/build_sidebar with storage mgs:temp

