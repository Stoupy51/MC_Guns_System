
#> mgs:v5.0.0/zombies/pap/append_level_to_lore_line
#
# @within	mgs:v5.0.0/zombies/pap/append_level_to_lore_iter with storage mgs:temp _pap_lore
#
# @args		level (unknown)
#

$execute if data storage mgs:temp _pap_lore.line.text unless data storage mgs:temp _pap_lore.line.extra[0] run data modify storage mgs:temp _pap_lore.line.extra set value []
	$execute if data storage mgs:temp _pap_lore.line.text run data modify storage mgs:temp _pap_lore.line.extra append value {"text":" +$(level)","color":"dark_green","italic":false}

