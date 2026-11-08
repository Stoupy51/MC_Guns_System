
#> mgs:v5.4.1/actionbar/display
#
# @within	mgs:v5.4.1/dialog/close_then
#			mgs:v5.4.1/actionbar/show with storage mgs:temp actionbar
#
# @args		list (unknown)
#

$data modify storage smithed.actionbar:input message set value {json:$(list),priority:'persistent',freeze:1}
function #smithed.actionbar:message

