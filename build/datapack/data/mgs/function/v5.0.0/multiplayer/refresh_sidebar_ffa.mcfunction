
#> mgs:v5.0.0/multiplayer/refresh_sidebar_ffa
#
# @within	mgs:v5.0.0/multiplayer/timer_display
#			mgs:v5.0.0/multiplayer/create_sidebar_ffa
#			mgs:v5.0.0/multiplayer/gamemodes/ffa/on_kill
#

# Initialize sidebar header in storage
data modify storage mgs:temp ffa_sb set value [[{text:" ⏱ ",color:"yellow"},[{score:{name:"#timer_min",objective:"mgs.data"},"color":"yellow"},{text:":"},{score:{name:"#timer_tens",objective:"mgs.data"}},{score:{name:"#timer_ones",objective:"mgs.data"}}]]," ",[{translate: "mgs.first_to",color:"gray"},{score:{name:"#score_limit",objective:"mgs.data"},color:"white"}]," "]

# Reset ranks and tag candidates
scoreboard players set @a mgs.mp.ffa_rank 0
tag @a[scores={mgs.mp.in_game=1..}] add mgs.ffa_candidate

# Rank 1
execute unless entity @a[tag=mgs.ffa_candidate] run return run function mgs:v5.0.0/multiplayer/build_sidebar_ffa with storage mgs:temp
scoreboard players set #ffa_max mgs.data -1
execute as @a[tag=mgs.ffa_candidate] run scoreboard players operation #ffa_max mgs.data > @s mgs.mp.kills
execute as @r[tag=mgs.ffa_candidate] if score @s mgs.mp.kills >= #ffa_max mgs.data run scoreboard players set @s mgs.mp.ffa_rank 1
execute as @a[scores={mgs.mp.ffa_rank=1}] run tag @s remove mgs.ffa_candidate
data modify storage mgs:temp ffa_sb append value [[{text:" 1. ",color:"gold"},{selector:"@a[scores={mgs.mp.ffa_rank=1}]",color:"yellow"}],{score:{name:"@a[scores={mgs.mp.ffa_rank=1}]",objective:"mgs.mp.kills"},color:"white"}]

# Rank 2
execute unless entity @a[tag=mgs.ffa_candidate] run return run function mgs:v5.0.0/multiplayer/build_sidebar_ffa with storage mgs:temp
scoreboard players set #ffa_max mgs.data -1
execute as @a[tag=mgs.ffa_candidate] run scoreboard players operation #ffa_max mgs.data > @s mgs.mp.kills
execute as @r[tag=mgs.ffa_candidate] if score @s mgs.mp.kills >= #ffa_max mgs.data run scoreboard players set @s mgs.mp.ffa_rank 2
execute as @a[scores={mgs.mp.ffa_rank=2}] run tag @s remove mgs.ffa_candidate
data modify storage mgs:temp ffa_sb append value [[{text:" 2. ",color:"gold"},{selector:"@a[scores={mgs.mp.ffa_rank=2}]",color:"yellow"}],{score:{name:"@a[scores={mgs.mp.ffa_rank=2}]",objective:"mgs.mp.kills"},color:"white"}]

# Rank 3
execute unless entity @a[tag=mgs.ffa_candidate] run return run function mgs:v5.0.0/multiplayer/build_sidebar_ffa with storage mgs:temp
scoreboard players set #ffa_max mgs.data -1
execute as @a[tag=mgs.ffa_candidate] run scoreboard players operation #ffa_max mgs.data > @s mgs.mp.kills
execute as @r[tag=mgs.ffa_candidate] if score @s mgs.mp.kills >= #ffa_max mgs.data run scoreboard players set @s mgs.mp.ffa_rank 3
execute as @a[scores={mgs.mp.ffa_rank=3}] run tag @s remove mgs.ffa_candidate
data modify storage mgs:temp ffa_sb append value [[{text:" 3. ",color:"gold"},{selector:"@a[scores={mgs.mp.ffa_rank=3}]",color:"yellow"}],{score:{name:"@a[scores={mgs.mp.ffa_rank=3}]",objective:"mgs.mp.kills"},color:"white"}]

# Rank 4
execute unless entity @a[tag=mgs.ffa_candidate] run return run function mgs:v5.0.0/multiplayer/build_sidebar_ffa with storage mgs:temp
scoreboard players set #ffa_max mgs.data -1
execute as @a[tag=mgs.ffa_candidate] run scoreboard players operation #ffa_max mgs.data > @s mgs.mp.kills
execute as @r[tag=mgs.ffa_candidate] if score @s mgs.mp.kills >= #ffa_max mgs.data run scoreboard players set @s mgs.mp.ffa_rank 4
execute as @a[scores={mgs.mp.ffa_rank=4}] run tag @s remove mgs.ffa_candidate
data modify storage mgs:temp ffa_sb append value [[{text:" 4. ",color:"gold"},{selector:"@a[scores={mgs.mp.ffa_rank=4}]",color:"yellow"}],{score:{name:"@a[scores={mgs.mp.ffa_rank=4}]",objective:"mgs.mp.kills"},color:"white"}]

