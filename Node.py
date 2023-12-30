from common import *

class Node:
    def __init__(self, ID, networksimulator, costs):
        self.myID = ID
        self.ns = networksimulator
        num = self.ns.NUM_NODES        
        self.distanceTable = [[0 for i in range(num)] for j in range(num)]
        self.routes = [0 for i in range(num)]
        self.neighbour = [False for i in range(num)]
        
        for i in range(num):
            if ID == i:
                self.distanceTable[ID] = costs

                if costs[i] != self.ns.INFINITY:
                    self.routes[i] = i
                                    
            else:
                
                for j in range(num):
                    if i != j:
                        self.distanceTable[i][j] = self.ns.INFINITY
                    
                if costs[i] != self.ns.INFINITY:
                    self.neighbour[i] = True
                    self.ns.tolayer2(RTPacket(ID, i, costs))
                    self.routes[i] = i
                    
    def recvUpdate(self, pkt):

        self.distanceTable[pkt.sourceid] = pkt.mincosts
        changed = False
        
        for i in range(self.ns.NUM_NODES):
            
            for j in range(self.ns.NUM_NODES):
                if self.distanceTable[pkt.destid][i] + self.distanceTable[i][j] < self.distanceTable[pkt.destid][j]:
                    self.distanceTable[pkt.destid][j] = self.distanceTable[pkt.destid][i] + self.distanceTable[i][j]
                    self.routes[j] = self.routes[self.ns.nodes[self.routes[i]].routes[i]]
                    changed = True
                    
            if changed:                
                for k in range(self.ns.NUM_NODES):  
                    if self.neighbour[k]:                        
                        self.ns.tolayer2(RTPacket(pkt.destid, k, self.distanceTable[pkt.destid]))
                changed = False
              
        return 

    
    def printdt(self):
        print("   D"+str(self.myID)+" |  ", end="")
        for i in range(self.ns.NUM_NODES):
            print("{:3d}   ".format(i), end="")
        print()
        print("  ----|-", end="")
        for i in range(self.ns.NUM_NODES):            
            print("------", end="")
        print()    
        for i in range(self.ns.NUM_NODES):
            print("     {}|  ".format(i), end="" )
            
            for j in range(self.ns.NUM_NODES):
                print("{:3d}   ".format(self.distanceTable[i][j]), end="" )
            print()            
        print()
    
