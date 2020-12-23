# survival
Simulation of simple creatures on a day by day basis


The program is run from 'survival.py'
The window initially asks for a food value and number of days for the simulation to run.

Initially one critter is generated and a field with 'food'.   If the critter hits food then the food is eaten and the critters health increases.   Once health increases beyond a certain threshold the critter reproduces a-sexually with half the health each and a slight random variation in strength and velocity.
Food is automatically grown throughout.

If a critter has a strength greater than another, then it can eat the other critter and increase both health and strength in the process.
Some critters have an avoidance sensor so they change direction if they get close to a critter than can eat them.

The stronger a critter, the bigger it gets and the more food it uses.
If a critter gets to zero health due to lack of food it dies and disappears.

Stats are shown at the top of the screen
The stats are collated and graphs produced at the end of the simulation if all days are completed.

It is possible for all critters to die.
If food runs out completely, then the next day, some more food appears (dormant seeds).

I find the food tends to lead the critter build up until the critters have reproduced a lot at which point, food crashes followed by a critter die off.

I've yet to find a good balance but a food value of 5 has had the simulation run for over 200 days.

When critters are low strength then they can be difficult to see!
