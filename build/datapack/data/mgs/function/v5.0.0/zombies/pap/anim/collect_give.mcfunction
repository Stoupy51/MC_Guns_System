
#> mgs:v5.0.0/zombies/pap/anim/collect_give
#
# @executed	at @s
#
# @within	mgs:v5.0.0/zombies/pap/anim/collect_lookup with storage mgs:temp _pap_cg
#
# @args		slot (unknown)
#			id (unknown)
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
function mgs:v5.0.0/zombies/pap/anim/restore_display

# Clear PAP slot tracking for the original owner
execute store result score #pap_mid mgs.data run scoreboard players get @s mgs.zb.pap.id
execute as @a[scores={mgs.zb.pap_s=1..}] if score @s mgs.zb.pap_mid = #pap_mid mgs.data run scoreboard players set @s mgs.zb.pap_s 0
execute as @a[scores={mgs.zb.pap_mid=1..}] if score @s mgs.zb.pap_mid = #pap_mid mgs.data run scoreboard players set @s mgs.zb.pap_mid 0

# Clean stored slot data
$data remove storage mgs:zombies pap_anim_slot."$(id)"

# Notify the player
execute as @p[tag=mgs.pap_owner] run function mgs:v5.0.0/zombies/feedback/sound_success

