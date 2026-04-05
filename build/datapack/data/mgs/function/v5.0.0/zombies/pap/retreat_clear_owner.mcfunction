
#> mgs:v5.0.0/zombies/pap/retreat_clear_owner
#
# @executed	as @a[scores={mgs.zb.pap_s=1..}]
#
# @within	mgs:v5.0.0/zombies/pap/retreat_cleanup [ as @a[scores={mgs.zb.pap_s=1..}] ]
#

# Clear the orphaned magazine from the corresponding inventory slot
execute if data storage mgs:temp _pap_retreat{slot:"hotbar.1"} run item replace entity @s inventory.1 with air
execute if data storage mgs:temp _pap_retreat{slot:"hotbar.2"} run item replace entity @s inventory.2 with air
execute if data storage mgs:temp _pap_retreat{slot:"hotbar.3"} run item replace entity @s inventory.3 with air

# Reset PAP tracking scores
scoreboard players set @s mgs.zb.pap_s 0
scoreboard players set @s mgs.zb.pap_mid 0

