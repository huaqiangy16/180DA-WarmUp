#Work Cited:
#Medium: Finding Dominant Colour on an Image, https://code.likeagirl.io/finding-dominant-colour-on-an-image-b4e075f98097

import cv2 as cv
import numpy as np
import matplotlib.pyplot as plt
from sklearn.cluster import KMeans

def find_histogram(clt):
    """
    create a histogram with k clusters
    :param: clt
    :return:hist
    """
    numLabels = np.arange(0, len(np.unique(clt.labels_)) + 1)
    (hist, _) = np.histogram(clt.labels_, bins=numLabels)

    hist = hist.astype("float")
    hist /= hist.sum()

    return hist
def plot_colors2(hist, centroids):
    bar = np.zeros((50, 300, 3), dtype="uint8")
    startX = 0

    for (percent, color) in zip(hist, centroids):
        # plot the relative percentage of each cluster
        endX = startX + (percent * 300)
        cv.rectangle(bar, (int(startX), 0), (int(endX), 50),
                      color.astype("uint8").tolist(), -1)
        startX = endX

    # return the bar chart
    return bar

cap = cv.VideoCapture(0)
while(1):
    # Take each frame
    _, frame = cap.read()

    #task 4.4: This calculates the dominate color of a given rectangle for each frame
    cv.rectangle(frame,(210,160),(390,340),(0,255,0),2)
    cv.imshow('frame',frame)
    img = frame[160:340, 210:390] #extract the rectangle from the frame
    cv.imshow('image', img)
    img = cv.cvtColor(img, cv.COLOR_BGR2RGB)
    img = img.reshape((img.shape[0] * img.shape[1],3))
    clt = KMeans(n_clusters=1) #cluster number
    clt.fit(img) 

    hist = find_histogram(clt)
    bar = plot_colors2(hist, clt.cluster_centers_) 

    plt.axis("off")
    plt.imshow(bar)
    plt.show() 
