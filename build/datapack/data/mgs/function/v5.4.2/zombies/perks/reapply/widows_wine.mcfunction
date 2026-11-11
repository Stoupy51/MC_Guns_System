
#> mgs:v5.4.2/zombies/perks/reapply/widows_wine
#
# @within	mgs:v5.4.2/dialog/close_then
#			mgs:v5.4.2/zombies/perks/tombstone_collect
#			mgs:v5.4.2/zombies/whos_who/revive_complete
#

scoreboard players set @s mgs.special.widows_wine 1
attribute @s minecraft:attack_damage modifier add mgs:widows_wine 6 add_value
function mgs:v5.4.2/zombies/inventory/loot_replace_lethal
item modify entity @s hotbar.7 mgs:v5.4.2/grenade/set_count_2
function mgs:v5.4.2/zombies/inventory/apply_slot_tag {slot:"hotbar.7",group:"hotbar",index:7}

