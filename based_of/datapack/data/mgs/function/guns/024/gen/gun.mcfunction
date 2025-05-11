data remove storage mgs:tmp Item
data modify storage mgs:tmp Item.tag set value {CustomModelData:240,Id:240,display:{Name:"{\"text\":\"PPSh-41\",\"italic\":false}"}}
scoreboard players operation v0 V = ppsh41_damage S
scoreboard players operation v1 V = ppsh41_cooldown S
scoreboard players operation v2 V = ppsh41_acc_sneaky S
scoreboard players operation v3 V = ppsh41_mag S
scoreboard players operation v4 V = ppsh41_reload S
function mgs:guns/_common/gen/gun