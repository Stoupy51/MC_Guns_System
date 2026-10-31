
#> mgs:v5.3.0/zombies/mystery_box/weigh_ray_gun
#
# @executed	as @a[scores={mgs.zb.in_game=1}]
#
# @within	mgs:v5.3.0/zombies/mystery_box/pick_for_buyer
#

execute if score #mb_ray_index mgs.data matches ..-1 run return 0

scoreboard players operation #mb_w mgs.data = #mb_ray_weight mgs.data
execute if score #zb_round mgs.data matches ..24 if score #mb_dry_ray_gun mgs.data matches 6.. run scoreboard players operation #mb_w mgs.data += #mb_ray_weight mgs.data
execute store result storage mgs:temp _mb_ray.i int 1 run scoreboard players get #mb_ray_index mgs.data
execute store result storage mgs:temp _mb_ray.w int 1 run scoreboard players get #mb_w mgs.data
function mgs:v5.3.0/zombies/mystery_box/weigh_ray_gun_at with storage mgs:temp _mb_ray

