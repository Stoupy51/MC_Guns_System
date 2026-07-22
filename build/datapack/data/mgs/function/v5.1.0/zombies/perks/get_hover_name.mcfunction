
#> mgs:v5.1.0/zombies/perks/get_hover_name
#
# @executed	as @n[tag=mgs.pk_new]
#
# @within	mgs:v5.1.0/zombies/perks/announce_progress
#			mgs:v5.1.0/zombies/perks/on_hover
#

data modify storage mgs:temp _pk_hover_name set value "Perk"
execute if data storage mgs:temp _pk_data.name run data modify storage mgs:temp _pk_hover_name set from storage mgs:temp _pk_data.name
execute unless data storage mgs:temp _pk_data.name if data storage mgs:temp _pk_data{perk_id:"juggernog"} run data modify storage mgs:temp _pk_hover_name set value "Juggernog"
execute unless data storage mgs:temp _pk_data.name if data storage mgs:temp _pk_data{perk_id:"speed_cola"} run data modify storage mgs:temp _pk_hover_name set value "Speed Cola"
execute unless data storage mgs:temp _pk_data.name if data storage mgs:temp _pk_data{perk_id:"double_tap"} run data modify storage mgs:temp _pk_hover_name set value "Double Tap"
execute unless data storage mgs:temp _pk_data.name if data storage mgs:temp _pk_data{perk_id:"quick_revive"} run data modify storage mgs:temp _pk_hover_name set value "Quick Revive"
execute unless data storage mgs:temp _pk_data.name if data storage mgs:temp _pk_data{perk_id:"mule_kick"} run data modify storage mgs:temp _pk_hover_name set value "Mule Kick"
execute unless data storage mgs:temp _pk_data.name if data storage mgs:temp _pk_data{perk_id:"stamin_up"} run data modify storage mgs:temp _pk_hover_name set value "Stamin-Up"

