
#> mgs:v5.3.0/zombies/mystery_box/pool/read_weights
#
# @within	mgs:v5.3.0/zombies/mystery_box/pool/save_global {ak47:$(ak47),m16a4:$(m16a4),famas:$(famas),aug:$(aug),m4a1:$(m4a1),fnfal:$(fnfal),g3a3:$(g3a3),scar17:$(scar17),mp5:$(mp5),mp7:$(mp7),mac10:$(mac10),ppsh41:$(ppsh41),sten:$(sten),m249:$(m249),rpk:$(rpk),svd:$(svd),m82:$(m82),mosin:$(mosin),m24:$(m24),spas12:$(spas12),m500:$(m500),m590:$(m590),rpg7:$(rpg7),m1911:$(m1911),m9:$(m9),deagle:$(deagle),makarov:$(makarov),glock17:$(glock17),glock18:$(glock18),vz61:$(vz61),ray_gun:$(ray_gun),monkey_bomb:$(monkey_bomb)}
#			mgs:v5.3.0/zombies/mystery_box/pool/save_map {ak47:$(ak47),m16a4:$(m16a4),famas:$(famas),aug:$(aug),m4a1:$(m4a1),fnfal:$(fnfal),g3a3:$(g3a3),scar17:$(scar17),mp5:$(mp5),mp7:$(mp7),mac10:$(mac10),ppsh41:$(ppsh41),sten:$(sten),m249:$(m249),rpk:$(rpk),svd:$(svd),m82:$(m82),mosin:$(mosin),m24:$(m24),spas12:$(spas12),m500:$(m500),m590:$(m590),rpg7:$(rpg7),m1911:$(m1911),m9:$(m9),deagle:$(deagle),makarov:$(makarov),glock17:$(glock17),glock18:$(glock18),vz61:$(vz61),ray_gun:$(ray_gun),monkey_bomb:$(monkey_bomb)}
#
# @args		ak47 (unknown)
#			m16a4 (unknown)
#			famas (unknown)
#			aug (unknown)
#			m4a1 (unknown)
#			fnfal (unknown)
#			g3a3 (unknown)
#			scar17 (unknown)
#			mp5 (unknown)
#			mp7 (unknown)
#			mac10 (unknown)
#			ppsh41 (unknown)
#			sten (unknown)
#			m249 (unknown)
#			rpk (unknown)
#			svd (unknown)
#			m82 (unknown)
#			mosin (unknown)
#			m24 (unknown)
#			spas12 (unknown)
#			m500 (unknown)
#			m590 (unknown)
#			rpg7 (unknown)
#			m1911 (unknown)
#			m9 (unknown)
#			deagle (unknown)
#			makarov (unknown)
#			glock17 (unknown)
#			glock18 (unknown)
#			vz61 (unknown)
#			ray_gun (unknown)
#			monkey_bomb (unknown)
#

