
#> mgs:v5.1.0/zombies/escort/setup_lure_center
#
# @within	mgs:v5.1.0/zombies/preload_complete
#

kill @e[tag=mgs.lure_center]

# Let the map place its lure centre marker, run positioned at the map base
execute store result storage mgs:temp _base.x int 1 run scoreboard players get #gm_base_x mgs.data
execute store result storage mgs:temp _base.y int 1 run scoreboard players get #gm_base_y mgs.data
execute store result storage mgs:temp _base.z int 1 run scoreboard players get #gm_base_z mgs.data
data modify storage mgs:temp _base.fn set value "#mgs:zombies/setup_lure"
function mgs:v5.1.0/shared/call_at_base with storage mgs:temp _base

# Enable the lure only if the map actually placed a centre marker (its opt-in)
scoreboard players set #zb_pap_has mgs.data 0
execute if entity @e[tag=mgs.lure_center] run scoreboard players set #zb_pap_has mgs.data 1
scoreboard players set #zb_lure mgs.data 0

