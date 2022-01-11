# Calculate topology
This script calculates the best-case topology, given a swarmscan file

First, it parses the Swarmcan file and converts all overlay addresses to binary format (for ease of working)
Then, we take all these addresses and define for each address, in which bin all other addresses are placed (saved in connections.json)
Then, we calculate the depth for each node, assuming that it makes all required connections (saved in depths.json)

# Prerequisites
- python3
- install all modules with pip install <module_name>
- a swarmscan file, saved in this directory (see: https://swarmscan-api.resenje.org/#tag/Network/paths/~1v1~1network~1dump/get)

# Run
- adjust the filename of your swarmscan file in the main script
- python3 calculate_topology.py