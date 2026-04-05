
#> mgs:v5.0.0/zombies/pap/anim_start
#
# @executed	at @s
#
# @within	mgs:v5.0.0/zombies/pap/on_right_click with storage mgs:temp _pap [ at @s ]
#
# @args		slot (unknown)
#

# @s = PAP machine entity, AT machine position
# $(slot) = player weapon slot (hotbar.1 / hotbar.2 / hotbar.3)

# Summon weapon item_display offset to the right of the machine
summon minecraft:item_display ~ ~0.8 ~ {Tags:["mgs.pap_weapon_display","mgs.gm_entity"],billboard:"fixed",item_display:"fixed",Glowing:0b,transformation:{left_rotation:[0f,0f,0f,1f],right_rotation:[0f,0f,0f,1f],translation:[0.8f,0f,0f],scale:[0.85f,0.85f,0.85f]}}

# Transfer weapon into display entity via contents slot, then clear player slot
$item replace entity @n[tag=mgs.pap_weapon_display,distance=..2] contents from entity @p[tag=mgs.pap_owner] $(slot)
$item replace entity @p[tag=mgs.pap_owner] $(slot) with minecraft:air

# Start going-in interpolation: slide horizontally from ahead to center over 40 ticks with 45-degree Y rotation
data merge entity @n[tag=mgs.pap_weapon_display,distance=..2] {interpolation_duration:40,start_interpolation:0,transformation:{left_rotation:[0f,0.0f,0f,0.1f],right_rotation:[0f,0f,0f,1f],translation:[0f,0f,0f],scale:[0.8f,0.8f,0.8f]}}

# Store this machine's slot for later retrieval when player collects the weapon
execute store result storage mgs:temp _pap_anim_slot.id int 1 run scoreboard players get @s mgs.zb.pap.id
$data modify storage mgs:temp _pap_anim_slot.slot set value "$(slot)"
function mgs:v5.0.0/zombies/pap/anim_store_slot with storage mgs:temp _pap_anim_slot

# Hide the static item_display temporarily (restored on collect or retreat finish)
kill @e[tag=mgs.pap_display,distance=..2]

# Start animation timer: 240 ticks (40 going-in + 60 inside + 40 coming-out; retreat after)
scoreboard players set @s mgs.pap_anim 240

# Sound: machine accepting weapon
playsound minecraft:block.beacon.activate ambient @a[distance=..30] ~ ~ ~ 1.0 0.6

