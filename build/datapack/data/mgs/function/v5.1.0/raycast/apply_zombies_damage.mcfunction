
#> mgs:v5.1.0/raycast/apply_zombies_damage
#
# @within	mgs:v5.1.0/raycast/on_targeted_entity
#

execute store result score #zb_damage_mult mgs.data run data get storage mgs:gun all.stats.zombies_damage 100
scoreboard players operation #damage mgs.data *= #zb_damage_mult mgs.data
scoreboard players operation #damage mgs.data /= #100 mgs.data

