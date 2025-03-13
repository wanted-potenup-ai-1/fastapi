import socket
import cv2
import numpy as np
import mediapipe as mp
import json

# 서버 설정
SERVER_IP = "127.0.0.1"
SERVER_PORT = 5005
BUFFER_SIZE = 8192  # UDP 패킷 크기 제한

# UDP 소켓 설정
sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
sock.bind((SERVER_IP, SERVER_PORT)) # 서버가 특정 IP와 포트에서 데이터를 받을 준비

# MediaPipe 설정
mp_hands = mp.solutions.hands
hands = mp_hands.Hands(
    static_image_mode=False, 
    max_num_hands=2, 
    min_detection_confidence=0.5, 
    min_tracking_confidence=0.5
)

while True:
    # 클라이언트에서 데이터 받기
    image_data = []
    while True:
        chunk, addr = sock.recvfrom(BUFFER_SIZE)
        if chunk == b"END":
            break 
        image_data.append(chunk)
    image_data = b"".join(image_data)
    np_data = np.frombuffer(image_data, dtype=np.uint8)
    frame = cv2.imdecode(np_data, cv2.IMREAD_COLOR)
    
    if frame is None:
        continue

    # 손 감지
    results = hands.process(frame)

    # 손 랜드마크 추출
    landmark_dict = {"Left": [], "Right": []}
    if results.multi_hand_landmarks:
        for idx, hand_landmarks in enumerate(results.multi_hand_landmarks):
            hand_label = results.multi_handedness[idx].classification[0].label
            # 좌표 모으기(21개
            for landmark in hand_landmarks.landmark:
                landmark_dict[hand_label].append({"x":landmark.x, "y":landmark.y, "z":landmark.z})
            
    # JSON 변환 후 나눠서 전송
    json_data = json.dumps(landmark_dict).encode("utf-8")
    
    for i in range(0, len(json_data), BUFFER_SIZE):
        chunk = json_data[i:i + BUFFER_SIZE]
        sock.sendto(chunk, addr)    # 부분 전송
    sock.sendto(b"END", addr)       # 전송 종료 신호