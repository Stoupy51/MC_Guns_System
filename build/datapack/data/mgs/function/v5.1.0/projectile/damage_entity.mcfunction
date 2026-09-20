
#> mgs:v5.1.0/projectile/damage_entity
#
# @executed	at @s
#
# @within	mgs:v5.1.0/projectile/damage_area
#

# Skip non-living entities and other projectiles
execute if entity @s[tag=mgs.slow_bullet] run return fail

# Friendly fire check: skip if target is a teammate (but not the shooter themselves)
execute if entity @s[type=player] unless entity @s[tag=mgs.temp_shooter] store result score #shooter_team mgs.data run scoreboard players get @n[tag=mgs.temp_shooter] mgs.mp.team
execute if entity @s[type=player] unless entity @s[tag=mgs.temp_shooter] if score #shooter_team mgs.data matches 1.. if score @s mgs.mp.team = #shooter_team mgs.data run return fail

# Get this entity's position (scaled by 1000)
execute store result score #ent_x mgs.data run data get entity @s Pos[0] 1000
execute store result score #ent_y mgs.data run data get entity @s Pos[1] 1000
execute store result score #ent_z mgs.data run data get entity @s Pos[2] 1000

# Calculate distance squared: dx*dx + dy*dy + dz*dz
scoreboard players operation #dx mgs.data = #ent_x mgs.data
scoreboard players operation #dx mgs.data -= #ctr_x mgs.data
scoreboard players operation #dy mgs.data = #ent_y mgs.data
scoreboard players operation #dy mgs.data -= #ctr_y mgs.data
scoreboard players operation #dz mgs.data = #ent_z mgs.data
scoreboard players operation #dz mgs.data -= #ctr_z mgs.data

# Square each component
scoreboard players operation #dx2 mgs.data = #dx mgs.data
scoreboard players operation #dx2 mgs.data *= #dx mgs.data
scoreboard players operation #dy2 mgs.data = #dy mgs.data
scoreboard players operation #dy2 mgs.data *= #dy mgs.data
scoreboard players operation #dz2 mgs.data = #dz mgs.data
scoreboard players operation #dz2 mgs.data *= #dz mgs.data

# Sum: dist_sq = dx2 + dy2 + dz2 (in millionths of blocks squared)
scoreboard players operation #dist_sq mgs.data = #dx2 mgs.data
scoreboard players operation #dist_sq mgs.data += #dy2 mgs.data
scoreboard players operation #dist_sq mgs.data += #dz2 mgs.data

# Get distance using sqrt (https://docs.mcbookshelf.dev/en/latest/modules/math.html#square-root)
execute store result storage bs:in math.sqrt.x double 0.000001 run scoreboard players get #dist_sq mgs.data
function #bs.math:sqrt
# Store distance in tenths of blocks (x10) for sub-block decimal precision in decay
execute store result score #distance mgs.data run data get storage bs:out math.sqrt 10

# Apply decay-based falloff: damage *= pow(decay, distance)
# decay into x
data modify storage bs:in math.pow.x set from storage mgs:temp expl.expl_decay

# distance into y (float tenths-of-blocks * 0.1 = actual block distance as float)
execute store result storage bs:in math.pow.y float 0.1 run scoreboard players get #distance mgs.data

# Compute pow(decay, distance)
function #bs.math:pow

# Get base damage and multiply by decay factor
execute store result score #expl_dmg mgs.data run data get storage mgs:temp expl.expl_damage 10
execute store result score #decay_factor mgs.data run data get storage bs:out math.pow 1000000

scoreboard players operation #expl_dmg mgs.data *= #decay_factor mgs.data
scoreboard players operation #expl_dmg mgs.data /= #1000000 mgs.data

# If zombie game is active: explosives hit zombies 5x harder, cap for players (6 hp = 3 hearts)
execute if data storage mgs:zombies game{state:"active"} if entity @s[type=!player] run scoreboard players operation #expl_dmg mgs.data *= #5 mgs.data
execute if data storage mgs:zombies game{state:"active"} if entity @s[type=player] if score #expl_dmg mgs.data matches 60.. run scoreboard players set #expl_dmg mgs.data 60

