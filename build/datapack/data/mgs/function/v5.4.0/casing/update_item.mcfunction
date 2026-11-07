
#> mgs:v5.4.0/casing/update_item
#
# @within	mgs:v5.4.0/dialog/close_then
#			mgs:v5.4.0/casing/main [ as @n[type=item,tag=mgs.new] ]
#

data modify entity @s {} merge from storage mgs:temp casing
tag @s remove mgs.new

