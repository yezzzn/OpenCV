import random
import cv2
import mediapipe as mp
import time
import cvzone

cap = cv2.VideoCapture(cv2.CAP_DSHOW + 0)
cap.set(cv2.CAP_PROP_FRAME_WIDTH, 1280)
cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)

mpHands = mp.solutions.hands
hands = mpHands.Hands()
mpDraw = mp.solutions.drawing_utils

pTime = 0  # 이전 시간
cTime = 0  # 현재 시간

# 타이머 설정 (초 단위)
timer_duration = 60  # 60초 동안 타이머 실행
start_time = time.time()  # 게임 시작 시간 기록

# 이미지 로드
tomato_img = cv2.imread(r"C:\JIN\opencv_study\p1\pro\minipro\Images\tomato.png")
bun_img = cv2.imread(r"C:\JIN\opencv_study\p1\pro\minipro\Images\bun.png")
cheese_img = cv2.imread(r"C:\JIN\opencv_study\p1\pro\minipro\Images\cheese.png")
patty_img = cv2.imread(r"C:\JIN\opencv_study\p1\pro\minipro\Images\patty.png")
lettuce_img = cv2.imread(r"C:\JIN\opencv_study\p1\pro\minipro\Images\lettuce.png")
bacon_img = cv2.imread(r"C:\JIN\opencv_study\p1\pro\minipro\Images\bacon.png")
base_img = cv2.imread(r"C:\JIN\opencv_study\p1\pro\minipro\Images\base.png")
start_img = cv2.imread(r"C:\JIN\opencv_study\p1\pro\minipro\Images\start_b.JPG")

# 이미지 로드
tomato_png = cv2.imread(
    r"C:\JIN\opencv_study\p1\pro\minipro\Images\tomato.png", cv2.IMREAD_UNCHANGED
)
bun_png = cv2.imread(
    r"C:\JIN\opencv_study\p1\pro\minipro\Images\bun.png", cv2.IMREAD_UNCHANGED
)
cheese_png = cv2.imread(
    r"C:\JIN\opencv_study\p1\pro\minipro\Images\cheese.png", cv2.IMREAD_UNCHANGED
)
patty_png = cv2.imread(
    r"C:\JIN\opencv_study\p1\pro\minipro\Images\patty.png", cv2.IMREAD_UNCHANGED
)
lettuce_png = cv2.imread(
    r"C:\JIN\opencv_study\p1\pro\minipro\Images\lettuce.png", cv2.IMREAD_UNCHANGED
)
bacon_png = cv2.imread(
    r"C:\JIN\opencv_study\p1\pro\minipro\Images\bacon.png", cv2.IMREAD_UNCHANGED
)
base_png = cv2.imread(
    r"C:\JIN\opencv_study\p1\pro\minipro\Images\base.png", cv2.IMREAD_UNCHANGED
)

# 재료 이미지 자리
img_positions = {
    "bun": (0, 0),
    "cheese": (210, 0),
    "patty": (420, 0),
    "tomato": (630, 0),
    "lettuce": (840, 0),
    "bacon": (1050, 0),
}

# 내가 만든 햄버거 이미지 자리
my_positions = {
    "0": (1000, 500),
    "1": (1000, 450),
    "2": (1000, 400),
    "3": (1000, 350),
    "4": (1000, 300),
    "5": (1000, 250),
}

# 만들 햄버거 이미지 자리
ham_positions = {
    "0": (150, 500),
    "1": (150, 450),
    "2": (150, 400),
    "3": (150, 350),
    "4": (150, 300),
}

# 올바른 순서의 재료 목록
correct_order = []

# 재료 랜덤
ing = ["cheese", "bacon", "lettuce", "patty", "tomato"]
random.shuffle(ing)
correct_order = ing

# 완성품
fin_order = correct_order + ["bun"]

# 점수
score = 0

# 완성 플래그
fin = False

myHam = []  # 클릭된 재료를 저장할 리스트

# 게임 시작 상태를 저장하는 변수
game_started = False

# 게임 종료 상태 저장하는 변수
game_ended = False

