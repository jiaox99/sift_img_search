import cv2
import glob
import csv
import re
import numpy
import structure_descriptor

idealDimension = (16, 16)
structureDescriptor = structure_descriptor.StructureDescriptor(idealDimension)

testImage = cv2.imread("query/forest.jpg")
rawQueryStructures = structureDescriptor.describe(testImage)

# index
output = open("structure_index.csv", "w")

for imagePath in glob.glob("dataset" + "/*.jpg"):
    imageName = imagePath[imagePath.rfind("/") + 1 : ]
    image = cv2.imread(imagePath)
    structures = structureDescriptor.describe(image)
    # write structures to file
    structures = [str(structure).replace("\n", "") for structure in structures]
    output.write("%s,%s\n" % (imageName, ",".join(structures)))
# close index file
output.close()

# searcher

def solveStructureDistance(self, structures, queryStructures, eps = 1e-5):
    distance = 0
    for index in range(len(queryStructures)):
        for subIndex in range(len(queryStructures[index])):
            a = structures[index][subIndex]
            b = queryStructures[index][subIndex]
            distance += (a - b) ** 2 / (a + b + eps)
    return distance / 5e3

queryStructures = []
for substructure in rawQueryStructures:
    structure = []
    for line in substructure:
        for tripleColor in line:
            structure.append(float(tripleColor))
    queryStructures.append(structure)
searchResults = {}
with open("structure_index.csv") as indexFile:
    reader = csv.reader(indexFile)
    for line in reader:
        structures = []
        for structure in line[1:]:
            structure = structure.replace("[", "").replace("]", "")
            structure = re.split("\s+", structure)
            if structure[0] == "":
                structure = structure[1:]
            structure = [float(eachValue) for eachValue in structure]
            print(len(structure))
            structures.append(structure)
        distance = solveStructureDistance(structures, queryStructures)
        searchResults[line[0]] = distance
    indexFile.close()
searchResults = sorted(searchResults.iteritems(), key=lambda item: item[1], reverse=False)

print(searchResults)
