
#> mgs:v5.1.0/zombies/wunderfizz/set_model/dying_wish
#
# @executed	as @e[tag=mgs.wunderfizz_orb] & at @s
#
# @within	mgs:v5.1.0/zombies/wunderfizz/spin_cycle
#			mgs:v5.1.0/zombies/wunderfizz/land
#

data modify entity @s item set value {id:"minecraft:potion",count:1,components:{"minecraft:item_model":"mgs:perk_machine_dying_wish"}}

