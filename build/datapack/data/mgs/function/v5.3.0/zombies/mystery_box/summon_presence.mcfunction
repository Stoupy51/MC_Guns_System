
#> mgs:v5.3.0/zombies/mystery_box/summon_presence
#
# @executed	as @n[tag=mgs.mystery_box_active] & at @s & positioned ~ ~-0.9 ~
#
# @within	mgs:v5.3.0/zombies/mystery_box/sync_presence_display {extra_tags:""} [ as @n[tag=mgs.mystery_box_active] & at @s & positioned ~ ~-0.9 ~ ]
#			mgs:v5.3.0/zombies/mystery_box/fire_sale_start {extra_tags:',"mgs.mb_temp"'} [ as @e[tag=...] & at @s & positioned ~ ~-0.9 ~ ]
#			mgs:v5.3.0/zombies/mystery_box/summon_descending {extra_tags:""}
#
# @args		extra_tags (string)
#

$function mgs:v5.3.0/zombies/mystery_box/summon_part {tags:["mgs.mb_presence","mgs.mb_base","mgs.zombies_entity","mgs.mb_part_new"$(extra_tags)],name:"Mystery Box",model:"mgs:mystery_box_base"}
$function mgs:v5.3.0/zombies/mystery_box/summon_part {tags:["mgs.mb_presence","mgs.mb_lid","mgs.zombies_entity","mgs.mb_part_new"$(extra_tags)],name:"Mystery Box Lid",model:"mgs:mystery_box_lid"}

