import cv2
import pickle
import numpy as np
import matplotlib.pyplot as plt

class KeyHeatMap:
    def __init__(self):
        self.keyboard_image_path = './assets/MK101.jpg'
    
    def plot(self, key_dict, alpha=.4):
        if len(key_dict)==0:
            return cv2.imread(self.keyboard_image_path)
        key_dict.pop((888,710), None) # skip the space bar
        k, v = key_dict.keys(), key_dict.values()
        c = self.heatmapColors(np.array(list(v))) # colors
        s = self.markerSize(np.array(list(v))) # sizes
        xy = list(k) # co-ordinates

        keyboard_image = cv2.imread(self.keyboard_image_path) # BGR
        heatmapImg = np.zeros_like(keyboard_image)

        for i in range(len(k)):
            x, y = xy[i]
            color = tuple(map(int, c[i][::-1])) #BGR
            radius = s[i]
            #print(list(k)[i], list(v)[i], x, y, color, radius)
            cv2.circle(heatmapImg, (x, y), radius, color, -1)
        mask = np.sum(heatmapImg, axis=2) > 0

        result = cv2.addWeighted(keyboard_image, 1 - alpha, heatmapImg, alpha, 0)
        result[~mask] = keyboard_image[~mask]
        result = cv2.cvtColor(result, cv2.COLOR_BGR2RGB)
        return result
    
    @staticmethod
    def heatmapColors(arr):
        bins = 20
        heatmap_color_map = plt.cm.RdBu(np.linspace(0, 1, bins))
        heatmap_color_map = (heatmap_color_map[:, :3] * 255).astype(np.uint8)
        colors = heatmap_color_map[(arr/arr.max()*bins-1).astype(int)]
        return colors
    
    @staticmethod
    def markerSize(arr, minr=25, maxr=75):
        radii = (minr+(maxr-minr)*arr/max(arr)).astype(int)
        return radii


class Mappings:
    def __init__(self):
        with open('./assets/coordinates.pkl', 'rb') as file:
            self.coordinates_dicts = pickle.load(file)
    def get_coord(self, key):
        return self.coordinates_dicts['lower'].get(key, self.coordinates_dicts['upper'].get(key))