data remove storage mgs:tmp Item
data modify storage mgs:tmp Item.tag set value {CustomModelData:20,Id:20,display:{Name:"{\"text\":\"AK47\",\"italic\":false}"}}
scoreboard players operation v0 V = ak47_damage S
scoreboard players operation v1 V = ak47_cooldown S
scoreboard players operation v2 V = ak47_acc_sneaky S
scoreboard players operation v3 V = ak47_mag S
scoreboard players operation v4 V = ak47_reload S
function mgs:guns/_common/gen/gun