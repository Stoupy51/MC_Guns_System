data remove storage mgs:tmp Item
data modify storage mgs:tmp Item.tag set value {CustomModelData:130,Id:130,display:{Name:"{\"text\":\"Desert Eagle Mark XIX\",\"italic\":false}"}}
scoreboard players operation v0 V = deagle_damage S
scoreboard players operation v1 V = deagle_cooldown S
scoreboard players operation v2 V = deagle_acc_sneaky S
scoreboard players operation v3 V = deagle_mag S
scoreboard players operation v4 V = deagle_reload S
function mgs:guns/_common/gen/gun