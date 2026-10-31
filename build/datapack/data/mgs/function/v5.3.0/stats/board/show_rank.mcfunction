
#> mgs:v5.3.0/stats/board/show_rank
#
# @executed	as @e[type=player,sort=random] & at @s
#
# @within	mgs:v5.3.0/stats/board/show with storage mgs:temp _lb_rank
#
# @args		k (unknown)
#

$data modify storage mgs:temp dialog.body append value {type:"minecraft:plain_message",contents:["",{translate:"mgs.your_rank",fallback:"Your rank",color:"gray"},": ",{text:"#$(k)",color:"gold"}]}

