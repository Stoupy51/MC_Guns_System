""" Late joining, and points awarded for kills and bullet hits. """
# Imports
from stewbeet import Mem, write_versioned_function

from ....helpers.lifecycle import GameLifecycle


# Functions
def write_zombies_join() -> None:
	ns: str = Mem.ctx.project_id
	version: str = Mem.ctx.project_version

	## Join Ongoing Zombies Game (late-joiner support)
	write_versioned_function("zombies/join_game", GameLifecycle.late_join_flow_lines(
		ns,
		"zombies",
		f"{ns}.zb.in_game",
		"No active zombies game to join!",
		"You are already in the zombies game!",
		f"""
scoreboard players set @s {ns}.zb.in_game 1
team join {ns}.zombies @s
# Keep the XP spend tracker in step: an unsynced reset reads as points being SPENT (see zombies/xp.py)
scoreboard players set @s {ns}.zb.points 500
scoreboard players set @s {ns}.zb.xp_pts_prev 500
scoreboard players set @s {ns}.zb.xp_spent_acc 0
scoreboard players set @s {ns}.zb.kills 0
scoreboard players set @s {ns}.zb.downs 0
scoreboard players set @s {ns}.zb.passive 0
scoreboard players set @s {ns}.zb.ability 0
scoreboard players set @s {ns}.zb.ability_cd 0
scoreboard players set @s {ns}.zb.horde_cd 0
scoreboard players set @s {ns}.mp.spectate_timer 0
scoreboard players set @s {ns}.mp.death_count 0
attribute @s minecraft:max_health base reset
attribute @s minecraft:entity_interaction_range base set 5
""",
		f"{ns}:v{version}/zombies/respawn_tp",
		"joined the zombies game!",
		"dark_green",
		xp_side="zb",
		post_class_lines=f"scoreboard players operation @s {ns}.zb.prev_kills = @s {ns}.total_kills",
		class_menu_lines=(
			"# Zombies has no class selection: give the fixed starting loadout (knife + pistol), matching "
			"the start function\n"
			f"function {ns}:v{version}/zombies/inventory/give_starting_loadout"
		),
	))

	# Kill points, tracked via the totalKillCount stat delta so every kill type counts.
	write_versioned_function("zombies/check_kill_points", f"""
# Calculate delta kills since last check
scoreboard players operation #zb_kills_delta {ns}.data = @s {ns}.total_kills
scoreboard players operation #zb_kills_delta {ns}.data -= @s {ns}.zb.prev_kills
scoreboard players operation @s {ns}.zb.prev_kills = @s {ns}.total_kills

# Skip if no new kills
execute if score #zb_kills_delta {ns}.data matches ..0 run return 0

# Determine kill type: gun (bullet kill = 50) or melee (knife kill = 130)
scoreboard players set #zb_kill_points {ns}.data 0
execute if items entity @s weapon.mainhand *[custom_data~{{{ns}:{{gun:true}}}}] run scoreboard players operation #zb_kill_points {ns}.data = #zb_points_kill {ns}.config
execute unless items entity @s weapon.mainhand *[custom_data~{{{ns}:{{gun:true}}}}] run scoreboard players operation #zb_kill_points {ns}.data = #zb_points_knife_kill {ns}.config

# Award base points (delta * points_per_kill_type)
scoreboard players operation #total_kill_points {ns}.data = #zb_kills_delta {ns}.data
scoreboard players operation #total_kill_points {ns}.data *= #zb_kill_points {ns}.data
scoreboard players operation @s {ns}.zb.points += #total_kill_points {ns}.data

# Apply x1.2 points passive: add 20% extra
execute if score @s {ns}.zb.passive matches 1 run scoreboard players operation #additional {ns}.data = #total_kill_points {ns}.data
execute if score @s {ns}.zb.passive matches 1 run scoreboard players operation #additional {ns}.data /= #5 {ns}.data
execute if score @s {ns}.zb.passive matches 1 run scoreboard players operation @s {ns}.zb.points += #additional {ns}.data

# Accumulate kill count
scoreboard players operation @s {ns}.zb.kills += #zb_kills_delta {ns}.data
""")

	# Bullet hit points (+10 per bullet hit on a live zombie)
	write_versioned_function("zombies/on_hit_signal", f"""
# Only process if zombies game is active & If the hit target is a live round zombie
execute unless data storage {ns}:zombies game{{state:"active"}} run return fail
execute unless entity @s[tag={ns}.zombie_round] run return fail

# Mark this zombie as hit by a player this tick (gates power-up drops to player kills)
scoreboard players operation @s {ns}.zb.player_hit = #total_tick {ns}.data

# Award +10 bullet hit points to the shooter
scoreboard players operation @n[tag={ns}.ticking] {ns}.zb.points += #zb_points_hit {ns}.config
""", tags=[f"{ns}:signals/damage"])

	# Hook kill check into game_tick (per in-game player, non-spectator)
	write_versioned_function("zombies/game_tick", f"""
# Award kill points from totalKillCount delta
execute as @a[scores={{{ns}.zb.in_game=1}},gamemode=!spectator] run function {ns}:v{version}/zombies/check_kill_points
""")

