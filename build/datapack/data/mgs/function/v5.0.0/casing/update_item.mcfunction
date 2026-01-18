
#> mgs:v5.0.0/casing/update_item
#
# @executed	as @n[type=item,tag=mgs.new]
#
# @within	mgs:v5.0.0/casing/main [ as @n[type=item,tag=mgs.new] ]
#

data modify entity @s {} merge from storage mgs:temp casing
tag @s remove mgs.new

