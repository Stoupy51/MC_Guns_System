data remove storage mgs:tmp Item
data modify storage mgs:tmp Item.tag set value {CustomModelData:30,Id:30,display:{Name:"{\"text\":\"FN-FAL\",\"italic\":false}"}}
scoreboard players operation v0 V = fal_damage S
scoreboard players operation v1 V = fal_cooldown S
scoreboard players operation v2 V = fal_acc_sneaky S
scoreboard players operation v3 V = fal_mag S
scoreboard players operation v4 V = fal_reload S
function mgs:guns/_common/gen/gun