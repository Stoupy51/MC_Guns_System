
#> mgs:v5.2.0/maps/editor/settings_apply
#
# @within	string in mgs:v5.2.0/maps/editor/settings {name:\"$(name)\",description:\"$(description)\",dimension:\"$(dimension)\"}
#
# @args		name (string)
#			description (string)
#			dimension (string)
#

$data modify storage mgs:temp map_settings.fields set value {name:"$(name)",description:"$(description)",dimension:"$(dimension)"}
function mgs:v5.2.0/maps/editor/settings_write with storage mgs:temp map_settings.target
tellraw @s [[{"text":"","color":"gold"},"[",{"translate":"mgs","fallback":"MGS"},"] "],{"translate":"mgs.map_settings_saved","fallback":"Map settings saved.","color":"green"}]

