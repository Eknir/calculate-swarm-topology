import json
import math
import numpy as np
import requests
import matplotlib as plt
from collections import defaultdict

# get a list of all Swarm overlay addresses in binary form from a swarmscan network dump saved in the folder where this file also resides 
# (see: https://swarmscan-api.resenje.org/#tag/Network/paths/~1v1~1network~1dump/get)
def getBinaryOverlays(swarmscan):

    with open(swarmscan, 'r') as f:
        data = json.load(f)
    
    overlays = np.array([])

    for node in data['nodes']:
        overlaystr = node['overlay']
        overlaybin = bin(int(overlaystr, 16))
        overlays = np.append(overlays, overlaybin)

    return overlays

# returns maxDepth bin indentifiers a certain binary encoded overlay, where bin x identifier is getBins[x]    
def getBins(self, maxDepth):
    ret = []
    selfArray = list(self)
    
    for i in range(maxDepth):
        pos = i+2
        retItem = selfArray[0:pos+1]
        if retItem[pos] == '0':
            retItem[pos] = '1'
        else:
            retItem[pos] = '0'
        ret.append(''.join([str(elem) for elem in retItem]))       
    return ret

# given a self overlay and another overlay, define which bin the other overlay belongs to, respective to self
def defBin(self, node, maxDepth):
    for i in range(maxDepth):
        if node.startswith(self[0:maxDepth+3-i]):
            return maxDepth - i
    return 0

# get the topology (depth) of a node, given a certain connectivity, maxDepth and binSize (connections per bin)
def getIndividualDepth(connectivity, maxDepth, binSize):
    suspectedDepth = maxDepth

    # find the shallowest bin in which there are less than binSize nodes
    for i in range(maxDepth):
        if connectivity[maxDepth-i] < binSize:
            suspectedDepth = maxDepth - i   
    
    # check if higher bins have at least binSize nodes
    deepNodeCount = 0
    enoughDeepPeers = False
    for i in range(maxDepth - suspectedDepth):
        deepNodeCount = deepNodeCount + connectivity[suspectedDepth + i]
        if deepNodeCount >= binSize: 
            enoughDeepPeers = True
            break
    
    if enoughDeepPeers == False:
        suspectedDepth = suspectedDepth - 1
                   
    
    return suspectedDepth

# return the expected connectivity of the whole Swarm network, given an array of binary Swarm overlay addresses (get those with the function getOverlays)
def getSwarmConnectivity(overlays, maxDepth):
    
    topology = defaultdict(dict)
    
    for self in overlays:  
        # initialize
        for i in range(0, maxDepth+1):
            topology[self][i] = 0
    
        # get bin for each other node that is not self
        for node in overlays:
            if not node == self:
                binID = defBin(self, node, maxDepth)
                topology[self][binID] = topology[self][binID]+1   
            
    return topology

# 
def getSwarmDepths(connections, maxDepth, binSize):
    # initialize
    depths = defaultdict(dict)
    for i in range(0, maxDepth):
        depths[i] = 0
    for node in connections:
        depth =  getIndividualDepth(connections[node], maxDepth, binSize)
        depths[depth] =  depths[depth] + 1
    return depths
    
# call the functions:

file = 'swarmscan-nodes-2022-01-10-09-17-56.json'
maxDepth = 32
binSize = 4

overlays = getBinaryOverlays(file)
print("got overlays")

connections = getSwarmConnectivity(overlays, maxDepth)
print("got connections, saving result")

# save results to file
with open('connections.json', 'w') as fp:
    json.dump(connections, fp)

depths = getSwarmDepths(connections, maxDepth, binSize)
print("got depths, saving result")

# save results to file
with open('depths.json', 'w') as fp:
    json.dump(depths, fp)

