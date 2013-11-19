import heatmap
import random

import heatmap
import random

hm = heatmap.Heatmap()
pts = [(random.uniform(-77.012, -77.050), random.uniform(38.888, 38.910)) for x in range(100)]
hm.heatmap(pts)
hm.saveKML("data.kml")

if __name__ == "__main__":    
    pts = []
    for x in range(400):
        pts.append((random.random(), random.random() ))

    print "Processing %d points..." % len(pts)

    hm = heatmap.Heatmap()
    img = hm.heatmap(pts)
    img.save("classic.png")
    
    