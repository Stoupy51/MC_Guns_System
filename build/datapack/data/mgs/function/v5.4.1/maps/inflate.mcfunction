
#> mgs:v5.4.1/maps/inflate
#
# @within	mgs:v5.4.1/dialog/close_then
#			mgs:v5.4.1/zombies/start
#			mgs:v5.4.1/maps/editor/enter
#

# Run with a zombies map in mgs:temp _inf_map.
data modify storage mgs:temp _inf_shared set value {}
data modify storage mgs:temp _inf_shared set from storage mgs:temp _inf_map.shared
data remove storage mgs:temp _inf_map.shared
execute unless data storage mgs:temp _inf_map.barricades run data modify storage mgs:temp _inf_map.barricades set from storage mgs:temp _inf_map.barriers
data remove storage mgs:temp _inf_map.barriers

data modify storage mgs:temp _inf_src set value []
data modify storage mgs:temp _inf_src set from storage mgs:temp _inf_map.spawning_points.zombies
execute if data storage mgs:temp _inf_src[0] run data modify storage mgs:temp _inf_map.spawning_points.zombies set value []
execute if data storage mgs:temp _inf_src[0] run function mgs:v5.4.1/maps/inflate/zombie_spawn

data modify storage mgs:temp _inf_src set value []
data modify storage mgs:temp _inf_src set from storage mgs:temp _inf_map.spawning_points.players
execute if data storage mgs:temp _inf_src[0] run data modify storage mgs:temp _inf_map.spawning_points.players set value []
execute if data storage mgs:temp _inf_src[0] run function mgs:v5.4.1/maps/inflate/player_spawn_zb

data modify storage mgs:temp _inf_src set value []
data modify storage mgs:temp _inf_src set from storage mgs:temp _inf_map.spawning_points.special
execute if data storage mgs:temp _inf_src[0] run data modify storage mgs:temp _inf_map.spawning_points.special set value []
execute if data storage mgs:temp _inf_src[0] run function mgs:v5.4.1/maps/inflate/special_spawn

data modify storage mgs:temp _inf_src set value []
data modify storage mgs:temp _inf_src set from storage mgs:temp _inf_map.wallbuys
execute if data storage mgs:temp _inf_src[0] run data modify storage mgs:temp _inf_map.wallbuys set value []
execute if data storage mgs:temp _inf_src[0] run function mgs:v5.4.1/maps/inflate/wallbuy

data modify storage mgs:temp _inf_src set value []
data modify storage mgs:temp _inf_src set from storage mgs:temp _inf_map.doors
execute if data storage mgs:temp _inf_src[0] run data modify storage mgs:temp _inf_map.doors set value []
execute if data storage mgs:temp _inf_src[0] run function mgs:v5.4.1/maps/inflate/door

data modify storage mgs:temp _inf_src set value []
data modify storage mgs:temp _inf_src set from storage mgs:temp _inf_map.traps
execute if data storage mgs:temp _inf_src[0] run data modify storage mgs:temp _inf_map.traps set value []
execute if data storage mgs:temp _inf_src[0] run function mgs:v5.4.1/maps/inflate/trap

data modify storage mgs:temp _inf_src set value []
data modify storage mgs:temp _inf_src set from storage mgs:temp _inf_map.perks
execute if data storage mgs:temp _inf_src[0] run data modify storage mgs:temp _inf_map.perks set value []
execute if data storage mgs:temp _inf_src[0] run function mgs:v5.4.1/maps/inflate/perk_machine

data modify storage mgs:temp _inf_src set value []
data modify storage mgs:temp _inf_src set from storage mgs:temp _inf_map.wunderfizz
execute if data storage mgs:temp _inf_src[0] run data modify storage mgs:temp _inf_map.wunderfizz set value []
execute if data storage mgs:temp _inf_src[0] run function mgs:v5.4.1/maps/inflate/wunderfizz

data modify storage mgs:temp _inf_src set value []
data modify storage mgs:temp _inf_src set from storage mgs:temp _inf_map.pap_machines
execute if data storage mgs:temp _inf_src[0] run data modify storage mgs:temp _inf_map.pap_machines set value []
execute if data storage mgs:temp _inf_src[0] run function mgs:v5.4.1/maps/inflate/pap_machine

data modify storage mgs:temp _inf_src set value []
data modify storage mgs:temp _inf_src set from storage mgs:temp _inf_map.mystery_box.positions
execute if data storage mgs:temp _inf_src[0] run data modify storage mgs:temp _inf_map.mystery_box.positions set value []
execute if data storage mgs:temp _inf_src[0] run function mgs:v5.4.1/maps/inflate/mystery_box_pos

data modify storage mgs:temp _inf_src set value []
data modify storage mgs:temp _inf_src set from storage mgs:temp _inf_map.power_switch
execute if data storage mgs:temp _inf_src[0] run data modify storage mgs:temp _inf_map.power_switch set value []
execute if data storage mgs:temp _inf_src[0] run function mgs:v5.4.1/maps/inflate/power_switch

data modify storage mgs:temp _inf_src set value []
data modify storage mgs:temp _inf_src set from storage mgs:temp _inf_map.barricades
execute if data storage mgs:temp _inf_src[0] run data modify storage mgs:temp _inf_map.barricades set value []
execute if data storage mgs:temp _inf_src[0] run function mgs:v5.4.1/maps/inflate/barricade

