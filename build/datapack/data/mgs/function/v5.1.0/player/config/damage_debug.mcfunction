
#> mgs:v5.1.0/player/config/damage_debug
#
# @within	#mgs:signals/damage
#
# @args		amount (unknown)
#			target (unknown)
#			attacker (unknown)
#

# Amount x10 as an int score, then split into whole and decimal parts.
$data modify storage mgs:temp amount set value $(amount)
execute store result score #dmg_x10 mgs.data run data get storage mgs:temp amount 10
scoreboard players operation #dmg_whole mgs.data = #dmg_x10 mgs.data
scoreboard players operation #dmg_whole mgs.data /= #10 mgs.data
scoreboard players operation #dmg_dec mgs.data = #dmg_x10 mgs.data
scoreboard players operation #dmg_dec mgs.data %= #10 mgs.data

# The global config (tellraw @a) wins over the player's own (tellraw to the shooter).
$execute if score #damage_debug mgs.config matches 1 run tellraw @a ["",[{"text":"","color":"red"},"[",{"translate":"mgs.dmg"},"] "],[{"score":{"name":"#dmg_whole","objective":"mgs.data"},"color":"gold"},".",{"score":{"name":"#dmg_dec","objective":"mgs.data"}}]," ",{"translate":"mgs.hp_to","color":"gray"}," ",{"selector":"$(target)"}," ",{"text":"by","color":"gray"}," ",{"selector":"$(attacker)"}]
$execute unless score #damage_debug mgs.config matches 1 as $(attacker) if entity @s[type=player] run tag @s add mgs.temp_dmg_reader
tellraw @a[tag=mgs.temp_dmg_reader,scores={mgs.player.damage_debug=1}] ["",[{"text":"","color":"red"},"[",{"translate":"mgs.dmg"},"] "],[{"score":{"name":"#dmg_whole","objective":"mgs.data"},"color":"gold"},".",{"score":{"name":"#dmg_dec","objective":"mgs.data"}}]," ",{"translate":"mgs.hp_to","color":"gray"}," ",{"selector":"@s"}]
tag @a[tag=mgs.temp_dmg_reader] remove mgs.temp_dmg_reader

