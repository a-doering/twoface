import numpy as np
import cv2

FACIAL_LANDMARKS_IDXS = {}
FACIAL_LANDMARKS_IDXS["left_eye"] = (468, 468 + 5)
FACIAL_LANDMARKS_IDXS["right_eye"] = (468 + 6, 468 + 10)


class FaceAligner:
    def __init__(
        self,
        detector,
        left_point_pos_out=(0.4, 0.4),
        face_width_out=512,
        face_height_out=None,
    ):
        self.detector = detector
        self.left_point_pos_out = left_point_pos_out
        self.face_width_out = face_width_out
        self.face_height_out = face_height_out if face_height_out else face_width_out

    def align(self, image):
        detection_result = self.detector.detect(image)
        landmarks = detection_result.face_landmarks[0]
        # extract the left and right eye (x, y)-coordinates
        (left_idx_start, left_idx_end) = FACIAL_LANDMARKS_IDXS["left_eye"]
        (right_idx_start, right_idx_end) = FACIAL_LANDMARKS_IDXS["right_eye"]
        left_points = np.array(
            [
                [landmarks[i].x * image.width, landmarks[i].y * image.height]
                for i in range(left_idx_start, left_idx_end)
            ]
        )
        right_points = np.array(
            [
                [landmarks[i].x * image.width, landmarks[i].y * image.height]
                for i in range(right_idx_start, right_idx_end)
            ]
        )

        left_center = left_points.mean(axis=0).astype("int")
        right_center = right_points.mean(axis=0).astype("int")

        dy = right_center[1] - left_center[1]
        dx = right_center[0] - left_center[0]
        angle = np.degrees(np.arctan2(dy, dx))

        # Compute output right eye x coordinate
        right_center_x = 1.0 - self.left_point_pos_out[0]

        # Compute scale of output image
        dist = np.sqrt((dx**2) + (dy**2))
        dist_out = right_center_x - self.left_point_pos_out[0]
        dist_out *= self.face_width_out
        scale = dist_out / dist

        # Center between left and right to rotate around
        center = (
            int((left_center[0] + right_center[0]) // 2),
            int((left_center[1] + right_center[1]) // 2),
        )
        rot = cv2.getRotationMatrix2D(center, angle, scale)

        # Translation component of matrix
        tx = self.face_width_out * 0.5
        ty = self.face_height_out * self.left_point_pos_out[1]
        rot[0, 2] += tx - center[0]
        rot[1, 2] += ty - center[1]

        (w, h) = (self.face_width_out, self.face_height_out)
        output = cv2.warpAffine(image.numpy_view(), rot, (w, h), flags=cv2.INTER_CUBIC)
        return output
