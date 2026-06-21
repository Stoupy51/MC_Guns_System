
#> mgs:v5.0.1/zombies/refresh_sidebar
#
# @within	mgs:v5.0.1/zombies/game_tick
#			mgs:v5.0.1/zombies/check_kill_points
#			mgs:v5.0.1/zombies/on_hit_signal
#			mgs:v5.0.1/zombies/create_sidebar
#			mgs:v5.0.1/zombies/start_round
#

# Zombie count (#zb_alive) is recomputed every tick by game_tick. Reuse it here instead of
# rescanning @e[tag=mgs.zombie_round]: refresh_sidebar runs on every bullet hit (on_hit_signal)
# and every kill (check_kill_points), so the old rescan was a full entity scan per hit/kill during
# combat. Non-tick callers (create_sidebar during prep) seed #zb_alive themselves before calling.
scoreboard players operation #zb_total mgs.data = #zb_alive mgs.data
scoreboard players operation #zb_total mgs.data += #zb_to_spawn mgs.data
execute if score #zb_total mgs.data matches ..-1 run scoreboard players set #zb_total mgs.data 0

# Initialize sidebar contents
data modify storage mgs:temp zb_sb set value [[{translate:"mgs.round_2",color:"red"},{score:{name:"#zb_round",objective:"mgs.data"},color:"gold"}],[{translate:"mgs.zombies",color:"red"},{score:{name:"#zb_total",objective:"mgs.data"},color:"gold"}]," "]

# Rank players for sidebar display
scoreboard players set @a mgs.zb.sb_rank 0
tag @a remove mgs.zb_sb_cand
tag @a[scores={mgs.zb.in_game=1}] add mgs.zb_sb_cand
function mgs:v5.0.1/zombies/sidebar_rank_players

# Build sidebar via macro
function mgs:v5.0.1/zombies/build_sidebar with storage mgs:temp

