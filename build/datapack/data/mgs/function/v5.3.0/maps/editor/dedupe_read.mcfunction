
#> mgs:v5.3.0/maps/editor/dedupe_read
#
# @within	mgs:v5.3.0/dialog/close_then
#			mgs:v5.3.0/maps/editor/dedupe/red_spawn
#			mgs:v5.3.0/maps/editor/dedupe/blue_spawn
#			mgs:v5.3.0/maps/editor/dedupe/general_spawn
#			mgs:v5.3.0/maps/editor/dedupe/out_of_bounds
#			mgs:v5.3.0/maps/editor/dedupe/boundary
#			mgs:v5.3.0/maps/editor/dedupe/search_and_destroy
#			mgs:v5.3.0/maps/editor/dedupe/domination
#			mgs:v5.3.0/maps/editor/dedupe/hardpoint
#			mgs:v5.3.0/maps/editor/dedupe/start_command
#			mgs:v5.3.0/maps/editor/dedupe/respawn_command
#			mgs:v5.3.0/maps/editor/dedupe/mission_spawn
#			mgs:v5.3.0/maps/editor/dedupe/enemy
#			mgs:v5.3.0/maps/editor/dedupe/zombie_spawn
#			mgs:v5.3.0/maps/editor/dedupe/player_spawn_zb
#			mgs:v5.3.0/maps/editor/dedupe/special_spawn
#			mgs:v5.3.0/maps/editor/dedupe/wallbuy
#			mgs:v5.3.0/maps/editor/dedupe/door
#			mgs:v5.3.0/maps/editor/dedupe/trap
#			mgs:v5.3.0/maps/editor/dedupe/perk_machine
#			mgs:v5.3.0/maps/editor/dedupe/wunderfizz
#			mgs:v5.3.0/maps/editor/dedupe/pap_machine
#			mgs:v5.3.0/maps/editor/dedupe/mystery_box_pos
#			mgs:v5.3.0/maps/editor/dedupe/power_switch
#			mgs:v5.3.0/maps/editor/dedupe/barricade
#

data modify storage mgs:temp _dedupe set from entity @s data
data remove storage mgs:temp _dedupe._ed
data remove storage mgs:temp _dedupe._disp_sig

