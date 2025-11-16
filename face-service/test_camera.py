import cv2

print("Testing camera detection...")
for i in range(10):
    print(f"\nTrying index {i}...")
    cap = cv2.VideoCapture(i)
    is_open = cap.isOpened()
    print(f"  isOpened: {is_open}")
    if is_open:
        ret, frame = cap.read()
        print(f"  can read frame: {ret}")
        print(f"  frame shape: {frame.shape if ret else 'N/A'}")
    cap.release()
    print(f"  released")
