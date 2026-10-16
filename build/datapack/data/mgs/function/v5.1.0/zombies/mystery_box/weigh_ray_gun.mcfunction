
#> mgs:v5.1.0/zombies/mystery_box/weigh_ray_gun
#
# @executed	as @a[scores={mgs.zb.in_game=1}]
#
# @within	mgs:v5.1.0/zombies/mystery_box/pick_for_buyer
#

data modify storage mgs:zombies mystery_box_weights[29] set value 1
execute if score #zb_round mgs.data matches ..24 if score #mb_dry_ray_gun mgs.data matches 6.. run data modify storage mgs:zombies mystery_box_weights[29] set value 2

