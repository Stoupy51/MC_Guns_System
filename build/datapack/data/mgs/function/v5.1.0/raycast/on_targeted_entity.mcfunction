
#> mgs:v5.1.0/raycast/on_targeted_entity
#
# @within	string in mgs:v5.1.0/raycast/main
#

# Teammates are skipped, the shooter is not.
execute if entity @s[type=player,gamemode=spectator] run return 0
execute if entity @s[type=player] unless entity @s[tag=mgs.ticking] store result score #shooter_team mgs.data run scoreboard players get @n[tag=mgs.ticking] mgs.mp.team
execute if entity @s[type=player] unless entity @s[tag=mgs.ticking] if score #shooter_team mgs.data matches 1.. if score @s mgs.mp.team = #shooter_team mgs.data run return fail

scoreboard players set #is_entity_hit mgs.data 1
tag @s add mgs.raycast_target

# Only the first 3 entities hit per shot bleed.
execute if score #hit_particles_left mgs.data matches 1.. at @s run particle block{block_state:"redstone_wire"} ~ ~1 ~ 0.35 0.5 0.35 0 100 force @a[distance=..128]
scoreboard players remove #hit_particles_left mgs.data 1

data modify storage mgs:input with set value {target:"@s", amount:0.0f, attacker:"@n[tag=mgs.ticking]"}
execute if entity @n[tag=mgs.ticking,type=player] run data modify storage mgs:input with.attacker set value "@p[tag=mgs.ticking]"
execute store result score #damage mgs.data run data get storage mgs:temp damage 10
execute if score @n[tag=mgs.ticking] mgs.special.double_tap matches 1.. run scoreboard players operation #damage mgs.data *= #2 mgs.data
function mgs:v5.1.0/raycast/apply_decay

