
#> mgs:v5.0.0/raycast/accuracy/apply_spread
#
# @executed	anchored eyes & positioned ^ ^ ^
#
# @within	mgs:v5.0.0/raycast/main
#

# Get random uniform rotation spread (https://docs.mcbookshelf.dev/en/latest/modules/random.html#random-distributions)
data modify storage mgs:input with set value {}
execute store result storage mgs:input with.min int -1 run data get storage mgs:gun accuracy
execute store result storage mgs:input with.max int 1 run data get storage mgs:gun accuracy
function #bs.random:uniform with storage mgs:input with

# Add horizontal rotation (divided by 100) (https://docs.mcbookshelf.dev/en/latest/modules/position.html#add-position-and-rotation)
scoreboard players operation @s bs.rot.h = $random.uniform bs.out
function #bs.position:add_rot_h {scale: 0.01}

# Get a new random rotation spread
function #bs.random:uniform with storage mgs:input with

# Add vertical rotation (divided by 100)
scoreboard players operation @s bs.rot.v = $random.uniform bs.out
function #bs.position:add_rot_v {scale: 0.01}

