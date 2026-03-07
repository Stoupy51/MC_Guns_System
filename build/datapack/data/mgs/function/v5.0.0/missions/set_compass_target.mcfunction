
#> mgs:v5.0.0/missions/set_compass_target
#
# @executed	at @s
#
# @within	mgs:v5.0.0/missions/update_compass with storage mgs:temp _compass
#
# @args		x (unknown)
#			y (unknown)
#			z (unknown)
#

$item replace entity @s hotbar.3 with compass[lodestone_tracker={target:{pos:[I;$(x),$(y),$(z)],dimension:"minecraft:overworld"},tracked:false},custom_data={mgs:{compass:true}}]

