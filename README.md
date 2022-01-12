# Calculate topology
This script calculates the best-case topology, given a swarmscan file

First, it parses the Swarmcan file and converts all overlay addresses to binary format (for ease of working)

Then, we take all these addresses and define for each address, in which bin all other addresses are placed (saved in connections.json)

Then, we calculate the depth for each node, assuming that it makes all required connections (saved in depths.json)

All results (from a demo swarmscan file) are provided

The script also calculate assumed real connections and depths based on the "peers" field

# Prerequisites
- python3
- install all modules with pip install <module_name>
- a swarmscan file, saved in this directory (get it by https://swarmscan-api.resenje.org/v1/network/dump => https://swarmscan-api.resenje.org/#tag/Network/paths/~1v1~1network~1dump/get)
    - this is already provided for your convenience. Be sure to update this if needed!

# Run
- python3 calculate_topology.py