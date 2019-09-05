import os
import numpy as np
from PIL import Image
import glob
import pickle
from datetime import datetime
from flask import Flask, request, render_template
import color_descriptor
import structure_descriptor
import searcher
import argparse
import cv2


app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        file = request.files['query_img']

        img = Image.open(file.stream)  # PIL image
        uploaded_img_path = "static/query/" + file.filename
        img.save(uploaded_img_path)

        idealBins = (8, 12, 3)
        idealDimension = (16, 16)

        colorDescriptor = color_descriptor.ColorDescriptor(idealBins)
        structureDescriptor = structure_descriptor.StructureDescriptor(idealDimension)
        queryImage = cv2.imread(uploaded_img_path)
        colorIndexPath = "static/color_index.csv"
        structureIndexPath = "static/structure_index.csv"
        resultPath = "static/dataset"

        queryFeatures = colorDescriptor.describe(queryImage)
        queryStructures = structureDescriptor.describe(queryImage)

        imageSearcher = searcher.Searcher(colorIndexPath, structureIndexPath)
        searchResults = imageSearcher.search(queryFeatures, queryStructures)

        return render_template('index.html',
                               query_path=uploaded_img_path,
                               scores=searchResults)
    else:
        return render_template('index.html')

if __name__=="__main__":
    app.run("127.0.0.1")
