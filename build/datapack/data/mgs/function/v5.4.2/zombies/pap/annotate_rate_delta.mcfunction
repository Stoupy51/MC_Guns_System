
#> mgs:v5.4.2/zombies/pap/annotate_rate_delta
#
# @within	mgs:v5.4.2/dialog/close_then
#			mgs:v5.4.2/zombies/pap/annotate_fire_rate_line
#

data modify storage mgs:temp _pap_ann.suffix set value ""

scoreboard players operation #pap_whole mgs.data = #pap_rate_new mgs.data
scoreboard players operation #pap_whole mgs.data /= #10 mgs.data
scoreboard players operation #pap_dec mgs.data = #pap_rate_new mgs.data
scoreboard players operation #pap_dec mgs.data %= #10 mgs.data

execute store result storage mgs:temp _pap_ann.whole int 1 run scoreboard players get #pap_whole mgs.data
execute store result storage mgs:temp _pap_ann.dec int 1 run scoreboard players get #pap_dec mgs.data
function mgs:v5.4.2/zombies/pap/annotate_append_dec with storage mgs:temp _pap_ann

