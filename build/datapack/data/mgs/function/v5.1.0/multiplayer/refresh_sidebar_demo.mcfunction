
#> mgs:v5.1.0/multiplayer/refresh_sidebar_demo
#
# @executed	as the player & at current position
#
# @within	mgs:v5.1.0/multiplayer/create_sidebar_demo
#			mgs:v5.1.0/multiplayer/gamemodes/demo/tick
#

# Which side is attacking. Label and team are stored apart so the decider only relabels the left half,
# instead of needing one row string per round kind and attacking side pair.
data modify storage mgs:temp demo_sb.atk_label set value '[" ⚔ ",{"translate":"mgs.attack","color":"gray"}]'
execute if score #demo_round mgs.data matches 3.. run data modify storage mgs:temp demo_sb.atk_label set value '[" ⚡ ",{"translate":"mgs.decider","color":"gold"}]'
data modify storage mgs:temp demo_sb.atk_team set value '{"text":"—","color":"dark_gray"}'
execute if score #demo_attackers mgs.data matches 1 run data modify storage mgs:temp demo_sb.atk_team set value '{"translate":"mgs.red","color":"red"}'
execute if score #demo_attackers mgs.data matches 2 run data modify storage mgs:temp demo_sb.atk_team set value '{"translate":"mgs.blue","color":"blue"}'

# One row per site, read off that site's own marker
data modify storage mgs:temp demo_sb.a set value '[[" ",{"translate":"mgs.site_a","color":"dark_gray"}],{"text":"—","color":"dark_gray"}]'
data modify storage mgs:temp demo_sb.b set value '[[" ",{"translate":"mgs.site_b","color":"dark_gray"}],{"text":"—","color":"dark_gray"}]'
execute if entity @e[tag=mgs.demo_obj,tag=mgs.demo_site_A,scores={mgs.demo_state=0}] run data modify storage mgs:temp demo_sb.a set value '[[" ",{"translate":"mgs.site_a","color":"gray"}],["🔹 ",{"translate":"mgs.intact","color":"gray"}]]'
execute if entity @e[tag=mgs.demo_obj,tag=mgs.demo_site_A,scores={mgs.demo_state=1}] run data modify storage mgs:temp demo_sb.a set value '[[" ",{"translate":"mgs.site_a","color":"red"}],["💣 ",{"translate":"mgs.planted","color":"red"}]]'
execute if entity @e[tag=mgs.demo_obj,tag=mgs.demo_site_A,scores={mgs.demo_state=2}] run data modify storage mgs:temp demo_sb.a set value '[[" ",{"translate":"mgs.site_a","color":"dark_gray"}],["💥 ",{"translate":"mgs.destroyed_2","color":"dark_gray"}]]'
execute if entity @e[tag=mgs.demo_obj,tag=mgs.demo_site_B,scores={mgs.demo_state=0}] run data modify storage mgs:temp demo_sb.b set value '[[" ",{"translate":"mgs.site_b","color":"gray"}],["🔹 ",{"translate":"mgs.intact","color":"gray"}]]'
execute if entity @e[tag=mgs.demo_obj,tag=mgs.demo_site_B,scores={mgs.demo_state=1}] run data modify storage mgs:temp demo_sb.b set value '[[" ",{"translate":"mgs.site_b","color":"red"}],["💣 ",{"translate":"mgs.planted","color":"red"}]]'
execute if entity @e[tag=mgs.demo_obj,tag=mgs.demo_site_B,scores={mgs.demo_state=2}] run data modify storage mgs:temp demo_sb.b set value '[[" ",{"translate":"mgs.site_b","color":"dark_gray"}],["💥 ",{"translate":"mgs.destroyed_2","color":"dark_gray"}]]'

function mgs:v5.1.0/multiplayer/build_sidebar_demo with storage mgs:temp demo_sb

