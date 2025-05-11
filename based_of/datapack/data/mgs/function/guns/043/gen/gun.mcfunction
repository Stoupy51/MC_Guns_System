data remove storage mgs:tmp Item
data modify storage mgs:tmp Item.tag set value {CustomModelData:430,Id:430,display:{Name:"{\"text\":\"M91/30\",\"italic\":false}"}}
scoreboard players operation v0 V = mosin_damage S
scoreboard players operation v1 V = mosin_cooldown S
scoreboard players operation v2 V = mosin_acc_sneaky S
scoreboard players operation v3 V = mosin_mag S
scoreboard players operation v4 V = mosin_mag S
scoreboard players operation v4 V *= mosin_reload S
function mgs:guns/_common/gen/gun