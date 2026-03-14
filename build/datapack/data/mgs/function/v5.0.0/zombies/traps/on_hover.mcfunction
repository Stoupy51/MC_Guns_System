
#> mgs:v5.0.0/zombies/traps/on_hover
#
# @within	???
#

data modify storage smithed.actionbar:input message set value {json:[[{"text":"⚠ ","color":"red"}, {"translate":"mgs.trap"}],[{"text":" - ","color":"gray"}, {"translate":"mgs.right_click_to_activate"}]],priority:'notification',freeze:5}
function #smithed.actionbar:message

