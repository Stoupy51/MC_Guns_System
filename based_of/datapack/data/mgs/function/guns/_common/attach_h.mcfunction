# v0 scope type -> 0:none 1:holo 2:kobra 3:acog 4:mk4 5:pso1 6:pu
# v1 success out -1:no-wep 0:failed 1:success
# v2 weapon id in -- out
scoreboard players set v1 V -1
execute if score v2 V matches 10..109 run function mgs:guns/_common/handler_attach_rifle
execute if score v2 V matches 110..209 run function mgs:guns/_common/handler_attach_pistol
execute if score v2 V matches 210..309 run function mgs:guns/_common/handler_attach_smg
execute if score v2 V matches 310..409 run function mgs:guns/_common/handler_attach_shotgun
execute if score v2 V matches 410..509 run function mgs:guns/_common/handler_attach_sniper
execute if score v2 V matches 510..609 run function mgs:guns/_common/handler_attach_special
execute if score v1 V matches 1 run scoreboard players operation v2 V /= 5 C
execute if score v1 V matches 1 run scoreboard players operation v2 V *= 5 C
execute if score v1 V matches 1 if score v0 V matches 1 run scoreboard players operation v2 V += holo S
execute if score v1 V matches 1 if score v0 V matches 2 run scoreboard players operation v2 V += kobra S
execute if score v1 V matches 1 if score v0 V matches 3 run scoreboard players operation v2 V += acog S
execute if score v1 V matches 1 if score v0 V matches 4 run scoreboard players operation v2 V += mk4 S
execute if score v1 V matches 1 if score v0 V matches 5 run scoreboard players operation v2 V += pso1 S
execute if score v1 V matches 1 if score v0 V matches 6 run scoreboard players operation v2 V += pu S