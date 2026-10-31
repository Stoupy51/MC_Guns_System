
#> mgs:v5.3.0/stats/first_login
#
# @executed	as @a
#
# @within	mgs:v5.3.0/stats/login_as with storage mgs:temp _st
#
# @args		uuid (unknown)
#			name (unknown)
#

$data modify storage mgs:stats players."$(uuid)" set value {name:"$(name)"}
execute store result score @s mgs.st.index run data get storage mgs:stats known
$data modify storage mgs:stats known append value $(uuid)

