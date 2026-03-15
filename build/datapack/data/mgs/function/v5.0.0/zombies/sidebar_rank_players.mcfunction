
#> mgs:v5.0.0/zombies/sidebar_rank_players
#
# @within	mgs:v5.0.0/zombies/refresh_sidebar
#

execute unless entity @a[tag=mgs.zb_sb_cand] run return 0
execute as @r[tag=mgs.zb_sb_cand] run scoreboard players set @s mgs.zb.sb_rank 1
tag @a[scores={mgs.zb.sb_rank=1}] remove mgs.zb_sb_cand
data modify storage mgs:temp zb_sb append value [{selector:"@a[scores={mgs.zb.sb_rank=1}]",color:"green"},{score:{name:"@a[scores={mgs.zb.sb_rank=1}]",objective:"mgs.zb.points"},color:"yellow"}]

execute unless entity @a[tag=mgs.zb_sb_cand] run return 0
execute as @r[tag=mgs.zb_sb_cand] run scoreboard players set @s mgs.zb.sb_rank 2
tag @a[scores={mgs.zb.sb_rank=2}] remove mgs.zb_sb_cand
data modify storage mgs:temp zb_sb append value [{selector:"@a[scores={mgs.zb.sb_rank=2}]",color:"green"},{score:{name:"@a[scores={mgs.zb.sb_rank=2}]",objective:"mgs.zb.points"},color:"yellow"}]

execute unless entity @a[tag=mgs.zb_sb_cand] run return 0
execute as @r[tag=mgs.zb_sb_cand] run scoreboard players set @s mgs.zb.sb_rank 3
tag @a[scores={mgs.zb.sb_rank=3}] remove mgs.zb_sb_cand
data modify storage mgs:temp zb_sb append value [{selector:"@a[scores={mgs.zb.sb_rank=3}]",color:"green"},{score:{name:"@a[scores={mgs.zb.sb_rank=3}]",objective:"mgs.zb.points"},color:"yellow"}]

execute unless entity @a[tag=mgs.zb_sb_cand] run return 0
execute as @r[tag=mgs.zb_sb_cand] run scoreboard players set @s mgs.zb.sb_rank 4
tag @a[scores={mgs.zb.sb_rank=4}] remove mgs.zb_sb_cand
data modify storage mgs:temp zb_sb append value [{selector:"@a[scores={mgs.zb.sb_rank=4}]",color:"green"},{score:{name:"@a[scores={mgs.zb.sb_rank=4}]",objective:"mgs.zb.points"},color:"yellow"}]

execute unless entity @a[tag=mgs.zb_sb_cand] run return 0
execute as @r[tag=mgs.zb_sb_cand] run scoreboard players set @s mgs.zb.sb_rank 5
tag @a[scores={mgs.zb.sb_rank=5}] remove mgs.zb_sb_cand
data modify storage mgs:temp zb_sb append value [{selector:"@a[scores={mgs.zb.sb_rank=5}]",color:"green"},{score:{name:"@a[scores={mgs.zb.sb_rank=5}]",objective:"mgs.zb.points"},color:"yellow"}]

execute unless entity @a[tag=mgs.zb_sb_cand] run return 0
execute as @r[tag=mgs.zb_sb_cand] run scoreboard players set @s mgs.zb.sb_rank 6
tag @a[scores={mgs.zb.sb_rank=6}] remove mgs.zb_sb_cand
data modify storage mgs:temp zb_sb append value [{selector:"@a[scores={mgs.zb.sb_rank=6}]",color:"green"},{score:{name:"@a[scores={mgs.zb.sb_rank=6}]",objective:"mgs.zb.points"},color:"yellow"}]

execute unless entity @a[tag=mgs.zb_sb_cand] run return 0
execute as @r[tag=mgs.zb_sb_cand] run scoreboard players set @s mgs.zb.sb_rank 7
tag @a[scores={mgs.zb.sb_rank=7}] remove mgs.zb_sb_cand
data modify storage mgs:temp zb_sb append value [{selector:"@a[scores={mgs.zb.sb_rank=7}]",color:"green"},{score:{name:"@a[scores={mgs.zb.sb_rank=7}]",objective:"mgs.zb.points"},color:"yellow"}]

execute unless entity @a[tag=mgs.zb_sb_cand] run return 0
execute as @r[tag=mgs.zb_sb_cand] run scoreboard players set @s mgs.zb.sb_rank 8
tag @a[scores={mgs.zb.sb_rank=8}] remove mgs.zb_sb_cand
data modify storage mgs:temp zb_sb append value [{selector:"@a[scores={mgs.zb.sb_rank=8}]",color:"green"},{score:{name:"@a[scores={mgs.zb.sb_rank=8}]",objective:"mgs.zb.points"},color:"yellow"}]

tag @a remove mgs.zb_sb_cand

