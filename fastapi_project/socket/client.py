import cv2
import socket
import json

# 서버 정보 입력
SERVER_IP = "127.0.0.1"
SERVER_PORT = 5005
BUFFER_SIZE = 8192

# UDP 소켓 정보 입력
sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
addr = (SERVER_IP, SERVER_PORT)

# 비디오 캡처 설정
vcap = cv2.VideoCapture(0)

while True:
    # ret: 카메라 작동 상태, frame: 카메라 이미지
    ret, frame = vcap.read()
    if not ret:
        print("카메라가 작동하지 않습니다")
        break

    # 좌우 반전
    frame = cv2.flip(frame, 1)

    # 이미지 압축 후 전송
    _, buffer = cv2.imencode(".jpg", frame) # openCV 이미지를 JPG 형식으로 압축
    request_data = buffer.tobytes()
    for i in range(0, len(request_data), BUFFER_SIZE):
        chunk = request_data[i:i + BUFFER_SIZE]
        sock.sendto(chunk, addr)        # 부분 전송
    sock.sendto(b"END", addr)           # 전송 종료 신호

    # 서버에서 데이터 응답
    response_data = []
    while True:
        chunk, _ = sock.recvfrom(BUFFER_SIZE)
        if chunk == b"END":
            break 
        response_data.append(chunk)
    
    # 데이터 병합
    response_data = b"".join(response_data)
    response_data = json.loads(response_data)
    # print(response_data)

    # 랜드마크 출력
    height, width, _ = frame.shape
    for hand_data in response_data.values():
        for landmark in hand_data:
            x = int(landmark["x"] * width)
            y = int(landmark["y"] * height)
            cv2.circle(frame, (x, y), 5, (0, 0, 255), 2)

    # 이미지 출력
    cv2.imshow("Webcam", frame)

    # ESC(27) 누르면 종료
    key = cv2.waitKey(1)
    if key == 27:
        break

# 리소스 정리
vcap.release()
cv2.destroyAllWindows()
sock.close()