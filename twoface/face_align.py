import json

import cv2
import numpy as np

with open("twoface/config.json") as json_file:
    config = json.load(json_file)


class FaceAligner:
    def __init__(
        self,
        detector,
        left_point_pos_out=[0.4, 0.4],
        width_out=1024,
        height_out=None,
    ):
        self.detector = detector
        self.left_point_pos_out = left_point_pos_out
        self.width_out = width_out
        self.height_out = height_out if height_out else width_out

    def align(self, image, zoom=0.0):
        left_point_pos_out = self.left_point_pos_out.copy()
        left_point_pos_out[0] -= zoom

        detection_result = self.detector.detect(image)
        landmarks = detection_result.face_landmarks[0]
        # extract the left and right eye (x, y)-coordinates
        (left_idx_start, left_idx_end) = config["facial_landmark_ids"]["left_eye"]
        (right_idx_start, right_idx_end) = config["facial_landmark_ids"]["right_eye"]
        left_points = np.array(
            [
                [landmarks[i].x * image.width, landmarks[i].y * image.height]
                for i in range(left_idx_start, left_idx_end + 1)
            ]
        )
        right_points = np.array(
            [
                [landmarks[i].x * image.width, landmarks[i].y * image.height]
                for i in range(right_idx_start, right_idx_end + 1)
            ]
        )

        left_center = left_points.mean(axis=0).astype("int")
        right_center = right_points.mean(axis=0).astype("int")

        dy = right_center[1] - left_center[1]
        dx = right_center[0] - left_center[0]
        angle = np.degrees(np.arctan2(dy, dx))

        # Compute output right eye x coordinate
        right_center_x = 1.0 - left_point_pos_out[0]

        # Compute scale of output image
        dist = np.sqrt((dx**2) + (dy**2))
        dist_out = right_center_x - left_point_pos_out[0]
        dist_out *= self.width_out
        scale = dist_out / dist

        # Center between left and right to rotate around
        center = (
            int((left_center[0] + right_center[0]) // 2),
            int((left_center[1] + right_center[1]) // 2),
        )
        rot = cv2.getRotationMatrix2D(center, angle, scale)

        # Translation component of matrix
        tx = self.width_out * 0.5
        ty = self.height_out * self.left_point_pos_out[1]
        rot[0, 2] += tx - center[0]
        rot[1, 2] += ty - center[1]

        output = cv2.warpAffine(
            image.numpy_view(),
            rot,
            (self.width_out, self.height_out),
            flags=cv2.INTER_CUBIC,
        )
        return output
