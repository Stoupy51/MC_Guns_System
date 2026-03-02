
#> mgs:v5.0.0/player/config/damage_debug
#
# @within	#mgs:signals/damage
#
# @args		amount (unknown)
#			target (unknown)
#			attacker (unknown)
#

# Damage debug: global config overrides (tellraw @a), otherwise per-player (tellraw to shooter only)
$execute if score #damage_debug mgs.config matches 1 run tellraw @a [{"translate": "mgs.dmg","color":"red"},{"text":"$(amount)","color":"gold"},{"translate": "mgs.hp_to","color":"gray"},{"selector":"$(target)"},{"text":" by ","color":"gray"},{"selector":"$(attacker)"}]
$execute unless score #damage_debug mgs.config matches 1 if score $(attacker) mgs.player.damage_debug matches 1 run tellraw $(attacker) [{"translate": "mgs.dmg","color":"red"},{"text":"$(amount)","color":"gold"},{"translate": "mgs.hp_to","color":"gray"},{"selector":"$(target)"}]

