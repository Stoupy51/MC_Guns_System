
#> mgs:v5.0.0/multiplayer/refresh_sidebar_dom
#
# @within	mgs:v5.0.0/multiplayer/create_sidebar_dom
#			mgs:v5.0.0/multiplayer/gamemodes/dom/score_tick
#			mgs:v5.0.0/multiplayer/gamemodes/dom/on_kill
#

# Build point status strings based on ownership scores
# Zone A
execute if score #dom_owner_a mgs.data matches 0 run data modify storage mgs:temp dom_sb.a set value '{"translate": "mgs.a_neutral","color":"gray"}'
execute if score #dom_owner_a mgs.data matches 1 run data modify storage mgs:temp dom_sb.a set value '{"translate": "mgs.a_red","color":"red"}'
execute if score #dom_owner_a mgs.data matches 2 run data modify storage mgs:temp dom_sb.a set value '{"translate": "mgs.a_blue","color":"blue"}'

# Zone B
execute if score #dom_owner_b mgs.data matches 0 run data modify storage mgs:temp dom_sb.b set value '{"translate": "mgs.b_neutral","color":"gray"}'
execute if score #dom_owner_b mgs.data matches 1 run data modify storage mgs:temp dom_sb.b set value '{"translate": "mgs.b_red","color":"red"}'
execute if score #dom_owner_b mgs.data matches 2 run data modify storage mgs:temp dom_sb.b set value '{"translate": "mgs.b_blue","color":"blue"}'

# Zone C
execute if score #dom_owner_c mgs.data matches 0 run data modify storage mgs:temp dom_sb.c set value '{"translate": "mgs.c_neutral","color":"gray"}'
execute if score #dom_owner_c mgs.data matches 1 run data modify storage mgs:temp dom_sb.c set value '{"translate": "mgs.c_red","color":"red"}'
execute if score #dom_owner_c mgs.data matches 2 run data modify storage mgs:temp dom_sb.c set value '{"translate": "mgs.c_blue","color":"blue"}'

# Build sidebar with dynamic point entries
function mgs:v5.0.0/multiplayer/build_sidebar_dom with storage mgs:temp dom_sb

