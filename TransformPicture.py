import cv2
import numpy as np

class TransformPicture:
    """_summary_
    This class is responsible to curvate the strict picture to be hanged and fit it to the wall sizes
    """
    def __init__(self, filename_input, destination_points,filename_output):
        self.filename = filename_input
        self.img = cv2.imread(filename_input, cv2.IMREAD_UNCHANGED)
        self.height, self.width, channels = self.img.shape
        self.dp = destination_points
        self.filename_output = filename_output

    def transformation(self):

        # np.zeros((img_height, img_width, n_channels), dtype=np.uint8
        black = np.zeros((self.height + 15, self.width + 15, 8), np.uint8)
        #cv2.imwrite('./assets/black.png', black)
        bh, bw, _ = black.shape

        pts_src = np.array([[0.0, 0.0], [float(self.width), 0.0], [float(self.width), float(self.height)], [0.0, float(self.height)]])

        #pts_dst = np.array([[bw * 0.25, 0], [bw * 0.5, 0.0], [float(bw), float(bh)], [0.0, float(bh)]])
        pts_dst = np.array([[self.dp[0].x, self.dp[0].y],[self.dp[1].x, self.dp[1].y],[self.dp[2].x, self.dp[2].y],[self.dp[3].x, self.dp[3].y]])
        #pts_dst = np.array([[self.dp[0].x* 0.25, self.dp[0].y],[self.dp[1].x, self.dp[1].y],[float(bw), float(bh)],[0.0, float(bh)]])
        h, status = cv2.findHomography(pts_src, pts_dst)
        im_out = cv2.warpPerspective(self.img, h, (black.shape[1], black.shape[0]))
        cv2.imwrite(self.filename_output, im_out)


if __name__ == "__main__":
    t = TransformPicture('./assets/Rotated Image.png')
    t.transformation()






