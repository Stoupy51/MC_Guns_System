
#> mgs:v5.0.0/zombies/traps/place_at
#
# @within	mgs:v5.0.0/zombies/traps/setup_iter with storage mgs:temp _trap
#
# @args		ix (unknown)
#			iy (unknown)
#			iz (unknown)
#			cx (unknown)
#			cy (unknown)
#			cz (unknown)
#

# Summon interaction entity at offset position
$summon minecraft:interaction $(ix) $(iy) $(iz) {width:1.0f,height:1.0f,response:true,Tags:["mgs.trap_interact","mgs.gm_entity","bs.entity.interaction","_trap_new_i","_trap_new_bs"]}

# Summon marker entity at trap center
$summon minecraft:marker $(cx) $(cy) $(cz) {Tags:["mgs.trap_center","mgs.gm_entity","_trap_new_m"]}

