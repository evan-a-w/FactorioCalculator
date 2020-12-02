#base ratios - all values will be per prod and also base units per prod (in per second values)
#iron/copper/stone brick = 0, steel = 1
def furnacespermaterial(material, unitspersecond):
    if material == 0 or material == 1 or material == 3:
        return unitspersecond / 0.625
    if material == 2:
        return unitspersecond / 0.125

def minersperfurnace(furnaces):
    return (furnaces/11)*12
def minersperfurnacestone(furnaces):
    return (furnaces/4)*7
def minersforpersec(persec, materialid):
    if materialid == 8:
        return persec/0.25
    else:
        return persec/0.5
iddictionary = {
    "iron plate smelters":0,
    "copper plate smelters":1,
    "stone brick smelters":2,
    "steel smelters":3,
    "iron ore miners":4,
    "copper ore miners":5,
    "rock miners":6,
    "coal miners":7,
    "uranium ore miners":8,
    "copper cable":9,
    "iron stick":10,
    "gear":11,
    "electronic circuit":12,
    "advanced circuit":13,
    "plastic":14,
    "petroleum":15,
    "sulfur":16,
    "water":17,
    "sulfuric acid":18,
    "processing unit":19,
    "engine unit":20,
    "pipe":21,
    "electric engine unit":22,
    "lubricant":23,
    "heavy oil":24,
    "light oil":25,
    "low density structure":26,
    "red science":27,
    "green science":28,
    "transport belt":29,
    "inserter":30,
    "black science":31,
    "piercing rounds magazine":32,
    "grenade":33,
    "wall":34,
    "firearm magazine":35,
    "blue science":36,
    "purple science":37,
    "rail":38,
    "electric furnace":39,
    "productivity module":40,
    "yellow science":41,
    "flying robot frame":42,
    "battery":43,
    "solid fuel light":44,
    "solid fuel heavy":45,
    "rocket fuel":46,
    "uranium235":47,
    "uranium237":48,
    "uranium fuel cell":49,
    }
idtoname = []
for x in iddictionary:
    idtoname.append(x)
    
materialinfo = [ #indexed by id, 1st value in tuple is the per sec from 1 prod,
    #second value is a list of ingredients, with each one being a tuple
    #of id and per sec required per prod
    #units mined or smelted directly are not accurate, since it depends on the
    #ore yield/oil yield (don't pay attention to ores much)
    (0.625, [(4,0.625)]),
    (0.625, [(5,0.625)]),
    (0.625, [(6,0.625)]),
    (0.125, [(0,0.625)]),
    (0.5,[]),
    (0.5,[]),
    (0.5,[]),
    (0.5,[]),
    (0.25, []),
    (4,[(1,2)]), #copper cable
    (4,[(0,2)]),#iron stick
    (2, [(0,4)]),
    (2, [(0,2),(9,6)]), #elect circuit
    (1/6, [(14,1/3),(9,2/3),(12,1/3)]),
    (2, [(7,1),(15,20)]),
    (), #petroleum
    (2, [(15,30),(17,30)]),
    (), #water
    (50, [(0,1),(16,5),(17,100)]), #sulfuric acid
    (1/10, [(12,2),(13,1/5),(18,1/2)]), #proc unit
    (1/10, [(3,1/10),(11,1/10),(21,1/5)]), #eng unit
    (2, [(0,2)]),
    (1/10, [(12,1/5),(20,1/10),(23,3/2)]), #e-engine unit
    (10, [(24,10)]),
    (), #heavy oil
    (), #light oil
    (1/20, [(1,1),(3,1/10),(14,1/4)]), #low density structure
    (1/5, [(1,1/5),(11,1/5)]),
    (1/6, [(29,1/6),(30,1/6)]), #green science
    (4, [(0,2),(11,2)]),
    (2, [(0,2),(11,2),(12,2)]),
    (1/5, [(32,1/10),(33,1/10),(34,1/5)]),
    (1/3, [(1,5/3),(3,1/3),(35,1/3)]),
    (1/8, [(7,5/4),(0,5/8)]),
    (2, [(2,10)]),
    (1, [(0,4)]),
    (1/12, [(16,1/24),(13,1/8),(20,1/12)]), #blue science
    (1/7, [(38,10/7),(39,1/21),(40,1/21)]),
    (4, [(3,2),(6,2),(10,2)]), #rail
    (1/5, [(3,2),(13,1),(2,2)]), #e-furnace
    (1/15, [(12,1/3),(13,1/3)]),
    (1/7, [(19,2/21),(42,1/21),(26,1/7)]), #y science
    (1/20, [(3,1/20),(43,1/10),(12,3/20),(22,1/20)]), #flying robot frame
    (1/4, [(0,1/4),(1,1/4),(18,5)]), #battery
    (0.5, [(25,5)]),
    (0.5, [(24,10)]),
    (1/30, [(45,1/3),(25,1/3)]),
    (0.7/100/12, [(8,10/12)]),
    (0.993/12, [(8,10/12)]),
    (1/10, [(0,1),(47,1/10),(48,19/10)]),
    ]
def isbaseunit(materialid):
    if len(materialinfo[materialid]) == 0:
        return True
    else:
        return False
def calculatematerialsperprod(materialid):
    info = materialinfo[materialid]
    productions = []
    if not isbaseunit(materialid):
        for infotuple in info[1]:
            if not isbaseunit(infotuple[0]):
                persecondperprod = materialinfo[infotuple[0]][0]
                productions.append((infotuple[0],infotuple[1]/persecondperprod))
            else:
                productions.append((infotuple[0],furnacespermaterial(infotuple[0],infotuple[1])))
    return productions
def listmaterialsforprod(materialid, number, level):
    scalarproductions = []
    for matid, prod in calculatematerialsperprod(materialid):
        try:
            scalarproductions.append((matid, round(prod*number,3)))
        except:
            scalarproductions.append((matid, "Enough"))
    if level == 0:
        print("To create " + str(number), idtoname[materialid], "or",number*materialinfo[materialid][0],"per second requires:\n")
    for matid, prod in scalarproductions:
        print((1+level)*"    "+str(prod), idtoname[matid])
        listmaterialsforprod(matid, prod, level+1)
        if level == 0:
            print("\n")
    
while True:
    materialname = input("What material do you want to make? ")
    matid = 0
    fail = True
    while fail:
        try:
            matid = iddictionary[materialname]
            fail = False
        except:
            materialname = input("I don't know that material... please input again. ")
    prodno = int(input("How many builders do you want? (or 0 if you want the materials for x per second) "))
    if prodno == 0:
        psec = float(input("How many per second? "))
        prodno = psec/materialinfo[matid][0]
    listmaterialsforprod(matid, prodno, 0)
    print("\n")