data modify storage mgs:temp _mb_pool set value [{weapon_id:"ak47",weight:0},{weapon_id:"m16a4",weight:0},{weapon_id:"famas",weight:0},{weapon_id:"aug",weight:0},{weapon_id:"m4a1",weight:0},{weapon_id:"fnfal",weight:0},{weapon_id:"g3a3",weight:0},{weapon_id:"scar17",weight:0},{weapon_id:"mp5",weight:0},{weapon_id:"mp7",weight:0},{weapon_id:"mac10",weight:0},{weapon_id:"ppsh41",weight:0},{weapon_id:"sten",weight:0},{weapon_id:"m249",weight:0},{weapon_id:"rpk",weight:0},{weapon_id:"svd",weight:0},{weapon_id:"m82",weight:0},{weapon_id:"mosin",weight:0},{weapon_id:"m24",weight:0},{weapon_id:"spas12",weight:0},{weapon_id:"m500",weight:0},{weapon_id:"m590",weight:0},{weapon_id:"rpg7",weight:0},{weapon_id:"m1911",weight:0},{weapon_id:"m9",weight:0},{weapon_id:"deagle",weight:0},{weapon_id:"makarov",weight:0},{weapon_id:"glock17",weight:0},{weapon_id:"glock18",weight:0},{weapon_id:"vz61",weight:0},{weapon_id:"ray_gun",weight:0},{weapon_id:"monkey_bomb",weight:0}]
$data modify storage mgs:temp _mb_w set value $(ak47)
execute store result storage mgs:temp _mb_pool[{weapon_id:"ak47"}].weight int 1 run data get storage mgs:temp _mb_w
$data modify storage mgs:temp _mb_w set value $(m16a4)
execute store result storage mgs:temp _mb_pool[{weapon_id:"m16a4"}].weight int 1 run data get storage mgs:temp _mb_w
$data modify storage mgs:temp _mb_w set value $(famas)
execute store result storage mgs:temp _mb_pool[{weapon_id:"famas"}].weight int 1 run data get storage mgs:temp _mb_w
$data modify storage mgs:temp _mb_w set value $(aug)
execute store result storage mgs:temp _mb_pool[{weapon_id:"aug"}].weight int 1 run data get storage mgs:temp _mb_w
$data modify storage mgs:temp _mb_w set value $(m4a1)
execute store result storage mgs:temp _mb_pool[{weapon_id:"m4a1"}].weight int 1 run data get storage mgs:temp _mb_w
$data modify storage mgs:temp _mb_w set value $(fnfal)
execute store result storage mgs:temp _mb_pool[{weapon_id:"fnfal"}].weight int 1 run data get storage mgs:temp _mb_w
$data modify storage mgs:temp _mb_w set value $(g3a3)
execute store result storage mgs:temp _mb_pool[{weapon_id:"g3a3"}].weight int 1 run data get storage mgs:temp _mb_w
$data modify storage mgs:temp _mb_w set value $(scar17)
execute store result storage mgs:temp _mb_pool[{weapon_id:"scar17"}].weight int 1 run data get storage mgs:temp _mb_w
$data modify storage mgs:temp _mb_w set value $(mp5)
execute store result storage mgs:temp _mb_pool[{weapon_id:"mp5"}].weight int 1 run data get storage mgs:temp _mb_w
$data modify storage mgs:temp _mb_w set value $(mp7)
execute store result storage mgs:temp _mb_pool[{weapon_id:"mp7"}].weight int 1 run data get storage mgs:temp _mb_w
$data modify storage mgs:temp _mb_w set value $(mac10)
execute store result storage mgs:temp _mb_pool[{weapon_id:"mac10"}].weight int 1 run data get storage mgs:temp _mb_w
$data modify storage mgs:temp _mb_w set value $(ppsh41)
execute store result storage mgs:temp _mb_pool[{weapon_id:"ppsh41"}].weight int 1 run data get storage mgs:temp _mb_w
$data modify storage mgs:temp _mb_w set value $(sten)
execute store result storage mgs:temp _mb_pool[{weapon_id:"sten"}].weight int 1 run data get storage mgs:temp _mb_w
$data modify storage mgs:temp _mb_w set value $(m249)
execute store result storage mgs:temp _mb_pool[{weapon_id:"m249"}].weight int 1 run data get storage mgs:temp _mb_w
$data modify storage mgs:temp _mb_w set value $(rpk)
execute store result storage mgs:temp _mb_pool[{weapon_id:"rpk"}].weight int 1 run data get storage mgs:temp _mb_w
$data modify storage mgs:temp _mb_w set value $(svd)
execute store result storage mgs:temp _mb_pool[{weapon_id:"svd"}].weight int 1 run data get storage mgs:temp _mb_w
$data modify storage mgs:temp _mb_w set value $(m82)
execute store result storage mgs:temp _mb_pool[{weapon_id:"m82"}].weight int 1 run data get storage mgs:temp _mb_w
$data modify storage mgs:temp _mb_w set value $(mosin)
execute store result storage mgs:temp _mb_pool[{weapon_id:"mosin"}].weight int 1 run data get storage mgs:temp _mb_w
$data modify storage mgs:temp _mb_w set value $(m24)
execute store result storage mgs:temp _mb_pool[{weapon_id:"m24"}].weight int 1 run data get storage mgs:temp _mb_w
$data modify storage mgs:temp _mb_w set value $(spas12)
execute store result storage mgs:temp _mb_pool[{weapon_id:"spas12"}].weight int 1 run data get storage mgs:temp _mb_w
$data modify storage mgs:temp _mb_w set value $(m500)
execute store result storage mgs:temp _mb_pool[{weapon_id:"m500"}].weight int 1 run data get storage mgs:temp _mb_w
$data modify storage mgs:temp _mb_w set value $(m590)
execute store result storage mgs:temp _mb_pool[{weapon_id:"m590"}].weight int 1 run data get storage mgs:temp _mb_w
$data modify storage mgs:temp _mb_w set value $(rpg7)
execute store result storage mgs:temp _mb_pool[{weapon_id:"rpg7"}].weight int 1 run data get storage mgs:temp _mb_w
$data modify storage mgs:temp _mb_w set value $(m1911)
execute store result storage mgs:temp _mb_pool[{weapon_id:"m1911"}].weight int 1 run data get storage mgs:temp _mb_w
$data modify storage mgs:temp _mb_w set value $(m9)
execute store result storage mgs:temp _mb_pool[{weapon_id:"m9"}].weight int 1 run data get storage mgs:temp _mb_w
$data modify storage mgs:temp _mb_w set value $(deagle)
execute store result storage mgs:temp _mb_pool[{weapon_id:"deagle"}].weight int 1 run data get storage mgs:temp _mb_w
$data modify storage mgs:temp _mb_w set value $(makarov)
execute store result storage mgs:temp _mb_pool[{weapon_id:"makarov"}].weight int 1 run data get storage mgs:temp _mb_w
$data modify storage mgs:temp _mb_w set value $(glock17)
execute store result storage mgs:temp _mb_pool[{weapon_id:"glock17"}].weight int 1 run data get storage mgs:temp _mb_w
$data modify storage mgs:temp _mb_w set value $(glock18)
execute store result storage mgs:temp _mb_pool[{weapon_id:"glock18"}].weight int 1 run data get storage mgs:temp _mb_w
$data modify storage mgs:temp _mb_w set value $(vz61)
execute store result storage mgs:temp _mb_pool[{weapon_id:"vz61"}].weight int 1 run data get storage mgs:temp _mb_w
$data modify storage mgs:temp _mb_w set value $(ray_gun)
execute store result storage mgs:temp _mb_pool[{weapon_id:"ray_gun"}].weight int 1 run data get storage mgs:temp _mb_w
$data modify storage mgs:temp _mb_w set value $(monkey_bomb)
execute store result storage mgs:temp _mb_pool[{weapon_id:"monkey_bomb"}].weight int 1 run data get storage mgs:temp _mb_w

