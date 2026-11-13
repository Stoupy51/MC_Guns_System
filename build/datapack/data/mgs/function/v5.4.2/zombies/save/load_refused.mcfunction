
#> mgs:v5.4.2/zombies/save/load_refused
#
# @within	mgs:v5.4.2/dialog/close_then
#			mgs:v5.4.2/zombies/save/load {reason:"This slot is empty."}
#			mgs:v5.4.2/zombies/save/load {reason:"This save comes from a newer version of the pack."}
#			mgs:v5.4.2/zombies/save/load {reason:"The map of this save no longer exists."}
#			mgs:v5.4.2/zombies/save/load {reason:"No player of this save is online."}
#
# @args		reason (string)
#

data remove storage mgs:zombies_saves loading
$tellraw @s [[{"text":"","color":"gold"},"[",{"translate":"mgs","fallback":"MGS"},"] "],{"text":"$(reason)","color":"red"}]

