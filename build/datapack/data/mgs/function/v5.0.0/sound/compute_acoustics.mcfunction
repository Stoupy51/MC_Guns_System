
#> mgs:v5.0.0/sound/compute_acoustics
#
# @within	mgs:v5.0.0/player/tick
#

# Initialize acoustics score
scoreboard players set #acoustics mgs.data 0

# Compute it
execute if block ~ ~1 ~ #mgs:v5.0.0/outside if block ~ ~2 ~ #mgs:v5.0.0/outside if block ~ ~3 ~ #mgs:v5.0.0/outside run scoreboard players add #acoustics mgs.data 8
execute if block ~ ~4 ~ #mgs:v5.0.0/outside if block ~ ~5 ~ #mgs:v5.0.0/outside if block ~ ~6 ~ #mgs:v5.0.0/outside run scoreboard players add #acoustics mgs.data 8
execute if block ~1 ~1 ~ #mgs:v5.0.0/outside if block ~2 ~1 ~ #mgs:v5.0.0/outside if block ~3 ~1 ~ #mgs:v5.0.0/outside if block ~1 ~2 ~ #mgs:v5.0.0/outside if block ~2 ~2 ~ #mgs:v5.0.0/outside if block ~3 ~2 ~ #mgs:v5.0.0/outside run scoreboard players add #acoustics mgs.data 4
execute if block ~-1 ~1 ~ #mgs:v5.0.0/outside if block ~-2 ~1 ~ #mgs:v5.0.0/outside if block ~-3 ~1 ~ #mgs:v5.0.0/outside if block ~-1 ~2 ~ #mgs:v5.0.0/outside if block ~-2 ~2 ~ #mgs:v5.0.0/outside if block ~-3 ~2 ~ #mgs:v5.0.0/outside run scoreboard players add #acoustics mgs.data 4
execute if block ~ ~1 ~1 #mgs:v5.0.0/outside if block ~ ~1 ~2 #mgs:v5.0.0/outside if block ~ ~1 ~3 #mgs:v5.0.0/outside if block ~ ~2 ~1 #mgs:v5.0.0/outside if block ~ ~2 ~2 #mgs:v5.0.0/outside if block ~ ~2 ~3 #mgs:v5.0.0/outside run scoreboard players add #acoustics mgs.data 4
execute if block ~ ~1 ~-1 #mgs:v5.0.0/outside if block ~ ~1 ~-2 #mgs:v5.0.0/outside if block ~ ~1 ~-3 #mgs:v5.0.0/outside if block ~ ~2 ~-1 #mgs:v5.0.0/outside if block ~ ~2 ~-2 #mgs:v5.0.0/outside if block ~ ~2 ~-3 #mgs:v5.0.0/outside run scoreboard players add #acoustics mgs.data 4
execute if block ~1 ~1 ~1 #mgs:v5.0.0/outside if block ~2 ~1 ~2 #mgs:v5.0.0/outside if block ~3 ~1 ~3 #mgs:v5.0.0/outside if block ~1 ~2 ~1 #mgs:v5.0.0/outside if block ~2 ~2 ~2 #mgs:v5.0.0/outside if block ~3 ~2 ~3 #mgs:v5.0.0/outside run scoreboard players add #acoustics mgs.data 4
execute if block ~-1 ~1 ~1 #mgs:v5.0.0/outside if block ~-2 ~1 ~2 #mgs:v5.0.0/outside if block ~-3 ~1 ~3 #mgs:v5.0.0/outside if block ~-1 ~2 ~1 #mgs:v5.0.0/outside if block ~-2 ~2 ~2 #mgs:v5.0.0/outside if block ~-3 ~2 ~3 #mgs:v5.0.0/outside run scoreboard players add #acoustics mgs.data 4
execute if block ~1 ~1 ~-1 #mgs:v5.0.0/outside if block ~2 ~1 ~-2 #mgs:v5.0.0/outside if block ~3 ~1 ~-3 #mgs:v5.0.0/outside if block ~1 ~2 ~-1 #mgs:v5.0.0/outside if block ~2 ~2 ~-2 #mgs:v5.0.0/outside if block ~3 ~2 ~-3 #mgs:v5.0.0/outside run scoreboard players add #acoustics mgs.data 4
execute if block ~-1 ~1 ~-1 #mgs:v5.0.0/outside if block ~-2 ~1 ~-2 #mgs:v5.0.0/outside if block ~-3 ~1 ~-3 #mgs:v5.0.0/outside if block ~-1 ~2 ~-1 #mgs:v5.0.0/outside if block ~-2 ~2 ~-2 #mgs:v5.0.0/outside if block ~-3 ~2 ~-3 #mgs:v5.0.0/outside run scoreboard players add #acoustics mgs.data 4
execute if block ~1 ~3 ~ #mgs:v5.0.0/outside if block ~2 ~3 ~ #mgs:v5.0.0/outside if block ~3 ~3 ~ #mgs:v5.0.0/outside if block ~1 ~4 ~ #mgs:v5.0.0/outside if block ~2 ~4 ~ #mgs:v5.0.0/outside if block ~3 ~4 ~ #mgs:v5.0.0/outside run scoreboard players add #acoustics mgs.data 4
execute if block ~-1 ~3 ~ #mgs:v5.0.0/outside if block ~-2 ~3 ~ #mgs:v5.0.0/outside if block ~-3 ~3 ~ #mgs:v5.0.0/outside if block ~-1 ~4 ~ #mgs:v5.0.0/outside if block ~-2 ~4 ~ #mgs:v5.0.0/outside if block ~-3 ~4 ~ #mgs:v5.0.0/outside run scoreboard players add #acoustics mgs.data 4
execute if block ~ ~3 ~1 #mgs:v5.0.0/outside if block ~ ~3 ~2 #mgs:v5.0.0/outside if block ~ ~3 ~3 #mgs:v5.0.0/outside if block ~ ~4 ~1 #mgs:v5.0.0/outside if block ~ ~4 ~2 #mgs:v5.0.0/outside if block ~ ~4 ~3 #mgs:v5.0.0/outside run scoreboard players add #acoustics mgs.data 4
execute if block ~ ~3 ~-1 #mgs:v5.0.0/outside if block ~ ~3 ~-2 #mgs:v5.0.0/outside if block ~ ~3 ~-3 #mgs:v5.0.0/outside if block ~ ~4 ~-1 #mgs:v5.0.0/outside if block ~ ~4 ~-2 #mgs:v5.0.0/outside if block ~ ~4 ~-3 #mgs:v5.0.0/outside run scoreboard players add #acoustics mgs.data 4
execute if block ~1 ~3 ~1 #mgs:v5.0.0/outside if block ~2 ~3 ~2 #mgs:v5.0.0/outside if block ~3 ~3 ~3 #mgs:v5.0.0/outside if block ~1 ~4 ~1 #mgs:v5.0.0/outside if block ~2 ~4 ~2 #mgs:v5.0.0/outside if block ~3 ~4 ~3 #mgs:v5.0.0/outside run scoreboard players add #acoustics mgs.data 4
execute if block ~-1 ~3 ~1 #mgs:v5.0.0/outside if block ~-2 ~3 ~2 #mgs:v5.0.0/outside if block ~-3 ~3 ~3 #mgs:v5.0.0/outside if block ~-1 ~4 ~1 #mgs:v5.0.0/outside if block ~-2 ~4 ~2 #mgs:v5.0.0/outside if block ~-3 ~4 ~3 #mgs:v5.0.0/outside run scoreboard players add #acoustics mgs.data 4
execute if block ~1 ~3 ~-1 #mgs:v5.0.0/outside if block ~2 ~3 ~-2 #mgs:v5.0.0/outside if block ~3 ~3 ~-3 #mgs:v5.0.0/outside if block ~1 ~4 ~-1 #mgs:v5.0.0/outside if block ~2 ~4 ~-2 #mgs:v5.0.0/outside if block ~3 ~4 ~-3 #mgs:v5.0.0/outside run scoreboard players add #acoustics mgs.data 4
execute if block ~-1 ~3 ~-1 #mgs:v5.0.0/outside if block ~-2 ~3 ~-2 #mgs:v5.0.0/outside if block ~-3 ~3 ~-3 #mgs:v5.0.0/outside if block ~-1 ~4 ~-1 #mgs:v5.0.0/outside if block ~-2 ~4 ~-2 #mgs:v5.0.0/outside if block ~-3 ~4 ~-3 #mgs:v5.0.0/outside run scoreboard players add #acoustics mgs.data 4
execute if block ~1 ~5 ~ #mgs:v5.0.0/outside if block ~2 ~5 ~ #mgs:v5.0.0/outside if block ~1 ~6 ~ #mgs:v5.0.0/outside if block ~2 ~6 ~ #mgs:v5.0.0/outside run scoreboard players add #acoustics mgs.data 6
execute if block ~-1 ~5 ~ #mgs:v5.0.0/outside if block ~-2 ~5 ~ #mgs:v5.0.0/outside if block ~-1 ~6 ~ #mgs:v5.0.0/outside if block ~-2 ~6 ~ #mgs:v5.0.0/outside run scoreboard players add #acoustics mgs.data 6
execute if block ~ ~5 ~1 #mgs:v5.0.0/outside if block ~ ~5 ~2 #mgs:v5.0.0/outside if block ~ ~6 ~1 #mgs:v5.0.0/outside if block ~ ~6 ~2 #mgs:v5.0.0/outside run scoreboard players add #acoustics mgs.data 6
execute if block ~ ~5 ~-1 #mgs:v5.0.0/outside if block ~ ~5 ~-2 #mgs:v5.0.0/outside if block ~ ~6 ~-1 #mgs:v5.0.0/outside if block ~ ~6 ~-2 #mgs:v5.0.0/outside run scoreboard players add #acoustics mgs.data 6
execute if block ~1 ~5 ~1 #mgs:v5.0.0/outside if block ~2 ~5 ~2 #mgs:v5.0.0/outside if block ~1 ~6 ~1 #mgs:v5.0.0/outside if block ~2 ~6 ~2 #mgs:v5.0.0/outside run scoreboard players add #acoustics mgs.data 6
execute if block ~-1 ~5 ~1 #mgs:v5.0.0/outside if block ~-2 ~5 ~2 #mgs:v5.0.0/outside if block ~-1 ~6 ~1 #mgs:v5.0.0/outside if block ~-2 ~6 ~2 #mgs:v5.0.0/outside run scoreboard players add #acoustics mgs.data 6
execute if block ~1 ~5 ~-1 #mgs:v5.0.0/outside if block ~2 ~5 ~-2 #mgs:v5.0.0/outside if block ~1 ~6 ~-1 #mgs:v5.0.0/outside if block ~2 ~6 ~-2 #mgs:v5.0.0/outside run scoreboard players add #acoustics mgs.data 6
execute if block ~-1 ~5 ~-1 #mgs:v5.0.0/outside if block ~-2 ~5 ~-2 #mgs:v5.0.0/outside if block ~-1 ~6 ~-1 #mgs:v5.0.0/outside if block ~-2 ~6 ~-2 #mgs:v5.0.0/outside run scoreboard players add #acoustics mgs.data 6
execute if block ~2 ~1 ~1 #mgs:v5.0.0/outside if block ~2 ~2 ~1 #mgs:v5.0.0/outside if block ~2 ~1 ~-1 #mgs:v5.0.0/outside if block ~2 ~2 ~-1 #mgs:v5.0.0/outside run scoreboard players add #acoustics mgs.data 4
execute if block ~-2 ~1 ~1 #mgs:v5.0.0/outside if block ~-2 ~2 ~1 #mgs:v5.0.0/outside if block ~-2 ~1 ~-1 #mgs:v5.0.0/outside if block ~-2 ~2 ~-1 #mgs:v5.0.0/outside run scoreboard players add #acoustics mgs.data 4
execute if block ~1 ~1 ~2 #mgs:v5.0.0/outside if block ~1 ~2 ~2 #mgs:v5.0.0/outside if block ~-1 ~1 ~2 #mgs:v5.0.0/outside if block ~-1 ~2 ~2 #mgs:v5.0.0/outside run scoreboard players add #acoustics mgs.data 4
execute if block ~1 ~1 ~-2 #mgs:v5.0.0/outside if block ~1 ~2 ~-2 #mgs:v5.0.0/outside if block ~-1 ~1 ~-2 #mgs:v5.0.0/outside if block ~-1 ~2 ~-2 #mgs:v5.0.0/outside run scoreboard players add #acoustics mgs.data 4
execute if block ~2 ~3 ~1 #mgs:v5.0.0/outside if block ~2 ~4 ~1 #mgs:v5.0.0/outside if block ~2 ~3 ~-1 #mgs:v5.0.0/outside if block ~2 ~4 ~-1 #mgs:v5.0.0/outside run scoreboard players add #acoustics mgs.data 6
execute if block ~-2 ~3 ~1 #mgs:v5.0.0/outside if block ~-2 ~4 ~1 #mgs:v5.0.0/outside if block ~-2 ~3 ~-1 #mgs:v5.0.0/outside if block ~-2 ~4 ~-1 #mgs:v5.0.0/outside run scoreboard players add #acoustics mgs.data 6
execute if block ~1 ~3 ~2 #mgs:v5.0.0/outside if block ~1 ~4 ~2 #mgs:v5.0.0/outside if block ~-1 ~3 ~2 #mgs:v5.0.0/outside if block ~-1 ~4 ~2 #mgs:v5.0.0/outside run scoreboard players add #acoustics mgs.data 6
execute if block ~1 ~3 ~-2 #mgs:v5.0.0/outside if block ~1 ~4 ~-2 #mgs:v5.0.0/outside if block ~-1 ~3 ~-2 #mgs:v5.0.0/outside if block ~-1 ~4 ~-2 #mgs:v5.0.0/outside run scoreboard players add #acoustics mgs.data 6
execute if block ~2 ~5 ~1 #mgs:v5.0.0/outside if block ~2 ~6 ~1 #mgs:v5.0.0/outside if block ~2 ~5 ~-1 #mgs:v5.0.0/outside if block ~2 ~6 ~-1 #mgs:v5.0.0/outside run scoreboard players add #acoustics mgs.data 8
execute if block ~-2 ~5 ~1 #mgs:v5.0.0/outside if block ~-2 ~6 ~1 #mgs:v5.0.0/outside if block ~-2 ~5 ~-1 #mgs:v5.0.0/outside if block ~-2 ~6 ~-1 #mgs:v5.0.0/outside run scoreboard players add #acoustics mgs.data 8
execute if block ~1 ~5 ~2 #mgs:v5.0.0/outside if block ~1 ~6 ~2 #mgs:v5.0.0/outside if block ~-1 ~5 ~2 #mgs:v5.0.0/outside if block ~-1 ~6 ~2 #mgs:v5.0.0/outside run scoreboard players add #acoustics mgs.data 8
execute if block ~1 ~5 ~-2 #mgs:v5.0.0/outside if block ~1 ~6 ~-2 #mgs:v5.0.0/outside if block ~-1 ~5 ~-2 #mgs:v5.0.0/outside if block ~-1 ~6 ~-2 #mgs:v5.0.0/outside run scoreboard players add #acoustics mgs.data 8

# Turn score into acoustics level
scoreboard players set @s mgs.acoustics_level 0
execute if score #acoustics mgs.data matches 121..155 run scoreboard players set @s mgs.acoustics_level 1
execute if score #acoustics mgs.data matches 86..120 run scoreboard players set @s mgs.acoustics_level 2
execute if score #acoustics mgs.data matches 51..85 run scoreboard players set @s mgs.acoustics_level 3
execute if score #acoustics mgs.data matches ..50 run scoreboard players set @s mgs.acoustics_level 4
execute anchored eyes positioned ^ ^ ^ if block ~ ~ ~ #mgs:v5.0.0/sounds/water run scoreboard players set @s mgs.acoustics_level 5

