
#> mgs:v5.0.0/lore/compute_values
#
# @within	mgs:v5.0.0/utils/update_all_lore
#

# Initialize input storage for macro functions
data modify storage mgs:input lore set value {}

# --- Damage ---
execute store result storage mgs:input lore.damage int 1 run scoreboard players get #lore_damage mgs.data

# --- Ammo ---
execute store result storage mgs:input lore.remaining int 1 run scoreboard players get #lore_remaining mgs.data
execute store result storage mgs:input lore.capacity int 1 run scoreboard players get #lore_capacity mgs.data

# --- Reload time: ticks → "X.Y" seconds (ticks / 2 gives tenths, then split) ---
scoreboard players operation #half mgs.data = #lore_reload mgs.data
scoreboard players operation #half mgs.data /= #2 mgs.data
scoreboard players operation #reload_int mgs.data = #half mgs.data
scoreboard players operation #reload_int mgs.data /= #10 mgs.data
scoreboard players operation #reload_dec mgs.data = #half mgs.data
scoreboard players operation #reload_dec mgs.data %= #10 mgs.data
execute store result storage mgs:input lore.reload_int int 1 run scoreboard players get #reload_int mgs.data
execute store result storage mgs:input lore.reload_dec int 1 run scoreboard players get #reload_dec mgs.data

# --- Fire rate: tenths_of_shots_per_second = 200 / cooldown → "X.Y" ---
scoreboard players operation #fire_rate_tenths mgs.data = #200 mgs.data
scoreboard players operation #fire_rate_tenths mgs.data /= #lore_cooldown mgs.data
scoreboard players operation #rate_int mgs.data = #fire_rate_tenths mgs.data
scoreboard players operation #rate_int mgs.data /= #10 mgs.data
scoreboard players operation #rate_dec mgs.data = #fire_rate_tenths mgs.data
scoreboard players operation #rate_dec mgs.data %= #10 mgs.data
execute store result storage mgs:input lore.rate_int int 1 run scoreboard players get #rate_int mgs.data
execute store result storage mgs:input lore.rate_dec int 1 run scoreboard players get #rate_dec mgs.data

# --- Pellets ---
execute store result storage mgs:input lore.pellets int 1 run scoreboard players get #lore_pellets mgs.data

# --- Decay: float*10000, round and divide by 100 for percentage ---
scoreboard players add #lore_decay mgs.data 50
scoreboard players operation #lore_decay mgs.data /= #100 mgs.data
execute store result storage mgs:input lore.decay_pct int 1 run scoreboard players get #lore_decay mgs.data

# --- Switch time: ticks → "X.Y" seconds ---
scoreboard players operation #switch_half mgs.data = #lore_switch mgs.data
scoreboard players operation #switch_half mgs.data /= #2 mgs.data
scoreboard players operation #switch_int mgs.data = #switch_half mgs.data
scoreboard players operation #switch_int mgs.data /= #10 mgs.data
scoreboard players operation #switch_dec mgs.data = #switch_half mgs.data
scoreboard players operation #switch_dec mgs.data %= #10 mgs.data
execute store result storage mgs:input lore.switch_int int 1 run scoreboard players get #switch_int mgs.data
execute store result storage mgs:input lore.switch_dec int 1 run scoreboard players get #switch_dec mgs.data

# --- Grenade stats ---
execute store result storage mgs:input lore.expl_damage int 1 run scoreboard players get #lore_expl_damage mgs.data
execute store result storage mgs:input lore.expl_radius int 1 run scoreboard players get #lore_expl_radius mgs.data

# --- Grenade fuse time: ticks → "X.Y" seconds ---
scoreboard players operation #fuse_half mgs.data = #lore_grenade_fuse mgs.data
scoreboard players operation #fuse_half mgs.data /= #2 mgs.data
scoreboard players operation #fuse_int mgs.data = #fuse_half mgs.data
scoreboard players operation #fuse_int mgs.data /= #10 mgs.data
scoreboard players operation #fuse_dec mgs.data = #fuse_half mgs.data
scoreboard players operation #fuse_dec mgs.data %= #10 mgs.data
execute store result storage mgs:input lore.fuse_int int 1 run scoreboard players get #fuse_int mgs.data
execute store result storage mgs:input lore.fuse_dec int 1 run scoreboard players get #fuse_dec mgs.data

# --- Grenade type display name ---
data modify storage mgs:input lore.type_display set value "Unknown"
execute if data storage mgs:temp {grenade_type:"frag"} run data modify storage mgs:input lore.type_display set value "Frag"
execute if data storage mgs:temp {grenade_type:"semtex"} run data modify storage mgs:input lore.type_display set value "Semtex"
execute if data storage mgs:temp {grenade_type:"smoke"} run data modify storage mgs:input lore.type_display set value "Smoke"
execute if data storage mgs:temp {grenade_type:"flash"} run data modify storage mgs:input lore.type_display set value "Flash"

