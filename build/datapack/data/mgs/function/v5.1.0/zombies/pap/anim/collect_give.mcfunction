
#> mgs:v5.1.0/zombies/pap/anim/collect_give
#
# @executed	at @s
#
# @within	mgs:v5.1.0/zombies/pap/anim/collect_lookup with storage mgs:temp _pap_cg
#
# @args		slot (unknown)
#			id (unknown)
#

$item replace entity @p[tag=mgs.pap_owner] $(slot) from entity @n[tag=mgs.pap_weapon_display,distance=..2] contents

execute as @p[tag=mgs.pap_owner] run function mgs:v5.1.0/ammo/compute_reserve

scoreboard players set @s mgs.pap_anim -1

# The item was already given back.
kill @e[tag=mgs.pap_weapon_display,distance=..2]

execute store result score #pap_mid mgs.data run scoreboard players get @s mgs.zb.pap.id
execute as @a[scores={mgs.zb.pap_s=1..}] if score @s mgs.zb.pap_mid = #pap_mid mgs.data run scoreboard players set @s mgs.zb.pap_s 0
execute as @a[scores={mgs.zb.pap_mid=1..}] if score @s mgs.zb.pap_mid = #pap_mid mgs.data run scoreboard players set @s mgs.zb.pap_mid 0

$data remove storage mgs:zombies pap_anim_slot."$(id)"

execute as @p[tag=mgs.pap_owner] run playsound minecraft:entity.experience_orb.pickup ambient @s ~ ~ ~ 0.8 1.25

