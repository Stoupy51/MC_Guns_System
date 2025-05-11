data remove storage mgs:tmp Item
data modify storage mgs:tmp Item.tag set value {CustomModelData:510,Id:510,display:{Name:"{\"text\":\"RPG-7\",\"italic\":false}"}}
scoreboard players operation v0 V = rpg7_damage S
scoreboard players set v1 V 0
scoreboard players operation v2 V = rpg7_acc_sneaky S
scoreboard players operation v3 V = rpg7_mag S
scoreboard players operation v4 V = rpg7_reload S
function mgs:guns/_common/gen/gun