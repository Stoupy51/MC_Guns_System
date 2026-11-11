
#> mgs:v5.4.2/casing/update_item
#
# @within	mgs:v5.4.2/dialog/close_then
#			mgs:v5.4.2/casing/main [ as @n[type=item,tag=mgs.new] ]
#

data modify entity @s {} merge from storage mgs:temp casing
tag @s remove mgs.new

