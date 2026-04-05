
#> mgs:v5.0.0/zombies/pap/annotate_time_delta
#
# @executed	as @n[tag=mgs.pap_new]
#
# @within	mgs:v5.0.0/zombies/pap/annotate_lore
#

execute store result storage mgs:temp _pap_ann.index int 1 run scoreboard players get #pap_li mgs.data
data modify storage mgs:temp _pap_ann.suffix set value "s"

# Tenths of seconds: new_ticks * 10 / 20
scoreboard players operation #pap_tenths mgs.data = #pap_new mgs.data
scoreboard players operation #pap_tenths mgs.data *= #10 mgs.data
scoreboard players operation #pap_tenths mgs.data /= #20 mgs.data

# Split into whole.decimal
scoreboard players operation #pap_whole mgs.data = #pap_tenths mgs.data
scoreboard players operation #pap_whole mgs.data /= #10 mgs.data
scoreboard players operation #pap_dec mgs.data = #pap_tenths mgs.data
scoreboard players operation #pap_dec mgs.data %= #10 mgs.data

execute store result storage mgs:temp _pap_ann.whole int 1 run scoreboard players get #pap_whole mgs.data
execute store result storage mgs:temp _pap_ann.dec int 1 run scoreboard players get #pap_dec mgs.data
function mgs:v5.0.0/zombies/pap/annotate_append_dec with storage mgs:temp _pap_ann

