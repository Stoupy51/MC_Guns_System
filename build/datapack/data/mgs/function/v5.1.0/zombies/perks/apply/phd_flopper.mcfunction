
#> mgs:v5.1.0/zombies/perks/apply/phd_flopper
#
# @within	???
#

attribute @s minecraft:fall_damage_multiplier base set 0
scoreboard players set @s mgs.special.phd_flopper 1
tellraw @s [[{"text":"","color":"gold"},"[",{"translate":"mgs"},"] "],"🧪 ",{"translate":"mgs.phd_flopper_immune_to_explosions_fall_damage","color":"dark_purple"}]

