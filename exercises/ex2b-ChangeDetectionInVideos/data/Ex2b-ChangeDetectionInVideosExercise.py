import time
import cv2
import numpy as np
from skimage.util import img_as_float
from skimage.util import img_as_ubyte


def show_in_moved_window(win_name, img, x, y):
    """
    Show an image in a window, where the position of the window can be given
    """
    cv2.namedWindow(win_name)
    cv2.moveWindow(win_name, x, y)
    cv2.imshow(win_name,img)


def capture_from_camera_and_show_images():
    print("Starting image capture")

    print("Opening connection to camera")
    url = 0
    use_droid_cam = False
    if use_droid_cam:
        url = "http://10.10.4.228:4747/video"
    cap = cv2.VideoCapture(url)
    # cap = cv2.VideoCapture(0)
    if not cap.isOpened():
        print("Cannot open camera")
        exit()

    print("Starting camera loop")
    # Get first image
    ret, frame = cap.read()
    # if frame is read correctly ret is True
    if not ret:
        print("Can't receive frame")
        exit()

    # Transform image to gray scale and then to float, so we can do some processing
    bg_frame_gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    bg_frame_gray = img_as_float(bg_frame_gray)

    # To keep track of frames per second
    start_time = time.time()
    n_frames = 0
    stop = False
    while not stop:
        ret, new_frame = cap.read()
        if not ret:
            print("Can't receive frame. Exiting ...")
            break

        # Transform image to gray scale and then to float, so we can do some processing
        new_frame_gray = cv2.cvtColor(new_frame, cv2.COLOR_BGR2GRAY)
        new_frame_gray = img_as_float(new_frame_gray)

        # Compute difference image
        dif_img = np.abs(new_frame_gray - bg_frame_gray)

        # Create thresholded image
        T = 0.1
        bin_img = np.zeros_like(dif_img)
        bin_img[dif_img > T] = 1
        bin_img[dif_img <= T] = 0
        bin_img = img_as_ubyte(bin_img)

        F = (bin_img > 0).sum()
        F_proc = F / bin_img.size * 100

        # Keep track of frames-per-second (FPS)
        n_frames = n_frames + 1
        elapsed_time = time.time() - start_time
        fps = int(n_frames / elapsed_time)

        # Put the FPS on the new_frame
        str_out = f"fps: {fps}"
        font = cv2.FONT_HERSHEY_COMPLEX
        cv2.putText(new_frame, str_out, (100, 100), font, 1, 255, 1)

        # Change Detection Alarm
        A = 5
        if F_proc > A:
            str_out = f"Change Alarm!: {F_proc:.2f}%"
            font = cv2.FONT_HERSHEY_COMPLEX
            cv2.putText(new_frame, str_out, (100, 150), font, 1, (0, 0, 255), 1)

        # Display the resulting frame
        show_in_moved_window('Input', new_frame, 0, 10)
        show_in_moved_window('Background', bg_frame_gray, 600, 10)
        show_in_moved_window('Difference', dif_img, 1200, 10)
        show_in_moved_window('Binary', bin_img, 0, 600)

        # Old frame is updated
        a = 0.95
        bg_frame_gray = a * bg_frame_gray + (1 - a) * new_frame_gray

        if cv2.waitKey(1) == ord('q'):
            stop = True

    print("Stopping image loop")
    cap.release()
    cv2.destroyAllWindows()


if __name__ == '__main__':
    capture_from_camera_and_show_images()
