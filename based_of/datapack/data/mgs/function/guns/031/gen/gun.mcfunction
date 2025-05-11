data remove storage mgs:tmp Item
data modify storage mgs:tmp Item.tag set value {CustomModelData:310,Id:310,display:{Name:"{\"text\":\"SPAS-12\",\"italic\":false}"}}
scoreboard players set v0 V 3
scoreboard players operation v0 V *= spas12_damage S
scoreboard players operation v1 V = spas12_cooldown_s S
scoreboard players operation v2 V = spas12_acc_sneaky S
scoreboard players operation v3 V = spas12_mag S
scoreboard players operation v4 V = spas12_mag S
scoreboard players operation v4 V *= spas12_reload S
function mgs:guns/_common/gen/gun