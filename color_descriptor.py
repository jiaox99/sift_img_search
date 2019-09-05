import cv2
import numpy

class ColorDescriptor:
    __slot__ = ["bins"]
    def __init__(self, bins):
        self.bins = bins
    def getHistogram(self, image, mask, isCenter):
        # get histogram
        imageHistogram = cv2.calcHist([image], [0, 1, 2], mask, self.bins, [0, 180, 0, 256, 0, 256])
        # normalize
        imageHistogram = cv2.normalize(imageHistogram, imageHistogram).flatten()
        if isCenter:
            weight = 5.0
            for index in range(len(imageHistogram)):
                imageHistogram[index] *= weight
        return imageHistogram
    def describe(self, image):
        image = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)
        features = []
        # get dimension and center
        height, width = image.shape[0], image.shape[1]
        centerX, centerY = int(width * 0.5), int(height * 0.5)
        # initialize mask dimension
        segments = [(0, centerX, 0, centerY), (0, centerX, centerY, height), (centerX, width, 0, centerY), (centerX, width, centerY, height)]
        # initialize center part
        axesX, axesY = int(width * 0.75 / 2), int(height * 0.75 / 2)
        ellipseMask = numpy.zeros([height, width], dtype="uint8")
        # print(centerX, centerY, axesX, axesY, sep=' - ')
        cv2.ellipse(ellipseMask, (centerX, centerY), (axesX, axesY), 0, 0, 360, 255, -1)
        # initialize corner part
        for startX, endX, startY, endY in segments:
            cornerMask = numpy.zeros([height, width], dtype="uint8")
            cv2.rectangle(cornerMask, (startX, startY), (endX, endY), 255, -1)
            cornerMask = cv2.subtract(cornerMask, ellipseMask)
            # get histogram of corner part
            imageHistogram = self.getHistogram(image, cornerMask, False)
            features.append(imageHistogram)
        # get histogram of center part
        imageHistogram = self.getHistogram(image, ellipseMask, True)
        features.append(imageHistogram)
        # return
        return features