
#> mgs:v5.0.1/utils/coord_stick_print
#
# @executed	as @a[tag=mgs.coord_stick_user,limit=1]
#
# @within	mgs:v5.0.1/utils/coord_stick_relative with storage mgs:temp coord_stick.result [ as @a[tag=mgs.coord_stick_user,limit=1] ]
#
# @args		x (int)
#			y (int)
#			z (int)
#

$tellraw @s [[{"text":"","color":"gold"},"[",{"translate":"mgs"},"] "],{"text":"positioned ~$(x) ~$(y) ~$(z)","color":"aqua","click_event":{"action":"copy_to_clipboard","value":"positioned ~$(x) ~$(y) ~$(z)"},"hover_event":{"action":"show_text","value":"Click to copy"}}]

