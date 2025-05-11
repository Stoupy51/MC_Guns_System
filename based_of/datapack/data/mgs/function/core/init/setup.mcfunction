# clean previous session
schedule function mgs:core/init/cleanup 60t append
schedule function mgs:core/init/order_check 60t append

# init constants
scoreboard objectives add C dummy
scoreboard players set -4 C -4
scoreboard players set -2 C -2
scoreboard players set -1 C -1
scoreboard players set 0 C 0
scoreboard players set 1 C 1
scoreboard players set 2 C 2
scoreboard players set 3 C 3
scoreboard players set 4 C 4
scoreboard players set 5 C 5
scoreboard players set 6 C 6
scoreboard players set 7 C 7
scoreboard players set 8 C 8
scoreboard players set 9 C 9
scoreboard players set 10 C 10
scoreboard players set 20 C 20
scoreboard players set 40 C 40
scoreboard players set 100 C 100
scoreboard players set midprime C 73417
scoreboard players set bigprime C 2379673
scoreboard players set 1000 C 1000
scoreboard players set 10000 C 10000

# init variables
scoreboard objectives add V dummy
scoreboard players set v0 V 0
scoreboard players set v1 V 0
scoreboard players set v2 V 0
scoreboard players set v3 V 0
scoreboard players set v4 V 0
scoreboard players set v5 V 0
scoreboard players set v6 V 0
scoreboard players set v7 V 0
scoreboard players set v8 V 0
scoreboard players set v9 V 0
scoreboard players set v10 V 0
scoreboard players set v11 V 0
scoreboard players set v12 V 0
scoreboard players set v13 V 0
scoreboard players set v14 V 0
scoreboard players set v15 V 0
scoreboard players add rand V 0
scoreboard players add randraw V 0
scoreboard players add time V 0

# init settings
execute unless score enableUI V matches 0.. run scoreboard players set enableUI V 1
execute unless score enableTracer V matches 0.. run scoreboard players set enableTracer V 0
execute unless score enableCasing V matches 0.. run scoreboard players set enableCasing V 1
execute unless score enableSwitch V matches 0.. run scoreboard players set enableSwitch V 1
execute unless score enableRecoil V matches 0.. run scoreboard players set enableRecoil V 1
execute unless score enableHBComp V matches 0.. run scoreboard players set enableHBComp V 0
execute unless score enablePlayerHS V matches 0.. run scoreboard players set enablePlayerHS V 1
execute unless score enableMagazines V matches 0.. run scoreboard players set enableMagazines V 1
execute unless score enableEmptyMagazines V matches 0.. run scoreboard players set enableEmptyMagazines V 1
execute unless score enablePlayerDam V matches 0.. run scoreboard players set enablePlayerDam V 1
execute unless score enableShader V matches 0.. run scoreboard players set enableShader V 1
scoreboard players set shaderClearReapp V 8
scoreboard players set shaderZoomReapp V 21
scoreboard players set shaderZoomDelay V 12

# init objectives
scoreboard objectives add shader_delay dummy
scoreboard objectives add shader_pshots dummy
scoreboard objectives add shader_pws dummy
scoreboard objectives add shader_mode dummy

# init other objectives
scoreboard objectives add carrot_click minecraft.used:minecraft.carrot_on_a_stick
scoreboard objectives add carrot_drop minecraft.dropped:minecraft.carrot_on_a_stick
scoreboard objectives add exploded minecraft.killed_by:minecraft.creeper
scoreboard objectives add sneaky minecraft.custom:minecraft.sneak_time
scoreboard objectives add walk minecraft.custom:minecraft.walk_one_cm
scoreboard objectives add sprint minecraft.custom:minecraft.sprint_one_cm
scoreboard objectives add jump minecraft.custom:minecraft.jump
scoreboard objectives add kick dummy
scoreboard objectives add kickdir dummy
scoreboard objectives add timestamp dummy
scoreboard objectives add acoustics dummy
scoreboard objectives add acoustics_level dummy
scoreboard objectives add health dummy
scoreboard objectives add shealth health
scoreboard objectives add phealth dummy
scoreboard objectives add damage dummy
scoreboard objectives add hit_by dummy
scoreboard objectives add deaths deathCount
scoreboard objectives add kills playerKillCount
scoreboard objectives add gunkills dummy
scoreboard objectives add mobkills minecraft.custom:minecraft.mob_kills
scoreboard objectives add mobgunkills dummy
scoreboard objectives add shots dummy
scoreboard objectives add hits dummy
scoreboard objectives add mobhits dummy
scoreboard objectives add headshots dummy
scoreboard objectives add fire dummy
scoreboard objectives add weapon dummy
scoreboard objectives add weapon_id dummy
scoreboard objectives add pweapon_id dummy
scoreboard objectives add pdeaths dummy
scoreboard objectives add decay dummy
scoreboard objectives add cooldown dummy
scoreboard objectives add selector dummy
scoreboard objectives add mag dummy
scoreboard objectives add lim dummy
scoreboard objectives add r dummy
scoreboard objectives add h dummy
scoreboard objectives add dx dummy
scoreboard objectives add dy dummy
scoreboard objectives add dz dummy
scoreboard objectives add ndx dummy
scoreboard objectives add ndy dummy
scoreboard objectives add ndz dummy
scoreboard objectives add tdx dummy
scoreboard objectives add tdz dummy
scoreboard objectives add d dummy
scoreboard objectives add slow dummy
scoreboard objectives add pslow dummy

# init weapon stats
scoreboard objectives add S dummy
function mgs:core/init/weapon_stat

# core/init/reset pseudo-Unique IDs
scoreboard objectives add UID dummy
scoreboard players add _uid_ptr UID 0
scoreboard players set _default UID 0

# init misc
forceload add 0 0
setblock 0 -64 0 minecraft:air
setblock 0 -64 0 minecraft:barrel{Lock:420-69-42-1337-12,Items:[{Slot:1b,id:"minecraft:stone",Count:1b}]}
clone 0 -64 1 0 -64 1 0 -63 0

# init message
tellraw @a [{"text":"Loaded "},{"text":"MGS 4.2","color":"green"},{"text":" for MC 1.19\n"},{"text":"by thebradqq","color":"gray","underlined":true,"clickEvent":{"action":"open_url","value":"https://www.youtube.com/channel/UCQZezU6K1XRePGOZLFoQyKA"}}]