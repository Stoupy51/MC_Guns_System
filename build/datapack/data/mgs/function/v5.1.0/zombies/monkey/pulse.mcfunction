
#> mgs:v5.1.0/zombies/monkey/pulse
#
# @executed	at @s
#
# @within	mgs:v5.1.0/zombies/monkey/tick
#

# Mark the paired taunt as the current damage source for this pulse
execute as @e[tag=mgs.monkey_taunt,distance=..8] if score @s mgs.monkey_id = #monkey_cur_id mgs.data run tag @s add mgs.monkey_cur
execute unless entity @e[tag=mgs.monkey_cur,distance=..8] run return 0

# Steal aggro: a 0.01 hit BY the taunt makes each enemy retaliate against it (HurtByTarget beats
# player targeting; also writes wolves' angry_at). 40 blocks matches the enemies' follow_range —
# targets further than that get dropped by vanilla target validation anyway. Rising zombies are
# skipped (NoAI underground); the next pulse catches them once they're up. Re-pulsing every second
# also re-captures enemies that were shot in between (being hurt by a player re-targets them).
execute as @e[tag=mgs.zombie_round,tag=!mgs.zb_rising,distance=..40] run damage @s 0.01 minecraft:mob_attack by @n[tag=mgs.monkey_cur]
tag @e[tag=mgs.monkey_cur] remove mgs.monkey_cur

# Toy jingle placeholder: cycle chime pitches each pulse (real monkey-music .ogg is a HUMAN asset)
scoreboard players operation #monkey_note mgs.data = @s mgs.data
scoreboard players operation #monkey_note mgs.data /= #20 mgs.data
scoreboard players operation #monkey_note mgs.data %= #4 mgs.data
execute if score #monkey_note mgs.data matches 0 run playsound minecraft:block.note_block.chime ambient @a[distance=..32] ~ ~ ~ 1.0 0.7
execute if score #monkey_note mgs.data matches 1 run playsound minecraft:block.note_block.chime ambient @a[distance=..32] ~ ~ ~ 1.0 0.9
execute if score #monkey_note mgs.data matches 2 run playsound minecraft:block.note_block.chime ambient @a[distance=..32] ~ ~ ~ 1.0 1.1
execute if score #monkey_note mgs.data matches 3 run playsound minecraft:block.note_block.chime ambient @a[distance=..32] ~ ~ ~ 1.0 1.4
particle minecraft:note ~ ~0.5 ~ 0.3 0.3 0.3 1 3 force @a[distance=..32]

