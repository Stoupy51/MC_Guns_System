#player init scoreboard
tag @a[tag=logged] remove logged
tag @a[tag=respawn] remove respawn
execute if score doImmResp V matches 2 run gamerule doImmediateRespawn false
execute store result score doImmResp V run gamerule doImmediateRespawn
execute store result score showDeath V run gamerule showDeathMessages
execute store result score time V run time query gametime
execute as @e[type=minecraft:marker,tag=!wm] if score @s timestamp < time V run function mgs:util/marker_dispose
execute as @a[tag=!ini] run function mgs:core/init/player_init
scoreboard players set @a[tag=ini] h 600
execute as @a[tag=ini] at @s positioned ~ ~0.61 ~ run scoreboard players set @s[dx=0,dy=0,dz=0] h 1500
execute as @a[tag=ini] at @s positioned ~ ~1.51 ~ run scoreboard players set @s[dx=0,dy=0,dz=0] h 1850
scoreboard players set @a[tag=ini] r 400
execute as @a[tag=ini,scores={h=1500..,sprint=0,jump=0}] run scoreboard players set @s r 300
execute as @a[tag=ini] run scoreboard players operation @s health = @s shealth
execute as @a[tag=ini,scores={shealth=0}] store result score @s health run data get entity @s Health

#preprocess
execute as @a[tag=!dead] at @s run function mgs:util/room_acoustics
execute if score enableCasing V matches 1.. as @e[type=item,tag=newc,tag=casing] run function mgs:core/casing_update
tag @a[tag=dead,scores={health=1..}] add respawn
scoreboard players set @a[tag=respawn] damage 0
scoreboard players set @a[tag=respawn] fire 0
scoreboard players set @a[tag=respawn] carrot_click 0
scoreboard players set @a[tag=no_shoot] carrot_click 0
tag @a[tag=respawn] remove hs
tag @a[tag=respawn] remove dead
execute as @a if score @s pdeaths < @s deaths run tag @s add dead
execute as @a[tag=exploded,tag=dead,scores={exploded=1..}] run function mgs:core/rocket_killcount
tag @a[tag=exploded] remove exploded
scoreboard players set @a exploded 0
scoreboard players set @a hit_by 0
scoreboard players set @a slow 0
execute as @a[nbt={OnGround:0b}] at @s if block ~ ~-0.07 ~ #mgs:jump run scoreboard players add @s jump 1
execute if score enableHBComp V matches 1 as @a[tag=damaged] run function mgs:util/damage_post
execute as @e[type=item,nbt={Item:{tag:{Gun:1}}}] store result score @s weapon_id run data get entity @s Item.tag.WUID
execute as @a[scores={carrot_drop=1..}] run function mgs:core/q_reload
tag @a[scores={selector=1,cooldown=0}] add reloading
scoreboard players set @a weapon 0
execute as @a[predicate=mgs:gun] store result score @s weapon run data get entity @s SelectedItem.tag.CustomModelData
scoreboard players set @a weapon_id 0
execute as @a[predicate=mgs:gun] run function mgs:core/weapon_id
execute as @a[scores={weapon=1..,weapon_id=0}] run function mgs:core/init/weapon_init

execute if score enableSwitch V matches 1 as @a unless score @s pweapon_id = @s weapon_id run function mgs:core/change_reset
execute if score enableSwitch V matches 0 as @a unless score @s pweapon_id = @s weapon_id run function mgs:core/change_reset_simp

# identify and do weapon fire
execute as @a[tag=!switch,scores={weapon=10..109}] at @s run function mgs:guns/_common/handler_rifle
execute as @a[tag=!switch,scores={weapon=110..209}] at @s run function mgs:guns/_common/handler_pistol
execute as @a[tag=!switch,scores={weapon=210..309}] at @s run function mgs:guns/_common/handler_smg
execute as @a[tag=!switch,scores={weapon=310..409}] at @s run function mgs:guns/_common/handler_shotgun
execute as @a[tag=!switch,scores={weapon=410..509}] at @s run function mgs:guns/_common/handler_sniper
execute as @a[tag=!switch,scores={weapon=510..609}] at @s run function mgs:guns/_common/handler_special
execute if score enableUI V matches 1 run title @a[tag=reloading] actionbar ["",{"text":"reloading..."}]
execute if score enableShader V matches 1.. run function mgs:core/shader
tag @a[tag=rstop] remove rstop
tag @a[tag=switch,scores={cooldown=0}] remove switch

# postprocess
execute as @e[type=minecraft:marker,tag=fired] at @s run function mgs:core/bullet_physics
execute as @e[type=minecraft:marker,tag=rocket] at @s run function mgs:core/rocket_physics
scoreboard players set @a bow_click 0
scoreboard players set @a carrot_click 0
scoreboard players set @a carrot_drop 0
scoreboard players remove @e[scores={cooldown=1..}] cooldown 1
scoreboard players remove @a[scores={selector=1..}] selector 1
scoreboard players set @a[scores={selector=-1}] selector 0
scoreboard players set @a[scores={sneaky=1..}] sneaky 0
scoreboard players set @a[scores={walk=1..}] walk 0
scoreboard players set @a[scores={sprint=1..}] sprint 0
scoreboard players operation @a[nbt={OnGround:1b},scores={jump=1..}] jump /= 2 C
execute as @a run scoreboard players operation @s pweapon_id = @s weapon_id
execute as @a unless score @s pslow = @s slow run function mgs:util/speed_update
execute as @e[type=!#mgs:mob_ex,scores={damage=1..}] at @s run function mgs:util/damage_mob
execute as @a[scores={damage=1..,health=1..}] run function mgs:util/damage

execute if score enablePlayerDam V matches 1.. as @a[gamemode=!creative,gamemode=!spectator,tag=!dead,tag=!no_damage] at @s run function mgs:core/last_pos
execute if score enableRecoil V matches 1.. run function mgs:util/kick/kick

scoreboard players remove @a[scores={kick=0..}] kick 1
execute as @a run scoreboard players operation @s phealth = @s health
execute as @a run scoreboard players operation @s pdeaths = @s deaths
execute as @a run scoreboard players operation @s pslow = @s slow