from accelerants import aStarSearch
import numpy as np
from queue import SimpleQueue, Empty

MAX_PATH_LENGTH = 100

class PathFinder:
    def __init__(self, map_size):
        self.map_size = map_size

        self.path = SimpleQueue()

        self.tempx = np.empty(MAX_PATH_LENGTH, dtype=np.int32)
        self.tempy = np.empty(MAX_PATH_LENGTH, dtype=np.int32)

    def setOpaques(self, array):
        self.opaques = array

    def genOpaquesFromElevCutoff(self, elevs, cutoff):
        self.setOpaques(elevs > cutoff)

    def extendPath(self, path):
        for node in path:
            self.addPathNode(node)

    def addPathNode(self, node):
        self.path.put(node)

    def clearPath(self):
        self.path = SimpleQueue()

    def getNode(self):
        try:
            return self.path.get(False)
        except Empty:
            return None

    def extendPathFromXY(self, pathx, pathy, length):
        # Back to front add nodes
        for i in range(length):
            index = length - i - 1

            node = (pathx[index], pathy[index])

            self.addPathNode(node)

    def calcPath(self, start, end):
        length = aStarSearch(self.opaques,
                             start[0], start[1],
                             end[0], end[1],
                             self.map_size[0], self.map_size[1],
                             self.tempx, self.tempy)

        self.clearPath()
        self.extendPathFromXY(self.tempx, self.tempy, length)
