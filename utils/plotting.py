import cv2
import pickle
import numpy as np
from io import BytesIO
import matplotlib.pyplot as plt
from scipy.stats import gaussian_kde

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
    

def plot_kde(data):
    import matplotlib
    matplotlib.use('agg')
    kde = gaussian_kde(data)
    x = np.linspace(min(data), max(data), 1000)
    y = kde(x)

    plt.figure(figsize=(12, 6))
    plt.plot(x, y, color='blue', linewidth=1)
    plt.fill_between(x, y, color='lightblue')

    # Plot vertical line for latest value
    plt.axvline(x=data[-1], color='red', linestyle='--', linewidth=2)
    plt.box(False)

    # Set ticks on x-axis
    plt.tick_params(axis='both', which='major', labelsize=22)
    plt.xticks([min(data), data[-1], max(data)])
    plt.yticks([])

    byte_stream = BytesIO()
    plt.savefig(byte_stream, format='JPEG')
    byte_stream.seek(0)
    plt.close()
    return byte_stream

def plot_placeholder(text='Not enough data! \n keep practicing'):
    import matplotlib
    matplotlib.use('agg')
    plt.figure(figsize=(12, 6))
    plt.fill([-0.5, 0.5, 0.5, -0.5], [-0.5, -0.5, 0.5, 0.5], color='aliceblue')
    plt.text(0, 0, text, ha='center', va='center', color='black', fontsize=42)
    plt.axis('off')

    byte_stream = BytesIO()
    plt.savefig(byte_stream, format='JPEG')
    byte_stream.seek(0)
    plt.close()
    return byte_stream