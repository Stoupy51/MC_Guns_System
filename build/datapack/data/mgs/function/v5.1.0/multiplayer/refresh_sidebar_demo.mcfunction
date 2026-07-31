
#> mgs:v5.1.0/multiplayer/refresh_sidebar_demo
#
# @executed	as the player & at current position
#
# @within	mgs:v5.1.0/multiplayer/create_sidebar_demo
#			mgs:v5.1.0/multiplayer/gamemodes/demo/tick
#

# Which side is attacking (in overtime both are, and the row says so)
execute if score #demo_attackers mgs.data matches 1 run data modify storage mgs:temp demo_sb.atk set value '[[" ⚔ ",{"translate":"mgs.attack","color":"gray"}],{"translate":"mgs.red","color":"red"}]'
execute if score #demo_attackers mgs.data matches 2 run data modify storage mgs:temp demo_sb.atk set value '[[" ⚔ ",{"translate":"mgs.attack","color":"gray"}],{"translate":"mgs.blue","color":"blue"}]'
execute if score #demo_round mgs.data matches 3.. run data modify storage mgs:temp demo_sb.atk set value '[[" ⚡ ",{"translate":"mgs.overtime","color":"gray"}],{"translate":"mgs.both","color":"gold"}]'

# One row per site, read off that site's own marker. Both rows stay meaningful in overtime: the sites are
# the same two, they just belong to nobody, so there is no third layout to describe here.
data modify storage mgs:temp demo_sb.a set value '[[" ",{"translate":"mgs.site_a","color":"dark_gray"}],{"text":"—","color":"dark_gray"}]'
data modify storage mgs:temp demo_sb.b set value '[[" ",{"translate":"mgs.site_b","color":"dark_gray"}],{"text":"—","color":"dark_gray"}]'
execute if entity @e[tag=mgs.demo_obj,tag=mgs.demo_site_A,scores={mgs.demo_state=0}] run data modify storage mgs:temp demo_sb.a set value '[[" ",{"translate":"mgs.site_a","color":"gray"}],["🔹 ",{"translate":"mgs.intact","color":"gray"}]]'
execute if entity @e[tag=mgs.demo_obj,tag=mgs.demo_site_A,scores={mgs.demo_state=1}] run data modify storage mgs:temp demo_sb.a set value '[[" ",{"translate":"mgs.site_a","color":"red"}],["💣 ",{"translate":"mgs.planted","color":"red"}]]'
execute if entity @e[tag=mgs.demo_obj,tag=mgs.demo_site_A,scores={mgs.demo_state=2}] run data modify storage mgs:temp demo_sb.a set value '[[" ",{"translate":"mgs.site_a","color":"dark_gray"}],["💥 ",{"translate":"mgs.destroyed_2","color":"dark_gray"}]]'
execute if entity @e[tag=mgs.demo_obj,tag=mgs.demo_site_B,scores={mgs.demo_state=0}] run data modify storage mgs:temp demo_sb.b set value '[[" ",{"translate":"mgs.site_b","color":"gray"}],["🔹 ",{"translate":"mgs.intact","color":"gray"}]]'
execute if entity @e[tag=mgs.demo_obj,tag=mgs.demo_site_B,scores={mgs.demo_state=1}] run data modify storage mgs:temp demo_sb.b set value '[[" ",{"translate":"mgs.site_b","color":"red"}],["💣 ",{"translate":"mgs.planted","color":"red"}]]'
execute if entity @e[tag=mgs.demo_obj,tag=mgs.demo_site_B,scores={mgs.demo_state=2}] run data modify storage mgs:temp demo_sb.b set value '[[" ",{"translate":"mgs.site_b","color":"dark_gray"}],["💥 ",{"translate":"mgs.destroyed_2","color":"dark_gray"}]]'

function mgs:v5.1.0/multiplayer/build_sidebar_demo with storage mgs:temp demo_sb