while True:
    if not game_started:
        # 게임 시작 전 이미지 "start_b.jpg"를 표시
        start_image = cv2.imread(
            r"C:\JIN\opencv_study\p1\pro\minipro\Images\start_b.JPG"
        )
        cv2.imshow("Start Image", start_image)
        key = cv2.waitKey(1)
        # "s" 키를 누르면 게임 시작
        if key == ord("s") or key == ord("S"):
            game_started = True
            cv2.destroyWindow("Start Image")  # 시작 이미지 창 닫기
            start_time = time.time()  # 게임 시작 시간 기록

        continue  # 게임이 시작되지 않았으면 다음 반복으로 넘어감

    success, img = cap.read()
    img = cv2.flip(img, 1)

    # mpDraw.draw_landmarks 함수 호출 전에 이미지를 BGR 형식으로 변환
    img = cv2.cvtColor(img, cv2.COLOR_BGRA2BGR)
    imgRGB = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    results = hands.process(imgRGB)

    if not game_ended:  # game_ended가 False일 때만 타이머 업데이트
        # 타이머가 실행 중일 때 시간을 카운트다운하고 메시지 표시
        elapsed_time = time.time() - start_time
        timer_duration -= elapsed_time
        start_time = time.time()
        cv2.putText(
            img,
            str(int(timer_duration)),
            (600, 700),
            cv2.FONT_HERSHEY_COMPLEX,
            3,
            (255, 0, 0),
            3,
        )
    # 타이머 끝나면 게임 종료 플래그 주기
    if timer_duration <= 0:
        game_ended = True

    # 게임 종료 시 실행
    if game_ended:
        # 게임 종료 이미지 "end_b.jpg"를 표시
        end_image = cv2.imread(r"C:\JIN\opencv_study\p1\pro\minipro\Images\end_b.JPG")
        cv2.putText(
            end_image,
            str(score),
            (250, 230),
            cv2.FONT_HERSHEY_SIMPLEX,
            2,
            (255, 255, 255),
            5,
        )
        cv2.imshow("End Image", end_image)
        key = cv2.waitKey(1)
        # "q" 키를 누르면 게임 종료
        if key == ord("q") or key == ord("Q"):
            cv2.destroyAllWindows()  # 모든 창 닫기
            break

    # 재료 이미지 리스트로 저장
    overlay_images = [
        ("bun", bun_img),
        ("cheese", cheese_img),
        ("patty", patty_img),
        ("tomato", tomato_img),
        ("lettuce", lettuce_img),
        ("bacon", bacon_img),
    ]

    # 재료 이미지 리스트로 저장 - png
    overlay_imagess = [
        ("bun", bun_png),
        ("cheese", cheese_png),
        ("patty", patty_png),
        ("tomato", tomato_png),
        ("lettuce", lettuce_png),
        ("bacon", bacon_png),
    ]

    #  재료 이미지 하나씩 웹캠에 출력
    for overlay_name, overlay_img in overlay_imagess:
        overlay_img = cv2.resize(overlay_img, (200, 120))
        overlay_height, overlay_width, _ = overlay_img.shape
        x_pos, y_pos = img_positions[overlay_name]

        # 알파 채널을 고려하여 이미지 병합
        for c in range(0, 3):
            img[y_pos : y_pos + overlay_height, x_pos : x_pos + overlay_width, c] = img[
                y_pos : y_pos + overlay_height, x_pos : x_pos + overlay_width, c
            ] * (
                1 - overlay_img[:, :, 3] / 255.0
            ) + overlay_img[  # 알파 채널에 따라 가중치를 적용
                :, :, c
            ] * (
                overlay_img[:, :, 3] / 255.0
            )

    # 아래 번 출력
    base_img = cv2.resize(base_png, (180, 100))
    img = cvzone.overlayPNG(img, base_img, (1000, 550))

    # 만들 햄버거 이미지 출력
    # 재료 이미지 배치
    base_img = cv2.resize(base_png, (180, 100))
    img = cvzone.overlayPNG(img, base_img, (150, 550))

    for i, ingredient in enumerate(correct_order):
        for overlay_name, overlay_img in overlay_imagess:
            if ingredient == overlay_name:
                x_my, y_my = ham_positions[str(i)]
                overlay_img = cv2.resize(overlay_img, (180, 100))
                overlay_height, overlay_width, _ = overlay_img.shape
                img = cvzone.overlayPNG(img, overlay_img, (x_my, y_my))
    bun_img = cv2.resize(bun_png, (180, 100))
    img = cvzone.overlayPNG(img, bun_img, (150, 250))

    # 현재 재료 인덱스를 터치하는지 확인
    if results.multi_hand_landmarks:
        for handLandmarks in results.multi_hand_landmarks:
            index_finger_tip = handLandmarks.landmark[8]
            ix, iy = int(index_finger_tip.x * img.shape[1]), int(
                index_finger_tip.y * img.shape[0]
            )
            # 이미지 영역 안에 들어올 때만 재료 추가
            for i, (overlay_name, overlay_img) in enumerate(overlay_imagess):
                spacing = 20
                overlay_x = i * (overlay_width + spacing)
                if (
                    overlay_x <= ix <= overlay_x + overlay_width
                    and y_pos <= iy <= y_pos + overlay_height
                ):
                    if overlay_name not in myHam:
                        myHam.append(overlay_name)
                        print(overlay_name)

                    cv2.putText(
                        img,
                        str(overlay_name),
                        (overlay_x, y_pos + 200),
                        cv2.FONT_HERSHEY_SIMPLEX,
                        2,
                        (255, 0, 255),
                        4,
                    )
    print(myHam)

    # 내가 만든 햄버거 쌓기
    for i in range(0, len(myHam)):
        for overlay_name, overlay_img in overlay_imagess:
            if myHam[i] == overlay_name:
                x_my, y_my = my_positions[str(i)]
                overlay_img = cv2.resize(overlay_img, (180, 100))
                overlay_height, overlay_width, _ = overlay_img.shape
                img = cvzone.overlayPNG(img, overlay_img, (x_my, y_my))

    # 내가 쌓은 햄버거가 맞을 경우
    if fin == False and myHam == fin_order:
        score += 1000
        cv2.putText(
            img, str(score), (600, 500), cv2.FONT_HERSHEY_PLAIN, 5, (255, 0, 255), 4
        )
        myHam = []
        fin = True

    # 틀렸을 경우 초기화
    if len(myHam) == 6 and myHam is not fin_order:
        cv2.putText(
            img,
            str("try again!"),
            (400, 500),
            cv2.FONT_HERSHEY_COMPLEX,
            3,
            (0, 0, 255),
            5,
        )
        # 모든 재료 이미지가 다시 배치되었으므로 햄버거를 다시 만들 수 있도록 초기화
        myHam = []
        fin = False

    # 햄버거가 완성되면 재료 이미지를 다시 배치
    if fin:
        # 새로운 순서로 재료 배치
        random.shuffle(correct_order)
        fin_order = correct_order + ["bun"]

        # 재료 이미지 다시 배치
        for i, ingredient in enumerate(correct_order):
            for overlay_name, overlay_img in overlay_imagess:
                if ingredient == overlay_name:
                    x_my, y_my = ham_positions[str(i)]
                    overlay_img = cv2.resize(overlay_img, (180, 100))
                    overlay_height, overlay_width, _ = overlay_img.shape
                    img = cvzone.overlayPNG(img, overlay_img, (x_my, y_my))
        bun_img = cv2.resize(bun_png, (180, 100))
        img = cvzone.overlayPNG(img, bun_img, (150, 250))

        # 모든 재료 이미지가 다시 배치되었으므로 햄버거를 다시 만들 수 있도록 초기화
        myHam = []
        fin = False

    # 핸드를 인식하면 처리되는 코드
    if results.multi_hand_landmarks:
        for handLandmarks in results.multi_hand_landmarks:
            # 검지 끝 지점의 좌표 가져오기
            index_finger_tip = handLandmarks.landmark[8]
            middle_finger_tip = handLandmarks.landmark[12]
            ix, iy = int(index_finger_tip.x * img.shape[1]), int(
                index_finger_tip.y * img.shape[0]
            )
            # 중지 끝 지점의 좌표 가져오기
            middle_finger_tip_x = int(middle_finger_tip.x * img.shape[1])
            middle_finger_tip_y = int(middle_finger_tip.y * img.shape[0])
            if middle_finger_tip_y < iy:
                myHam.clear()
            # 핸드의 각 관절 포인트의 ID와 좌표를 알아냄
            for id, lm in enumerate(handLandmarks.landmark):
                h, w, c = img.shape
                cx, cy = int(lm.x * w), int(lm.y * h)
                # 검지 끝
                if id == 12:
                    cv2.circle(img, (cx, cy), 15, (90, 180, 0), cv2.FILLED)
                if id == 8:
                    cv2.circle(img, (cx, cy), 15, (90, 180, 0), cv2.FILLED)
                    # 게임 시작 시간 기록
                    if timer_duration == 100 and 0 < cy < 700 and 0 < cx < 1200:
                        start_time = time.time()
                        timer_duration = 100  # 타이머 초기값으로 재설정

    # 점수 텍스트를 추가합니다.
    cv2.putText(
        img, str(score), (600, 500), cv2.FONT_HERSHEY_PLAIN, 5, (255, 0, 255), 4
    )

    # 수정된 이미지를 표시합니다.
    cv2.imshow("Image", img)
    cv2.waitKey(1)
