
#> mgs:v5.0.0/zombies/pap/anim_collect_give
#
# @executed	at @s
#
# @within	mgs:v5.0.0/zombies/pap/anim_collect_lookup with storage mgs:temp _pap_cg
#
# @args		slot (unknown)
#

# Return upgraded weapon directly from the display entity's contents slot
$item replace entity @p[tag=mgs.pap_owner] $(slot) from entity @n[tag=mgs.pap_weapon_display,distance=..2] contents

# Refresh ammo HUD
execute as @p[tag=mgs.pap_owner] run function mgs:v5.0.0/ammo/compute_reserve

# Reset animation timer to idle
scoreboard players set @s mgs.pap_anim -1

# Remove weapon display (item already given back, safe to kill)
kill @e[tag=mgs.pap_weapon_display,distance=..2]

# Restore the static machine display entity
function mgs:v5.0.0/zombies/pap/anim_restore_display

# Notify the player
execute as @p[tag=mgs.pap_owner] run tellraw @s [[{"text":"","color":"gold"},"[",{"translate":"mgs"},"] "],{"translate":"mgs.collect_your_upgraded_weapon","color":"green","bold":true}]
execute as @p[tag=mgs.pap_owner] run function mgs:v5.0.0/zombies/feedback/sound_success

