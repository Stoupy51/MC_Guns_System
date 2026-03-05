
#> mgs:v5.0.0/player/config/damage_debug
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
$execute if score #damage_debug mgs.config matches 1 run tellraw @a ["",[{"text":"","color":"red"},"[",{"translate": "mgs.dmg"},"] "],[{"score":{"name":"#dmg_whole","objective":"mgs.data"},"color":"gold"},".",{"score":{"name":"#dmg_dec","objective":"mgs.data"}}],{"translate": "mgs.hp_to","color":"gray"},{"selector":"$(target)"},{"text":" by ","color":"gray"},{"selector":"$(attacker)"}]
$execute unless score #damage_debug mgs.config matches 1 at @s as $(attacker) if score @s mgs.player.damage_debug matches 1 run tellraw @s ["",[{"text":"","color":"red"},"[",{"translate": "mgs.dmg"},"] "],[{"score":{"name":"#dmg_whole","objective":"mgs.data"},"color":"gold"},".",{"score":{"name":"#dmg_dec","objective":"mgs.data"}}],{"translate": "mgs.hp_to","color":"gray"},{"selector":"@n"}]

