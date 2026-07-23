
#> mgs:v5.1.0/zombies/mystery_box/refresh_disabled
#
# @within	mgs:v5.1.0/zombies/mystery_box/sync_presence_display
#			mgs:v5.1.0/zombies/mystery_box/fire_sale_cleanup
#			mgs:v5.1.0/zombies/mystery_box/move_anim_land
#

kill @e[tag=mgs.mb_disabled]
execute if score #zb_fire_sale_timer mgs.data matches ..0 as @e[tag=mgs.mystery_box_pos,tag=!mgs.mystery_box_active] at @s run function mgs:v5.1.0/zombies/mystery_box/summon_disabled_display

