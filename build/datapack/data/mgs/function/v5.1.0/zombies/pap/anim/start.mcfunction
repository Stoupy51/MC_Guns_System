
#> mgs:v5.1.0/zombies/pap/anim/start
#
# @executed	at @s
#
# @within	mgs:v5.1.0/zombies/pap/repap_scope_only with storage mgs:temp _pap [ at @s ]
#			mgs:v5.1.0/zombies/pap/on_right_click with storage mgs:temp _pap [ at @s ]
#
# @args		slot (unknown)
#

# @s = PAP machine entity, AT machine position
# $(slot) = player weapon slot (hotbar.1 / hotbar.2 / hotbar.3)

# Summon weapon item_display offset ahead of the machine (will slide to center)
execute positioned ~ ~-2 ~ positioned ~ ~0.8 ~ run summon minecraft:item_display ^ ^ ^0.6 {Tags:["mgs.pap_weapon_display","mgs.gm_entity"],billboard:"fixed",item_display:"fixed",transformation:{left_rotation:[0f,0f,0f,1f],right_rotation:[0f,0f,0f,1f],translation:[0f,0f,0f],scale:[0.4f,0.4f,0.4f]}}

# Transfer weapon into display entity via contents slot, then clear player slot
data modify entity @n[tag=mgs.pap_weapon_display,distance=..2] Rotation set from entity @s Rotation
$item replace entity @n[tag=mgs.pap_weapon_display,distance=..2] contents from entity @p[tag=mgs.pap_owner] $(slot)
$item replace entity @p[tag=mgs.pap_owner] $(slot) with minecraft:air

# Timeslip: this PAP runs 3x faster (anim/step called 3x/tick). Flag the machine off the owner and
# shorten the display's slide interpolation so the going-in/coming-out/retreat slides keep up.
scoreboard players set @s mgs.zb.pap.timeslip 0
execute if score @p[tag=mgs.pap_owner] mgs.special.timeslip matches 1 run scoreboard players set @s mgs.zb.pap.timeslip 1
execute if score @s mgs.zb.pap.timeslip matches 1 run data modify entity @n[tag=mgs.pap_weapon_display,distance=..2] teleport_duration set value 7
execute unless score @s mgs.zb.pap.timeslip matches 1 run data modify entity @n[tag=mgs.pap_weapon_display,distance=..2] teleport_duration set value 20

# Store this machine's slot for later retrieval when player collects the weapon
execute store result storage mgs:temp _pap_anim_slot.id int 1 run scoreboard players get @s mgs.zb.pap.id
$data modify storage mgs:temp _pap_anim_slot.slot set value "$(slot)"
function mgs:v5.1.0/zombies/pap/anim/store_slot with storage mgs:temp _pap_anim_slot

# Start animation timer: 300 ticks total
scoreboard players set @s mgs.pap_anim 300

# Sound: machine accepting weapon (Timeslip owners hear the 3x-speed jingle sting)
playsound mgs:zombies/pap/knuckle_crack ambient @a[scores={mgs.zb.in_game=1}] ~ ~ ~ 1.0 1.0
execute if score @s mgs.zb.pap.timeslip matches 1 run playsound mgs:zombies/pap/jingle_sting_short ambient @a[scores={mgs.zb.in_game=1}] ~ ~ ~ 1.0 1.0
execute unless score @s mgs.zb.pap.timeslip matches 1 run playsound mgs:zombies/pap/jingle_sting ambient @a[scores={mgs.zb.in_game=1}] ~ ~ ~ 1.0 1.0

