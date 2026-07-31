
#> mgs:v5.1.0/multiplayer/gamemodes/demo/start_overtime
#
# @executed	as @e[tag=mgs.demo_obj,scores={mgs.demo_state=1}] & at @s
#
# @within	mgs:v5.1.0/multiplayer/gamemodes/demo/next_round
#

tellraw @a [[{"text":"","color":"gold"},"[",{"translate":"mgs"},"] "],"⚡ ",{"translate":"mgs.overtime_one_neutral_site_first_to_detonate_it_wins","color":"gold","bold":true}]

# Take the regulation sites down. The fill has to happen while their markers are still alive, which is
# exactly what BombSites.cleanup_lines guarantees the order of.
execute at @e[tag=mgs.demo_obj] run fill ~ ~ ~ ~ ~1 ~ air
kill @e[tag=mgs.demo_obj]
kill @e[tag=mgs.demo_label]
kill @e[tag=mgs.demo_wreck]
kill @e[tag=mgs.demo_rubble]

function mgs:v5.1.0/multiplayer/gamemodes/demo/summon_ot_site
schedule function mgs:v5.1.0/multiplayer/gamemodes/demo/start_round 60t

