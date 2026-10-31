
#> mgs:v5.3.0/maps/editor/name/special_spawn
#
# @within	mgs:v5.3.0/maps/editor/refresh_marker
#

execute if data storage mgs:temp _ed_name{arrival:"floor"} run data modify storage mgs:temp _ed_name.arrival_flag set value " floor"
execute if data storage mgs:temp _ed_name{arrival:"ceiling"} run data modify storage mgs:temp _ed_name.arrival_flag set value " ceiling"
execute if data storage mgs:temp _ed_name{arrival:"instant"} run data modify storage mgs:temp _ed_name.arrival_flag set value " instant"
function mgs:v5.3.0/maps/editor/name/special_spawn_apply with storage mgs:temp _ed_name

