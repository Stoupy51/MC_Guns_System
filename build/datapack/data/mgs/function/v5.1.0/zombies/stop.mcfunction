
#> mgs:v5.1.0/zombies/stop
#
# @executed	as the player & at current position
#
# @within	mgs:v5.1.0/zombies/game_over 100t [ scheduled ]
#			mgs:v5.1.0/zombies/restart
#			dialog mgs:v5.1.0/zombies/setup
#

function mgs:v5.1.0/shared/use_map_frame {mode:"zombies"}

data modify storage mgs:zombies game.state set value "lobby"
schedule clear mgs:v5.1.0/zombies/end_prep
scoreboard players set #zb_next_round mgs.data 0

# The attribute and NoAI restore of reset_player is part of the normal cleanup.
scoreboard players set #zb_freeze mgs.data 0
scoreboard players set #zb_resume_timer mgs.data 0
tag @e[tag=mgs.zb_frozen_ai] remove mgs.zb_frozen_ai
kill @e[tag=mgs.zombie_round]
kill @e[tag=mgs.zombies_entity]

execute if score #zb_has_bounds mgs.data matches 1 run function mgs:v5.1.0/shared/remove_forceload

scoreboard objectives setdisplay sidebar
scoreboard objectives remove mgs.zb_sidebar
gamerule advance_time true

scoreboard players set #any_game_active mgs.data 0
execute if data storage mgs:multiplayer game.state unless data storage mgs:multiplayer game{state:"lobby"} run scoreboard players set #any_game_active mgs.data 1
execute if data storage mgs:missions game.state unless data storage mgs:missions game{state:"lobby"} run scoreboard players set #any_game_active mgs.data 1
execute if data storage mgs:zombies game.state unless data storage mgs:zombies game{state:"lobby"} run scoreboard players set #any_game_active mgs.data 1
execute if score #any_game_active mgs.data matches 0 run gamerule natural_health_regeneration true

# Stop any hunger drain and refill the bar, so nobody is left winded.
effect clear @a[scores={mgs.zb.in_game=1}] minecraft:hunger
effect give @a[scores={mgs.zb.in_game=1}] minecraft:saturation 5 20 true
scoreboard players set @a[scores={mgs.zb.in_game=1}] mgs.stam_out 0
scoreboard players set @a[scores={mgs.zb.in_game=1}] mgs.stam_seen 0

# Every shader id off, so nothing survives into the lobby.
execute as @a[scores={mgs.zb.in_game=1}] run function mgs:v5.1.0/player/fx_reset

tellraw @a [[{"text":"","color":"gold"},"[",{"translate":"mgs"},"] "],{"translate":"mgs.zombies_game_ended","color":"red"}]
execute as @a[scores={mgs.zb.in_game=1}] run function mgs:v5.1.0/zombies/reset_player

kill @e[type=minecraft:marker,tag=mgs.death_watch]

# zombies_entity cleanup removes the portals, but the counter must be zeroed or the next game's round would never complete.
kill @e[type=minecraft:marker,tag=mgs.dog_portal]
scoreboard players set #zb_dog_pending mgs.data 0

scoreboard players set #zb_escort_count mgs.data 0

kill @e[tag=mgs.mb_display]
kill @e[tag=mgs.mb_presence]
kill @e[tag=mgs.mb_disabled]
kill @e[tag=mgs.mb_temp]
scoreboard players set #mb_pulls mgs.data 0
scoreboard players set #mb_dry_ray_gun mgs.data 0
scoreboard players set #mb_move_timer mgs.data 0
scoreboard players set #mb_fs_cleanup_pending mgs.data 0
scoreboard players set #mb_pid_counter mgs.data 0
tag @e remove mgs.mb_fs_active
tag @e remove mgs.mb_orig_active

tag @e[tag=mgs.barricade_removing] remove mgs.barricade_removing

kill @e[type=minecraft:item,tag=mgs.pu_item]
kill @e[type=minecraft:text_display,tag=mgs.pu_text]
scoreboard players set #pu_active mgs.data 0
scoreboard players set #zb_drops_this_round mgs.data 0
scoreboard players set #zb_cycle_done mgs.data 0
scoreboard players set #zb_cycle_len mgs.data 0
scoreboard players set @a mgs.special.instant_kill 0
scoreboard players set @a mgs.special.double_points 0
scoreboard players set @a mgs.special.infinite_ammo 0
data modify storage mgs:data _pu_queue set value []

# Also stops the song.
scoreboard players set #zb_fire_sale_timer mgs.data 0
scoreboard players set #mb_fs_cleanup_pending mgs.data 0
bossbar remove mgs:pu_fire_sale
stopsound @a ambient mgs:zombies/powerups/fire_sale_song
tag @e remove mgs.mb_fs_active
tag @e remove mgs.mb_orig_active
kill @e[tag=mgs.mb_temp]

scoreboard players set #zb_bonfire_sale_timer mgs.data 0
bossbar remove mgs:pu_bonfire_sale

bossbar remove mgs:pu_insta_kill
bossbar remove mgs:pu_double_points
bossbar remove mgs:pu_unlimited_ammo

# Every known score holder, offline players included.
scoreboard players reset * mgs.zb.perk.juggernog
scoreboard players reset * mgs.zb.perk.speed_cola
scoreboard players reset * mgs.zb.perk.double_tap
scoreboard players reset * mgs.zb.perk.quick_revive
scoreboard players reset * mgs.zb.perk.mule_kick
scoreboard players reset * mgs.zb.perk.stamin_up
scoreboard players reset * mgs.zb.perk.phd_flopper
scoreboard players reset * mgs.zb.perk.deadshot
scoreboard players reset * mgs.zb.perk.timeslip
scoreboard players reset * mgs.zb.perk.electric_cherry
scoreboard players reset * mgs.zb.perk.tombstone
scoreboard players reset * mgs.zb.perk.whos_who
scoreboard players reset * mgs.zb.perk.dying_wish
scoreboard players reset * mgs.zb.perk.widows_wine
scoreboard players reset * mgs.zb.perkpaid.juggernog
scoreboard players reset * mgs.zb.perkpaid.speed_cola
scoreboard players reset * mgs.zb.perkpaid.double_tap
scoreboard players reset * mgs.zb.perkpaid.quick_revive
scoreboard players reset * mgs.zb.perkpaid.mule_kick
scoreboard players reset * mgs.zb.perkpaid.stamin_up
scoreboard players reset * mgs.zb.perkpaid.phd_flopper
scoreboard players reset * mgs.zb.perkpaid.deadshot
scoreboard players reset * mgs.zb.perkpaid.timeslip
scoreboard players reset * mgs.zb.perkpaid.electric_cherry
scoreboard players reset * mgs.zb.perkpaid.tombstone
scoreboard players reset * mgs.zb.perkpaid.whos_who
scoreboard players reset * mgs.zb.perkpaid.dying_wish
scoreboard players reset * mgs.zb.perkpaid.widows_wine

kill @e[type=item_display,tag=mgs.wunderfizz_orb]
kill @e[tag=mgs.wf_display]
kill @e[tag=mgs.wf_bear]
scoreboard players set #wf_uses mgs.data 0
scoreboard players set #wf_move_timer mgs.data 0

data modify storage mgs:zombies ww_inv set value {}

scoreboard players set #downed_id_next mgs.data 0
kill @e[tag=mgs.downed_mannequin]
kill @e[tag=mgs.downed_hud]
kill @e[tag=mgs.downed_cam]
kill @e[tag=mgs.tombstone]
data modify storage mgs:zombies tombstone_inv set value {}

