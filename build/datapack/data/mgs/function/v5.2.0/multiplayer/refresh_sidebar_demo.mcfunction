
#> mgs:v5.2.0/multiplayer/refresh_sidebar_demo
#
# @executed	as the player & at current position
#
# @within	mgs:v5.2.0/multiplayer/create_sidebar_demo
#			mgs:v5.2.0/multiplayer/gamemodes/demo/tick
#

# Label and team are stored apart, so the decider only relabels the left half.
data modify storage mgs:temp demo_sb.atk_label set value '[" ⚔ ",{"translate":"mgs.attack","fallback":"Attack","color":"gray"}]'
execute if score #demo_round mgs.data matches 3.. run data modify storage mgs:temp demo_sb.atk_label set value '[" ⚡ ",{"translate":"mgs.decider","fallback":"Decider","color":"gold"}]'
data modify storage mgs:temp demo_sb.atk_team set value '{"text":"-","color":"dark_gray"}'
execute if score #demo_attackers mgs.data matches 1 run data modify storage mgs:temp demo_sb.atk_team set value '{"translate":"mgs.red","fallback":"Red","color":"red"}'
execute if score #demo_attackers mgs.data matches 2 run data modify storage mgs:temp demo_sb.atk_team set value '{"translate":"mgs.blue","fallback":"Blue","color":"blue"}'

data modify storage mgs:temp demo_sb.a set value '[[" ",{"translate":"mgs.site_a","fallback":"Site A","color":"dark_gray"}],{"text":"-","color":"dark_gray"}]'
data modify storage mgs:temp demo_sb.b set value '[[" ",{"translate":"mgs.site_b","fallback":"Site B","color":"dark_gray"}],{"text":"-","color":"dark_gray"}]'
execute if entity @e[tag=mgs.demo_obj,tag=mgs.demo_site_A,scores={mgs.demo_state=0}] run data modify storage mgs:temp demo_sb.a set value '[[" ",{"translate":"mgs.site_a","fallback":"Site A","color":"gray"}],["🔹 ",{"translate":"mgs.intact","fallback":"Intact","color":"gray"}]]'
execute if entity @e[tag=mgs.demo_obj,tag=mgs.demo_site_A,scores={mgs.demo_state=1}] run data modify storage mgs:temp demo_sb.a set value '[[" ",{"translate":"mgs.site_a","fallback":"Site A","color":"red"}],["💣 ",{"translate":"mgs.planted","fallback":"PLANTED","color":"red"}]]'
execute if entity @e[tag=mgs.demo_obj,tag=mgs.demo_site_A,scores={mgs.demo_state=2}] run data modify storage mgs:temp demo_sb.a set value '[[" ",{"translate":"mgs.site_a","fallback":"Site A","color":"dark_gray"}],["💥 ",{"translate":"mgs.destroyed_2","fallback":"Destroyed","color":"dark_gray"}]]'
execute if entity @e[tag=mgs.demo_obj,tag=mgs.demo_site_B,scores={mgs.demo_state=0}] run data modify storage mgs:temp demo_sb.b set value '[[" ",{"translate":"mgs.site_b","fallback":"Site B","color":"gray"}],["🔹 ",{"translate":"mgs.intact","fallback":"Intact","color":"gray"}]]'
execute if entity @e[tag=mgs.demo_obj,tag=mgs.demo_site_B,scores={mgs.demo_state=1}] run data modify storage mgs:temp demo_sb.b set value '[[" ",{"translate":"mgs.site_b","fallback":"Site B","color":"red"}],["💣 ",{"translate":"mgs.planted","fallback":"PLANTED","color":"red"}]]'
execute if entity @e[tag=mgs.demo_obj,tag=mgs.demo_site_B,scores={mgs.demo_state=2}] run data modify storage mgs:temp demo_sb.b set value '[[" ",{"translate":"mgs.site_b","fallback":"Site B","color":"dark_gray"}],["💥 ",{"translate":"mgs.destroyed_2","fallback":"Destroyed","color":"dark_gray"}]]'

function mgs:v5.2.0/multiplayer/build_sidebar_demo with storage mgs:temp demo_sb

