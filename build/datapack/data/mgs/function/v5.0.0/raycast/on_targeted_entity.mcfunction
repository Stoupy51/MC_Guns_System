
#> mgs:v5.0.0/raycast/on_targeted_entity
#
# @executed	anchored eyes & positioned ^ ^ ^
#
# @within	mgs:v5.0.0/raycast/main
#

# Friendly fire check: skip if target is a teammate (but not the shooter themselves)
execute if entity @s[type=player] unless entity @s[tag=mgs.ticking] store result score #shooter_team mgs.data run scoreboard players get @n[tag=mgs.ticking] mgs.mp.team
execute if entity @s[type=player] unless entity @s[tag=mgs.ticking] if score #shooter_team mgs.data matches 1.. if score @s mgs.mp.team = #shooter_team mgs.data run return fail

# Mark that we hit an entity
scoreboard players set #is_entity_hit mgs.data 1
tag @s add mgs.raycast_target

# Blood particles
execute at @s run particle block{block_state:"redstone_wire"} ~ ~1 ~ 0.35 0.5 0.35 0 100 force @a[distance=..128]

# Store attack info and calculate decay
data modify storage mgs:input with set value {target:"@s", amount:0.0f, attacker:"@n[tag=mgs.ticking]"}
execute if entity @n[tag=mgs.ticking,type=player] run data modify storage mgs:input with.attacker set value "@p[tag=mgs.ticking]"
execute store result score #damage mgs.data run data get storage mgs:temp damage 10
function mgs:v5.0.0/raycast/apply_decay