# Rank 5
execute unless entity @a[tag=mgs.ffa_candidate] run return run function mgs:v5.0.0/multiplayer/build_sidebar_ffa with storage mgs:temp
scoreboard players set #ffa_max mgs.data -1
execute as @a[tag=mgs.ffa_candidate] run scoreboard players operation #ffa_max mgs.data > @s mgs.mp.kills
execute as @r[tag=mgs.ffa_candidate] if score @s mgs.mp.kills >= #ffa_max mgs.data run scoreboard players set @s mgs.mp.ffa_rank 5
execute as @a[scores={mgs.mp.ffa_rank=5}] run tag @s remove mgs.ffa_candidate
data modify storage mgs:temp ffa_sb append value [[{text:" 5. ",color:"gold"},{selector:"@a[scores={mgs.mp.ffa_rank=5}]",color:"yellow"}],{score:{name:"@a[scores={mgs.mp.ffa_rank=5}]",objective:"mgs.mp.kills"},color:"white"}]

# Rank 6
execute unless entity @a[tag=mgs.ffa_candidate] run return run function mgs:v5.0.0/multiplayer/build_sidebar_ffa with storage mgs:temp
scoreboard players set #ffa_max mgs.data -1
execute as @a[tag=mgs.ffa_candidate] run scoreboard players operation #ffa_max mgs.data > @s mgs.mp.kills
execute as @r[tag=mgs.ffa_candidate] if score @s mgs.mp.kills >= #ffa_max mgs.data run scoreboard players set @s mgs.mp.ffa_rank 6
execute as @a[scores={mgs.mp.ffa_rank=6}] run tag @s remove mgs.ffa_candidate
data modify storage mgs:temp ffa_sb append value [[{text:" 6. ",color:"gold"},{selector:"@a[scores={mgs.mp.ffa_rank=6}]",color:"yellow"}],{score:{name:"@a[scores={mgs.mp.ffa_rank=6}]",objective:"mgs.mp.kills"},color:"white"}]

# Rank 7
execute unless entity @a[tag=mgs.ffa_candidate] run return run function mgs:v5.0.0/multiplayer/build_sidebar_ffa with storage mgs:temp
scoreboard players set #ffa_max mgs.data -1
execute as @a[tag=mgs.ffa_candidate] run scoreboard players operation #ffa_max mgs.data > @s mgs.mp.kills
execute as @r[tag=mgs.ffa_candidate] if score @s mgs.mp.kills >= #ffa_max mgs.data run scoreboard players set @s mgs.mp.ffa_rank 7
execute as @a[scores={mgs.mp.ffa_rank=7}] run tag @s remove mgs.ffa_candidate
data modify storage mgs:temp ffa_sb append value [[{text:" 7. ",color:"gold"},{selector:"@a[scores={mgs.mp.ffa_rank=7}]",color:"yellow"}],{score:{name:"@a[scores={mgs.mp.ffa_rank=7}]",objective:"mgs.mp.kills"},color:"white"}]

# Rank 8
execute unless entity @a[tag=mgs.ffa_candidate] run return run function mgs:v5.0.0/multiplayer/build_sidebar_ffa with storage mgs:temp
scoreboard players set #ffa_max mgs.data -1
execute as @a[tag=mgs.ffa_candidate] run scoreboard players operation #ffa_max mgs.data > @s mgs.mp.kills
execute as @r[tag=mgs.ffa_candidate] if score @s mgs.mp.kills >= #ffa_max mgs.data run scoreboard players set @s mgs.mp.ffa_rank 8
execute as @a[scores={mgs.mp.ffa_rank=8}] run tag @s remove mgs.ffa_candidate
data modify storage mgs:temp ffa_sb append value [[{text:" 8. ",color:"gold"},{selector:"@a[scores={mgs.mp.ffa_rank=8}]",color:"yellow"}],{score:{name:"@a[scores={mgs.mp.ffa_rank=8}]",objective:"mgs.mp.kills"},color:"white"}]

# Rank 9
execute unless entity @a[tag=mgs.ffa_candidate] run return run function mgs:v5.0.0/multiplayer/build_sidebar_ffa with storage mgs:temp
scoreboard players set #ffa_max mgs.data -1
execute as @a[tag=mgs.ffa_candidate] run scoreboard players operation #ffa_max mgs.data > @s mgs.mp.kills
execute as @r[tag=mgs.ffa_candidate] if score @s mgs.mp.kills >= #ffa_max mgs.data run scoreboard players set @s mgs.mp.ffa_rank 9
execute as @a[scores={mgs.mp.ffa_rank=9}] run tag @s remove mgs.ffa_candidate
data modify storage mgs:temp ffa_sb append value [[{text:" 9. ",color:"gold"},{selector:"@a[scores={mgs.mp.ffa_rank=9}]",color:"yellow"}],{score:{name:"@a[scores={mgs.mp.ffa_rank=9}]",objective:"mgs.mp.kills"},color:"white"}]

# Rank 10
execute unless entity @a[tag=mgs.ffa_candidate] run return run function mgs:v5.0.0/multiplayer/build_sidebar_ffa with storage mgs:temp
scoreboard players set #ffa_max mgs.data -1
execute as @a[tag=mgs.ffa_candidate] run scoreboard players operation #ffa_max mgs.data > @s mgs.mp.kills
execute as @r[tag=mgs.ffa_candidate] if score @s mgs.mp.kills >= #ffa_max mgs.data run scoreboard players set @s mgs.mp.ffa_rank 10
execute as @a[scores={mgs.mp.ffa_rank=10}] run tag @s remove mgs.ffa_candidate
data modify storage mgs:temp ffa_sb append value [[{text:" 10. ",color:"gold"},{selector:"@a[scores={mgs.mp.ffa_rank=10}]",color:"yellow"}],{score:{name:"@a[scores={mgs.mp.ffa_rank=10}]",objective:"mgs.mp.kills"},color:"white"}]

# Clean up and build
tag @a remove mgs.ffa_candidate
function mgs:v5.0.0/multiplayer/build_sidebar_ffa with storage mgs:temp

