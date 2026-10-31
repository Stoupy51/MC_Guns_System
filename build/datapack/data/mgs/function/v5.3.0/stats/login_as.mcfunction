
#> mgs:v5.3.0/stats/login_as
#
# @executed	as @a
#
# @within	mgs:v5.3.0/stats/login with storage mgs:temp _st
#
# @args		uuid (unknown)
#			name (unknown)
#

$execute unless data storage mgs:stats players."$(uuid)" run function mgs:v5.3.0/stats/first_login with storage mgs:temp _st

# A rename leaves the entry's name behind the current one.
$data modify storage mgs:temp _st.old set from storage mgs:stats players."$(uuid)".name
data modify storage mgs:temp _st.cmp set from storage mgs:temp _st.old
execute store success score #st_renamed mgs.data run data modify storage mgs:temp _st.cmp set from storage mgs:temp _st.name
execute if score #st_renamed mgs.data matches 1 run function mgs:v5.3.0/stats/rename with storage mgs:temp _st

$data modify storage mgs:stats players."$(uuid)".name set value "$(name)"
$function mgs:v5.3.0/stats/snapshot/player {uuid:$(uuid),name:"$(name)"}
function mgs:v5.3.0/stats/board/levels with storage mgs:temp _st
function mgs:v5.3.0/stats/board/refresh_holograms

