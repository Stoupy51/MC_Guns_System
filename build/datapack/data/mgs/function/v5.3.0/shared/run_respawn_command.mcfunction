
#> mgs:v5.3.0/shared/run_respawn_command
#
# @within	mgs:v5.3.0/dialog/close_then
#			mgs:v5.3.0/shared/run_respawn_commands_iter with storage mgs:temp _respawn_cmd
#
# @args		command (unknown)
#

$execute at @s run $(command)

