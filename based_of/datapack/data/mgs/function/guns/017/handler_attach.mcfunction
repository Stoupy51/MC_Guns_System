# v0 scope type -> 0:none 1:holo 2:kobra 3:acog 4:mk4 5:pso1 6:pu
# v1 compatibility (output)
execute if score v0 V matches 0 run scoreboard players set v1 V 1
execute if score v0 V matches 1.. run scoreboard players set v1 V 0