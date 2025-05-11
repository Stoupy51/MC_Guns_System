data remove storage mgs:tmp Item
data modify storage mgs:tmp Item.tag set value {CustomModelData:80,Id:80,display:{Name:"{\"text\":\"FN MK 17\",\"italic\":false}"}}
scoreboard players operation v0 V = scar17_damage S
scoreboard players operation v1 V = scar17_cooldown S
scoreboard players operation v2 V = scar17_acc_sneaky S
scoreboard players operation v3 V = scar17_mag S
scoreboard players operation v4 V = scar17_reload S
function mgs:guns/_common/gen/gun