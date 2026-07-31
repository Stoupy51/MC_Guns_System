
#> mgs:v5.1.0/progression/mp/settle
#
# @within	mgs:v5.1.0/progression/mp/award_kill
#			mgs:v5.1.0/progression/mp/award_headshot
#			mgs:v5.1.0/progression/mp/award_dom_capture
#			mgs:v5.1.0/progression/mp/award_dom_neutralize
#			mgs:v5.1.0/progression/mp/award_dom_hold
#			mgs:v5.1.0/progression/mp/award_hp_capture
#			mgs:v5.1.0/progression/mp/award_hp_hold
#			mgs:v5.1.0/progression/mp/award_bomb_pickup
#			mgs:v5.1.0/progression/mp/award_bomb_plant
#			mgs:v5.1.0/progression/mp/award_bomb_defuse
#			mgs:v5.1.0/progression/mp/award_site_destroyed
#			mgs:v5.1.0/progression/mp/award_round_win
#			mgs:v5.1.0/progression/mp/award_round_loss
#			mgs:v5.1.0/progression/mp/award_match_win
#			mgs:v5.1.0/progression/mp/award_match_loss
#

# XP only ever goes up, and the cap is far past anything reachable — it exists so the bar and bisect
# multiplications cannot overflow.
execute if score @s mgs.mp.xp_total matches 1000000000.. run scoreboard players set @s mgs.mp.xp_total 1000000000
execute unless score @s mgs.mp.xp_level matches 1.. run scoreboard players set @s mgs.mp.xp_level 1

# Drain the progress into levels, then announce ONCE however many levels that turned out to be: a single
# large award can cross twenty boundaries at low level, and twenty chat lines is not a reward.
scoreboard players operation #xp_lvl_before mgs.data = @s mgs.mp.xp_level
function mgs:v5.1.0/progression/mp/level_check
execute if score @s mgs.mp.xp_level > #xp_lvl_before mgs.data run function mgs:v5.1.0/progression/mp/level_up_feedback

function mgs:v5.1.0/progression/mp/refresh_bar

