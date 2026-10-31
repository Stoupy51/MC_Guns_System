
#> mgs:v5.3.0/stats/board/announce
#
# @within	mgs:v5.3.0/stats/board/zb_round_bucket with storage mgs:temp _lb
#
# @args		name (unknown)
#			value (unknown)
#			n (unknown)
#			rank (unknown)
#

$tellraw $(name) [[{"text":"","color":"gold"},"[",{"translate":"mgs","fallback":"MGS"},"] "],{"translate":"mgs.new_record","fallback":"New record! ","color":"gold","bold":true},{"text":"Round $(value) with $(n) players on this map, rank #$(rank)","color":"yellow"}]