# Flak Jacket perk: halve explosive area damage to a perked MP player
execute if entity @s[type=player,scores={mgs.mp.in_game=1,mgs.special.flak_jacket=1}] run scoreboard players operation #expl_dmg mgs.data /= #2 mgs.data

# PhD Flopper perk: a perked (zombies) player takes no explosive area damage
execute if entity @s[type=player,scores={mgs.special.phd_flopper=1}] run scoreboard players set #expl_dmg mgs.data 0

# Skip if damage is negligible (less than 0.1)
execute if score #expl_dmg mgs.data matches ..0 run return fail

# Instant kill: if shooter has active instant kill and target is not immune, set damage to 99999
# Never applied to players while a zombies game is active (would bypass the explosion cap above)
tag @n[tag=mgs.temp_shooter] add mgs.ticking
execute if entity @s[tag=!mgs.no_instant_kill,type=!player] as @n[tag=mgs.temp_shooter] if score @s mgs.special.instant_kill matches 1.. run scoreboard players set #expl_dmg mgs.data 99999
execute unless data storage mgs:zombies game{state:"active"} if entity @s[tag=!mgs.no_instant_kill,type=player] as @n[tag=mgs.temp_shooter] if score @s mgs.special.instant_kill matches 1.. run scoreboard players set #expl_dmg mgs.data 99999

# Apply damage using the existing damage utility
# Apply damage, fire damage signal (weapon info included for handlers)
data modify storage mgs:input with set value {target:"@s", amount:0.0f, attacker:"@n[tag=mgs.temp_shooter]"}
execute if entity @n[tag=mgs.temp_shooter,type=player] run data modify storage mgs:input with.attacker set value "@p[tag=mgs.temp_shooter]"
execute store result storage mgs:input with.amount float 0.1 run scoreboard players get #expl_dmg mgs.data
data modify storage mgs:input with.weapon set from storage mgs:gun all

# If the victim IS the shooter, a self 'by' hit is cancelled by team friendlyFire=false,
# so the shooter would take no damage from their own blast. Apply plain (unattributed)
# damage to them instead; everyone else takes normal attributed damage.
execute if entity @s[tag=mgs.temp_shooter] run function mgs:v5.1.0/utils/signal_and_damage_plain
execute unless entity @s[tag=mgs.temp_shooter] run function mgs:v5.1.0/utils/signal_and_damage

# Signal: on_kill (check if entity died after explosion damage, guard against double-fire)
# Initialize to 0 (dead) — if entity no longer exists, score stays 0
scoreboard players set #victim_hp mgs.data 0
execute store result score #victim_hp mgs.data run data get entity @s Health 100
scoreboard players set #is_new_kill mgs.data 0
execute if score #victim_hp mgs.data matches ..0 unless entity @s[tag=mgs.already_killed] run scoreboard players set #is_new_kill mgs.data 1
execute if score #victim_hp mgs.data matches ..0 unless entity @s[tag=mgs.already_killed] run tag @s add mgs.already_killed

# Same drop hook as raycast/apply_damage: @s is the victim, killed here by an explosion
execute if score #is_new_kill mgs.data matches 1 if entity @s[tag=mgs.mission_enemy] at @s run function mgs:v5.1.0/missions/drop_enemy_weapon

execute if score #is_new_kill mgs.data matches 1 run data modify storage mgs:signals on_kill set value {}
execute if score #is_new_kill mgs.data matches 1 run data modify storage mgs:signals on_kill.explosion set value true
execute if score #is_new_kill mgs.data matches 1 as @n[tag=mgs.temp_shooter] run function #mgs:signals/on_kill

# Remove temporary tag
tag @n[tag=mgs.temp_shooter] remove mgs.ticking

