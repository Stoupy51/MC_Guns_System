
#> mgs:v5.3.0/zombies/mystery_box/summon_disabled_display
#
# @executed	as @e[tag=...] & at @s
#
# @within	mgs:v5.3.0/zombies/mystery_box/refresh_disabled [ as @e[tag=...] & at @s ]
#

execute if entity @n[tag=mgs.mb_display,distance=..3] run return 0
execute unless entity @s[tag=mgs.roam_hidden] positioned ~ ~-0.9 ~ run function mgs:v5.3.0/zombies/mystery_box/summon_part {tags:["mgs.mb_disabled","mgs.zombies_entity","mgs.mb_part_new"],name:"Mystery Box (inactive)",model:"mgs:mystery_box_disabled"}
execute if entity @s[tag=mgs.roam_hidden] positioned ~ ~511.1 ~ run function mgs:v5.3.0/zombies/mystery_box/summon_part {tags:["mgs.mb_disabled","mgs.zombies_entity","mgs.mb_part_new"],name:"Mystery Box (inactive)",model:"mgs:mystery_box_disabled"}

