scoreboard players operation v0 V = time V
scoreboard players operation v0 V += @s UID
scoreboard players operation v0 V %= 20 C
execute if score v0 V matches 0 run function mgs:util/room_acoustics_h
scoreboard players set @s acoustics_level 0
execute if score @s acoustics matches 121..155 run scoreboard players set @s acoustics_level 1
execute if score @s acoustics matches 86..120 run scoreboard players set @s acoustics_level 2
execute if score @s acoustics matches 51..85 run scoreboard players set @s acoustics_level 3
execute if score @s acoustics matches ..50 run scoreboard players set @s acoustics_level 4
execute anchored eyes positioned ^ ^ ^ if block ~ ~ ~ #mgs:sounds/water run scoreboard players set @s acoustics_level 5