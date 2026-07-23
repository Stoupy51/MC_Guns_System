
#> mgs:v5.1.0/zombies/perks/apply/widows_wine
#
# @within	???
#

scoreboard players set @s mgs.special.widows_wine 1
attribute @s minecraft:attack_damage modifier add mgs:widows_wine 6 add_value
function mgs:v5.1.0/zombies/inventory/loot_replace_lethal
item modify entity @s hotbar.7 mgs:v5.1.0/grenade/set_count_2
function mgs:v5.1.0/zombies/inventory/apply_slot_tag {slot:"hotbar.7",group:"hotbar",index:7}
tellraw @s [[{"text":"","color":"gold"},"[",{"translate":"mgs"},"] "],"🕸 ",{"translate":"mgs.widows_wine_web_grenades_webbing_melee","color":"dark_red"}]

