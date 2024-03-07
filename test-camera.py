import cv2


def show_stream():
    """Test the camera stream to verify it works.
    """
    # Open the webcam/stream
    # Try 1 or 2 if 0 does not give any picture or accesses the wrong feed
    cap = cv2.VideoCapture(0)

    while True:
        # Capture video from the stream, frame-by-frame
        ret, frame = cap.read()

        # Display the frame
        cv2.imshow('Webcam/Stream', frame)

        # Wait for 'q' key to quit or close the stream
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    # Release the webcam
    cap.release()
    cv2.destroyAllWindows()

if __name__ == '__main__':
    show_stream()
