
#> mgs:v5.1.0/multiplayer/refresh_sidebar_dom
#
# @executed	as the player & at current position
#
# @within	mgs:v5.1.0/multiplayer/create_sidebar_dom
#			mgs:v5.1.0/multiplayer/gamemodes/dom/score_tick
#			mgs:v5.1.0/multiplayer/gamemodes/dom/on_kill
#

# Build point status strings based on ownership scores
# Zone A
execute if score #dom_owner_a mgs.data matches 0 run data modify storage mgs:temp dom_sb.a set value '[" ",{"text":"A: ","color":"gray"},"⚪ ",{"translate":"mgs.neutral","color":"gray"}]'
execute if score #dom_owner_a mgs.data matches 1 run data modify storage mgs:temp dom_sb.a set value '[" ",{"text":"A: ","color":"red"},"🔴 ",{"translate":"mgs.red","color":"red"}]'
execute if score #dom_owner_a mgs.data matches 2 run data modify storage mgs:temp dom_sb.a set value '[" ",{"text":"A: ","color":"blue"},"🔵 ",{"translate":"mgs.blue","color":"blue"}]'

# Zone B
execute if score #dom_owner_b mgs.data matches 0 run data modify storage mgs:temp dom_sb.b set value '[" ",{"text":"B: ","color":"gray"},"⚪ ",{"translate":"mgs.neutral","color":"gray"}]'
execute if score #dom_owner_b mgs.data matches 1 run data modify storage mgs:temp dom_sb.b set value '[" ",{"text":"B: ","color":"red"},"🔴 ",{"translate":"mgs.red","color":"red"}]'
execute if score #dom_owner_b mgs.data matches 2 run data modify storage mgs:temp dom_sb.b set value '[" ",{"text":"B: ","color":"blue"},"🔵 ",{"translate":"mgs.blue","color":"blue"}]'

# Zone C
execute if score #dom_owner_c mgs.data matches 0 run data modify storage mgs:temp dom_sb.c set value '[" ",{"text":"C: ","color":"gray"},"⚪ ",{"translate":"mgs.neutral","color":"gray"}]'
execute if score #dom_owner_c mgs.data matches 1 run data modify storage mgs:temp dom_sb.c set value '[" ",{"text":"C: ","color":"red"},"🔴 ",{"translate":"mgs.red","color":"red"}]'
execute if score #dom_owner_c mgs.data matches 2 run data modify storage mgs:temp dom_sb.c set value '[" ",{"text":"C: ","color":"blue"},"🔵 ",{"translate":"mgs.blue","color":"blue"}]'

# Build sidebar with dynamic point entries
function mgs:v5.1.0/multiplayer/build_sidebar_dom with storage mgs:temp dom_sb

