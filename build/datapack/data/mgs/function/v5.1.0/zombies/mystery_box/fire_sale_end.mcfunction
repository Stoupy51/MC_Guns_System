
#> mgs:v5.1.0/zombies/mystery_box/fire_sale_end
#
# @within	mgs:v5.1.0/zombies/powerups/fire_sale_tick
#

tag @e[tag=mgs.mb_fs_active] remove mgs.mb_fs_active
# Re-hide interaction entities of boxes that are no longer usable (boxes with a pull still in
# progress stay reachable via the sync's pull-in-progress check, so buyers can still collect).
function mgs:v5.1.0/zombies/mystery_box/sync_interaction_visibility
# If any pull is in progress, defer cleanup until the last display resets; otherwise clean up now.
execute if entity @e[tag=mgs.mb_display] run return run scoreboard players set #mb_fs_cleanup_pending mgs.data 1
function mgs:v5.1.0/zombies/mystery_box/fire_sale_cleanup

