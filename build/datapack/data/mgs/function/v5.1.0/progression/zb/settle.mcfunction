
#> mgs:v5.1.0/progression/zb/settle
#
# @executed	as @a[scores={mgs.zb.in_game=1},gamemode=!spectator]
#
# @within	mgs:v5.1.0/progression/zb/award_kill
#			mgs:v5.1.0/progression/zb/award_headshot
#			mgs:v5.1.0/progression/zb/award_points_spent
#			mgs:v5.1.0/progression/zb/award_round_survived
#			mgs:v5.1.0/progression/zb/award_revive
#			mgs:v5.1.0/progression/zb/award_perk
#			mgs:v5.1.0/progression/zb/award_pack_a_punch
#			mgs:v5.1.0/progression/zb/award_power
#			mgs:v5.1.0/progression/zb/award_door
#			mgs:v5.1.0/progression/zb/award_powerup
#			mgs:v5.1.0/progression/zb/award_mystery_box
#			mgs:v5.1.0/progression/zb/award_trap
#			mgs:v5.1.0/progression/zb/award_barricade
#			mgs:v5.1.0/progression/zb/award_game_over
#

# XP only ever goes up, and the cap is far past anything reachable — it exists so the bar and bisect
# multiplications cannot overflow.
execute if score @s mgs.zb.xp_total matches 1000000000.. run scoreboard players set @s mgs.zb.xp_total 1000000000
execute unless score @s mgs.zb.xp_level matches 1.. run scoreboard players set @s mgs.zb.xp_level 1

# Drain the progress into levels, then announce ONCE however many levels that turned out to be: a single
# large award can cross twenty boundaries at low level, and twenty chat lines is not a reward.
scoreboard players operation #xp_lvl_before mgs.data = @s mgs.zb.xp_level
function mgs:v5.1.0/progression/zb/level_check
execute if score @s mgs.zb.xp_level > #xp_lvl_before mgs.data run function mgs:v5.1.0/progression/zb/level_up_feedback

function mgs:v5.1.0/progression/zb/refresh_bar

