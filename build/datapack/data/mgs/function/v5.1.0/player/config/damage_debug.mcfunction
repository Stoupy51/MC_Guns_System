
#> mgs:v5.1.0/player/config/damage_debug
#
# @within	#mgs:signals/damage
#
# @args		amount (unknown)
#			target (unknown)
#			attacker (unknown)
#

# Round amount to 1 decimal: store (amount * 10) as int score, then split into whole + decimal parts
$data modify storage mgs:temp amount set value $(amount)
execute store result score #dmg_x10 mgs.data run data get storage mgs:temp amount 10
scoreboard players operation #dmg_whole mgs.data = #dmg_x10 mgs.data
scoreboard players operation #dmg_whole mgs.data /= #10 mgs.data
scoreboard players operation #dmg_dec mgs.data = #dmg_x10 mgs.data
scoreboard players operation #dmg_dec mgs.data %= #10 mgs.data

# Damage Debug: global config overrides (tellraw @a), otherwise per-player (tellraw to shooter only)
# Per-player variant stays executed as @s (the victim) so the displayed selector is the REAL victim:
# resolving "@n at the victim's position" instead could pick an unrelated entity (e.g. the invisible
# ray gun projectile item_display) when the victim just died from this hit.
$execute if score #damage_debug mgs.config matches 1 run tellraw @a ["",[{"text":"","color":"red"},"[",{"translate":"mgs.dmg"},"] "],[{"score":{"name":"#dmg_whole","objective":"mgs.data"},"color":"gold"},".",{"score":{"name":"#dmg_dec","objective":"mgs.data"}}]," ",{"translate":"mgs.hp_to","color":"gray"}," ",{"selector":"$(target)"}," ",{"text":"by","color":"gray"}," ",{"selector":"$(attacker)"}]
$execute unless score #damage_debug mgs.config matches 1 if score $(attacker) mgs.player.damage_debug matches 1 run tellraw $(attacker) ["",[{"text":"","color":"red"},"[",{"translate":"mgs.dmg"},"] "],[{"score":{"name":"#dmg_whole","objective":"mgs.data"},"color":"gold"},".",{"score":{"name":"#dmg_dec","objective":"mgs.data"}}]," ",{"translate":"mgs.hp_to","color":"gray"}," ",{"selector":"@s"}]

