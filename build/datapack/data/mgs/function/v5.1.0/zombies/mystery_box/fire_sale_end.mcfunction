
#> mgs:v5.1.0/zombies/mystery_box/fire_sale_end
#
# @within	mgs:v5.1.0/zombies/powerups/fire_sale_tick
#

tag @e[tag=mgs.mb_fs_active] remove mgs.mb_fs_active
# Boxes with a pull in progress stay reachable, so buyers can still collect.
function mgs:v5.1.0/zombies/mystery_box/sync_interaction_visibility
execute if entity @e[tag=mgs.mb_display] run return run scoreboard players set #mb_fs_cleanup_pending mgs.data 1
function mgs:v5.1.0/zombies/mystery_box/fire_sale_cleanup

