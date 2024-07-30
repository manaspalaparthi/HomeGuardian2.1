import numpy as np
from pyzbar import pyzbar as bar

import cv2

class QRCodeScanner:
    def __init__(self):
        pass

    def scan(self, image):
        # Find barcodes and QR codes
        decodedObjects = bar.decode(image)

        # Print results
        for obj in decodedObjects:
            print('Type : ', obj.type)
            print('Data : ', obj.data, '\n')

        return decodedObjects

    def read(self, image_path):
        # Read image
        image = cv2.imread(image_path)

        # Display images
        cv2.imshow("Image", image)

        decodedObjects = self.scan(image)

        for decodedObject in decodedObjects:
            points = decodedObject.polygon

            # If the points do not form a quad, find convex hull
            if len(points) > 4:
                hull = cv2.convexHull(np.array([point for point in points], dtype=np.float32))
                hull = list(map(tuple, np.squeeze(hull)))
            else:
                hull = points

            # Number of points in the convex hull
            n = len(hull)

            # Draw the convext hull
            for j in range(0, n):
                cv2.line(image, hull[j], hull[(j + 1) % n], (255, 0, 0), 3)

        cv2.imshow("Result", image)
        cv2.waitKey(0)
        cv2.destroyAllWindows()