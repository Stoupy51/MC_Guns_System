
#> mgs:v5.1.0/zombies/traps/place_at
#
# @within	mgs:v5.1.0/zombies/traps/setup_iter with storage mgs:temp _trap
#
# @args		ix (unknown)
#			iy (unknown)
#			iz (unknown)
#			cx (unknown)
#			cy (unknown)
#			cz (unknown)
#

# height -2.0 makes a downward hitbox, raised 2 blocks right after, so it covers the 2-block turret (as the perk machine does).
$execute positioned $(ix) $(iy) $(iz) run summon minecraft:interaction ~ ~2 ~ {width:1.1f,height:-2.0f,response:true,Tags:["mgs.trap_interact","mgs.gm_entity","bs.entity.interaction","mgs._trap_new_i","mgs._trap_new_bs"]}

$summon minecraft:marker $(cx) $(cy) $(cz) {Tags:["mgs.trap_center","mgs.gm_entity","mgs._trap_new_m"]}

