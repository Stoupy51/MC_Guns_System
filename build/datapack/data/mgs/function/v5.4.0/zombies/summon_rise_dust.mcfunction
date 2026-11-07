
#> mgs:v5.4.0/zombies/summon_rise_dust
#
# @within	mgs:v5.4.0/dialog/close_then
#			mgs:v5.4.0/zombies/arrival/floor {block_y:"-1"}
#			mgs:v5.4.0/zombies/arrival/ceiling {block_y:"0"} [ positioned ~ ~2 ~ ]
#			mgs:v5.4.0/zombies/arrival/rescued {block_y:"0"} [ positioned ~ ~2 ~ ]
#			mgs:v5.4.0/zombies/arrival/rescued {block_y:"-1"}
#
# @args		block_y (string)
#

$execute positioned ~ ~$(block_y) ~ run function #bs.block:get_type
summon minecraft:marker ~ ~ ~ {Tags:["mgs.zb_rise_dust","mgs.zombies_entity","mgs.zb_rise_dust_new"]}
data modify entity @n[tag=mgs.zb_rise_dust_new] data.block set from storage bs:out block.type
scoreboard players operation @n[tag=mgs.zb_rise_dust_new] mgs.zb.rise_tick = @s mgs.zb.rise_tick
tag @n[tag=mgs.zb_rise_dust_new] remove mgs.zb_rise_dust_new

