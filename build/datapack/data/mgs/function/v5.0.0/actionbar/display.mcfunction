
#> mgs:v5.0.0/actionbar/display
#
# @executed	as @e[type=player,sort=random] & at @s
#
# @within	mgs:v5.0.0/actionbar/show with storage mgs:temp actionbar
#
# @args		list (unknown)
#

$data modify storage smithed.actionbar:input message set value {json:$(list),priority:'persistent',freeze:1}
function #smithed.actionbar:message

