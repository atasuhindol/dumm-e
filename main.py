import time

from controllers.motor_controller import MotorController
from controllers.sensor_controller import SensorController
from controllers.camera_controller import CameraController
from controllers.display_controller import DisplayController
from ai.face_recognition import FaceRecognition
from ai.speech_recognition import SpeechRecognition
from ai.chatbot import ChatBot

def main():
    print("Booting")

    motor_ctrl = MotorController()
    sensor_ctrl = SensorController()
    camera_ctrl = CameraController()
    display_ctrl = DisplayController()
    face_ai = FaceRecognition()
    speech_ai = SpeechRecognition()
    chatbot_ai = ChatBot()

    display_ctrl.init_display()
    motor_ctrl.initialize_motors()
    sensor_ctrl.initialize_sensors()
    camera_ctrl.start_camera()

    try:
        while True:
            # Yüz algılama
            face_detected = camera_ctrl.detect_face()
            if face_detected:
                display_ctrl.show_eyes("happy")
                motor_ctrl.react_to_face()
            else:
                display_ctrl.show_eyes("neutral")

            # Engel algılama
            if sensor_ctrl.obstacle_detected():
                motor_ctrl.avoid_obstacle()

            # Sesli komut dinleme ve cevap
            command = speech_ai.listen()
            if command:
                response = chatbot_ai.get_response(command)
                speech_ai.speak(response)

            time.sleep(0.1)  # Döngü hız kontrolü

    except KeyboardInterrupt:
        print("\nRobot stopped")
        motor_ctrl.stop_all()
        display_ctrl.clear_display()

if __name__ == "__main__":
    main()
