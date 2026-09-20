
#> mgs:v5.1.0/zombies/perks/reapply/widows_wine
#
# @executed	as @a[distance=..2,gamemode=!spectator,scores={mgs.zb.in_game=1,mgs.zb.downed=0}]
#
# @within	mgs:v5.1.0/zombies/perks/tombstone_collect
#			mgs:v5.1.0/zombies/whos_who/revive_complete
#

scoreboard players set @s mgs.special.widows_wine 1
attribute @s minecraft:attack_damage modifier add mgs:widows_wine 6 add_value
function mgs:v5.1.0/zombies/inventory/loot_replace_lethal
item modify entity @s hotbar.7 mgs:v5.1.0/grenade/set_count_2
function mgs:v5.1.0/zombies/inventory/apply_slot_tag {slot:"hotbar.7",group:"hotbar",index:7}

