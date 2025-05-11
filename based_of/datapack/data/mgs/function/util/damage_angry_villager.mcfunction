data modify storage mgs:tmp data set value {Target:[],Type:"major_negative",Value:200}
data modify storage mgs:tmp data.Target set from entity @p[tag=angeryat] UUID
data modify entity @s Gossips append from storage mgs:tmp data