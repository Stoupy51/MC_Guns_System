
#> mgs:v5.4.4/missions/set_compass_target
#
# @within	mgs:v5.4.4/dialog/close_then
#			mgs:v5.4.4/missions/update_compass with storage mgs:temp _compass
#
# @args		x (unknown)
#			y (unknown)
#			z (unknown)
#			dimension (unknown)
#

$item replace entity @s hotbar.3 with compass[lodestone_tracker={target:{pos:[I;$(x),$(y),$(z)],dimension:"$(dimension)"},tracked:false},custom_data={mgs:{compass:true}}]

