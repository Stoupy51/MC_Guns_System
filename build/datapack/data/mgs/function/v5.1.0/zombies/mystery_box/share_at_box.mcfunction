
#> mgs:v5.1.0/zombies/mystery_box/share_at_box
#
# @executed	at @n[tag=bs.interaction.target]
#
# @within	mgs:v5.1.0/zombies/mystery_box/on_left_click [ at @n[tag=bs.interaction.target] ]
#

# Nothing to share unless a finished pull is sitting here (a spinning one has no weapon yet)
execute unless entity @n[tag=mgs.mb_display,distance=..3] run return fail
execute if entity @n[tag=mgs.mb_display,distance=..3,scores={mgs.mb.anim=1..}] run return fail

# Sharing twice is a no-op rather than a second announcement
execute if entity @n[tag=mgs.mb_display,distance=..3,tag=mgs.mb_shared] run return fail

# Only the buyer can give their own pull away
execute unless score @s mgs.mb.pid = @n[tag=mgs.mb_display,distance=..3] mgs.mb.buyer run return run function mgs:v5.1.0/zombies/mystery_box/deny_not_your_result

tag @n[tag=mgs.mb_display,distance=..3] add mgs.mb_shared
function mgs:v5.1.0/zombies/feedback/sound_success
tellraw @a[scores={mgs.zb.in_game=1}] [[{"text":"","color":"gold"},"[",{"translate":"mgs"},"] "],{"selector":"@s"},{"translate":"mgs.shared_their_mystery_box_weapon_anyone_can_take_it","color":"green"}]

