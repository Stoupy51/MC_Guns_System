
#> mgs:v5.4.1/maps/editor/name/rounds_between
#
# @within	mgs:v5.4.1/dialog/close_then
#			mgs:v5.4.1/maps/editor/name/rounds with storage mgs:temp _ed_rounds
#
# @args		min (unknown)
#			max (unknown)
#

$data modify storage mgs:temp _ed_name.rounds set value " r$(min)-$(max)"

