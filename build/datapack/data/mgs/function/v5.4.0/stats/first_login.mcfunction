
#> mgs:v5.4.0/stats/first_login
#
# @within	mgs:v5.4.0/dialog/close_then
#			mgs:v5.4.0/stats/login_as with storage mgs:temp _st
#
# @args		uuid (unknown)
#			name (unknown)
#

$data modify storage mgs:stats players."$(uuid)" set value {name:"$(name)"}
execute store result score @s mgs.st.index run data get storage mgs:stats known
$data modify storage mgs:stats known append value $(uuid)

