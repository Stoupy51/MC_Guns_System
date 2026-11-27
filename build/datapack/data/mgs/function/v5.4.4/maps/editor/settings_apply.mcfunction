
#> mgs:v5.4.4/maps/editor/settings_apply
#
# @within	mgs:v5.4.4/dialog/close_then
#			string in mgs:v5.4.4/maps/editor/settings {name:\"$(name)\",description:\"$(description)\",dimension:\"$(dimension)\",x:$(x),y:$(y),z:$(z)}
#
# @args		name (string)
#			description (string)
#			dimension (string)
#			x (unknown)
#			y (unknown)
#			z (unknown)
#

$data modify storage mgs:temp map_settings.fields set value {name:"$(name)",description:"$(description)",dimension:"$(dimension)",base_coordinates:[$(x),$(y),$(z)]}
function mgs:v5.4.4/maps/editor/settings_write with storage mgs:temp map_settings.target
tellraw @s [[{"text":"","color":"gold"},"[",{"translate":"mgs","fallback":"MGS"},"] "],{"translate":"mgs.map_settings_saved","fallback":"Map settings saved.","color":"green"}]

