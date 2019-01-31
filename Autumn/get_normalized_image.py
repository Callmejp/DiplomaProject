import cv2
import numpy as np
from scipy import misc


class AutumnModel(object):
    def __init__(self):
        self.prev_image = None
        self.last = []
        self.steps = []

    def process(self, img):
        prev_image = self.prev_image if self.prev_image is not None else img
        self.prev_image = img
        prev = cv2.cvtColor(prev_image, cv2.COLOR_RGB2GRAY)
        nxt = cv2.cvtColor(img, cv2.COLOR_RGB2GRAY)

        flow = cv2.calcOpticalFlowFarneback(prev, nxt, None, 0.5, 3, 15, 3, 5, 1.2, 0)

        self.last.append(flow)

        if len(self.last) > 4:
            self.last.pop(0)

        weights = [1, 1, 2, 2]
        last = list(self.last)
        for x in range(len(last)):
            last[x] = last[x] * weights[x]

        avg_flow = sum(last) / sum(weights)
        mag, ang = cv2.cartToPolar(avg_flow[..., 0], avg_flow[..., 1])

        hsv = np.zeros_like(prev_image)
        hsv[..., 1] = 255
        hsv[..., 0] = ang * 180 / np.pi / 2
        hsv[..., 2] = cv2.normalize(mag, None, 0, 255, cv2.NORM_MINMAX)
        rgb = cv2.cvtColor(hsv, cv2.COLOR_HSV2RGB)
        return rgb

    def predict(self, img, pid):
        img = self.process(img)
        # img = misc.imresize(img[-400:], [66, 200]) / 255.0
        img = misc.imresize(img[-400:], [66, 200])
        # print(img)
        misc.imsave('tmp_right_save/'+str(pid)+'.jpg', img)


if __name__ == '__main__':
    autumn = AutumnModel()
    for i in range(1, 17):
        image_path = 'tmp_right/' + str(i) + '.jpg'
        image = misc.imread(image_path)
        autumn.predict(image, i)



