
#> mgs:v5.3.0/maps/editor/name/zombie_spawn
#
# @within	mgs:v5.3.0/maps/editor/refresh_marker
#

execute if data storage mgs:temp _ed_name{arrival:"ceiling"} run data modify storage mgs:temp _ed_name.arrival_flag set value " ceiling"
execute if data storage mgs:temp _ed_name{arrival:"portal"} run data modify storage mgs:temp _ed_name.arrival_flag set value " portal"
execute if data storage mgs:temp _ed_name{arrival:"instant"} run data modify storage mgs:temp _ed_name.arrival_flag set value " instant"
function mgs:v5.3.0/maps/editor/name/zombie_spawn_apply with storage mgs:temp _ed_name

