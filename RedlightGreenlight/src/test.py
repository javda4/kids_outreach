import cv2
import threading
import keyboard

class Camera:
    def __init__(self, camera_index=0):
        self.camera_index = camera_index
        self.cap = cv2.VideoCapture(self.camera_index)

    def get_frame(self):
        ret, frame = self.cap.read()
        if not ret:
            print("Error: Couldn't read frame.")
            return None
        return frame

    def release_camera(self):
        self.cap.release()


class TrafficLight:
    def __init__(self):
        self.colors = ["red", "yellow", "green"]
        self.current_color = "red"
        self.user_defined_color = 0

    def change_color(self, user_defined_color):
        index = user_defined_color
        self.current_color = self.colors[index]

    def get_color(self):
        return self.current_color


def key_listener(traffic_light):
    while True:
        if keyboard.is_pressed('r'):
            traffic_light.change_color(0)
        elif keyboard.is_pressed('y'):
            traffic_light.change_color(1)
        elif keyboard.is_pressed('g'):
            traffic_light.change_color(2)


if __name__ == "__main__":
    camera = Camera()
    traffic_light = TrafficLight()
    count = 0
    cv2.namedWindow('Red Light, Green Light', cv2.WINDOW_NORMAL)
    cv2.resizeWindow('Red Light, Green Light', 1920, 1080)

    # Start the thread for keyboard input
    input_thread = threading.Thread(target=key_listener, args=(traffic_light,), daemon=True)
    input_thread.start()

    while True:
        frame = camera.get_frame()
        if frame is not None:
            color = traffic_light.get_color()
            if color == "red":
                cv2.circle(frame, (100, 50), 5, (0, 0, 255), 50)
            elif color == "yellow":
                cv2.circle(frame, (100, 100), 5, (0, 255, 255), 50)
            elif color == "green":
                cv2.circle(frame, (100, 150), 5, (0, 255, 0), 50)

            cv2.imshow("Red Light, Green Light", frame)
            print(traffic_light.get_color())

        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    camera.release_camera()
    cv2.destroyAllWindows()
