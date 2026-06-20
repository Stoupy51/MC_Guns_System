
#> mgs:v5.0.1/zombies/traps/place_at
#
# @within	mgs:v5.0.1/zombies/traps/setup_iter with storage mgs:temp _trap
#
# @args		ix (unknown)
#			iy (unknown)
#			iz (unknown)
#			cx (unknown)
#			cy (unknown)
#			cz (unknown)
#

# Summon interaction entity centred on the block, at the floor. height:-2.0 makes a downward 2-block
# hitbox; setup_iter then raises it 2 blocks (tp ~ ~2 ~) so it covers the 2-block turret from the floor
# up - the same trick the perk machine uses.
$execute positioned $(ix) $(iy) $(iz) run summon minecraft:interaction ~ ~2 ~ {width:1.1f,height:-2.0f,response:true,Tags:["mgs.trap_interact","mgs.gm_entity","bs.entity.interaction","mgs._trap_new_i","mgs._trap_new_bs"]}

# Summon marker entity at trap center
$summon minecraft:marker $(cx) $(cy) $(cz) {Tags:["mgs.trap_center","mgs.gm_entity","mgs._trap_new_m"]}

