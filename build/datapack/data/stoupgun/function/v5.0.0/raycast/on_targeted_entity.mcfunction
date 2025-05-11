
#> stoupgun:v5.0.0/raycast/on_targeted_entity
#
# @within	stoupgun:v5.0.0/right_click/handle
#

# Blood particles
particle block{block_state:"redstone_wire"} ~ ~1 ~ 0.35 0.5 0.35 0 100 force @a[distance=..128]

# Is headshot? (#FIXME: hit_point is updated after function call)
scoreboard players set #is_headshot stoupgun.data 0
execute store result score #entity_y stoupgun.data run data get entity @s Pos[1] 1000
execute store result score #hit_y stoupgun.data run data get storage bs:lambda raycast.hit_point[1] 1000
scoreboard players operation #y_diff stoupgun.data = #hit_y stoupgun.data
scoreboard players operation #y_diff stoupgun.data -= #entity_y stoupgun.data
execute if score #y_diff stoupgun.data matches 1500.. run scoreboard players set #is_headshot stoupgun.data 1
#execute if score #is_headshot stoupgun.data matches 1 run say Headshot!

# Damage entity
data modify storage stoupgun:input with set value {target:"@s", amount:0.0d, attacker:"@p[tag=stoupgun.attacker]"}
execute if score #is_headshot stoupgun.data matches 1 store result storage stoupgun:input with.amount float 1.0 run data get storage stoupgun:gun stats.damage
execute if score #is_headshot stoupgun.data matches 0 store result storage stoupgun:input with.amount float 0.5 run data get storage stoupgun:gun stats.damage
function stoupgun:v5.0.0/utils/damage with storage stoupgun:input with

