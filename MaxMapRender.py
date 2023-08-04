import pymxs
import os
import random
import string

rt = pymxs.runtime

# Set rendered map size and location (by default, it's 2048x2048 and it's located in the 'textures/baked' directory)
renderMapSize = rt.Point2(2048,2048)
bakedMapsPath = os.path.join(rt.maxFilePath, "textures", "baked")

# Check if already baked
if not os.path.exists(bakedMapsPath):
    os.makedirs(bakedMapsPath)
    
def checkForComplexMaps(map):
    if not (rt.classOf(map) == rt.Bitmaptexture):
        newName = 'Map_'+str(id_generator(7)) + '.png'
        if not os.path.exists(os.path.join(bakedMapsPath, newName)):
            bakedMap = rt.renderMap(map, size=renderMapSize, filter=False, fileName=os.path.join(bakedMapsPath, newName))
            rt.save(bakedMap)
            newMap = rt.Bitmaptexture()
            newMap.name = map.name
            newMap.fileName = bakedMap.fileName
            return newMap
        else:
            newMap = rt.Bitmaptexture()
            newMap.name = map.name
            newMap.fileName = os.path.join(bakedMapsPath, newName)
            return newMap
    else:
        return map

# Random ID generator to workaround maps which have the same name in Max
def id_generator(size=6, chars=string.ascii_uppercase + string.digits):
    return ''.join(random.choice(chars) for _ in range(size))


# Traverse all scene materials
for mat in rt.sceneMaterials:
    if (rt.classOf(mat) == rt.Multimaterial):
        for idx, sMat in enumerate(mat.materialList):
            if not mat[idx] is None:
                print(mat[idx])
                for map in mat[idx].maps:
                    if not map is None:
                        if not rt.classOf(map) == rt.Normal_Bump:
                            rt.replaceInstances(map, checkForComplexMaps(map))
    elif (rt.classOf(mat) == rt.standardMaterial):
        if not mat is None:
            print(mat)
            for map in mat.maps:
                if not map is None:
                    if not rt.classOf(map) == rt.Normal_Bump:
                        rt.replaceInstances(map, checkForComplexMaps(map))
