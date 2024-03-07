import os
import time
import argparse
import cv2
from groundlight import Groundlight
from PIL import Image
from playsound import playsound


def validate_audio_file(filename: str):
    """Check if the input file is an audio file of type .mp3 or .aac.
    
    Args:
        filename (str): The path of the audio file.

    Returns:
        True or False (bool)
    """
    video_extensions = ['.mp3', '.aac']
    
    return any(filename.endswith(ext) for ext in video_extensions)

def capture_image():
    """Capture an image from the live video stream.
    
    Args:
        None.

    Returns:
        An image object (Image) or None
    """
    cap = cv2.VideoCapture(0)

    ret, frame = cap.read()
    cap.release()

    if ret:
        # Convert to PIL image
        return Image.fromarray(cv2.cvtColor(frame, cv2.COLOR_BGR2RGB))
    else:
        return None

def play_sound(audio_file: str):
    """Play the sound from the input audio file.
    
    Args:
        audio_file (str): The path to the audio file.

    Returns:
        None
    """
    playsound(audio_file)

def run_detector(GROUNDLIGHT_TOKEN: str, waiting_period: int = 60):
    """Activates the detector via the Groundlight SDK. Utilizes capture_image() to
    collect the image, and play_sound() to play our warning sound if our criteria is met.
    
    Args:
        GROUNDLIGHT_TOKEN (str): The API token for the Groundlight detector.
        waiting_period (int): How long to wait (in seconds) between queries to the detector.

    Returns:
        None
    """
    gl = Groundlight(api_token=GROUNDLIGHT_TOKEN)

    detector = gl.get_or_create_detector(
        name="ppe",
        query="Is the person in the image wearing both their hard hat and safety vest properly?",
        confidence_threshold=0.7
        )

    while True:
        image = capture_image()
        if image:
            try:
                iq = gl.submit_image_query(detector=detector,
                                           image=image,
                                           wait=12.0,
                                           patience_time=12.0,
                                           confidence_threshold=0.7,
                                           human_review="ALWAYS"
                                           )
                answer = iq.result.label
                confidence = iq.result.confidence
                if (answer == "NO") & (confidence >= 0.7000):
                    print(f"\n** PPE is not worn, or is worn improperly! (Query Confidence: {confidence:.2%}) **")
                    play_sound("./assets/ppe-warning.mp3")
                elif (answer == "YES") & (confidence >= 0.7000):
                    print(f"\n** PPE is worn properly, no action needed. (Query Confidence: {confidence:.2%}) **")
                elif ((answer == "NO") & (confidence < 0.7000)) | ((answer == "YES") & (confidence < 0.7000)):
                    print(f"\n** NOTE: Query confidence is below desired threshold. (Query Confidence: {confidence:.2%}) **")
            except Exception as e:
                print(f"Error submitting image query: {e}")
        else:
            print("\n*** Failed to capture image. ***")

        # How long to sleep/wait (in seconds) between queries to the detector
        time.sleep(waiting_period)


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description="Initiate evaluation with the Groundlight SDK, source images, and audio file for warnings.")
    parser.add_argument("--audio", default="./assets/ppe-warning.mp3", type=str,
                        help="Enter the path to your own audio file to play for warnings, or the default file ./assets/ppe-warning.mp4 will play.")
    parser.add_argument("--wait", default=60, type=int, help="How long to wait (in seconds) between queries to the detector.")
    args = parser.parse_args()

    # this variable is useful after setting a system environment variable for GROUNDLIGHT_PPE
    # GROUNDLIGHT_TOKEN is your Groundlight API key (accessible in "Api tokens")
    GROUNDLIGHT_TOKEN = os.environ.get('GROUNDLIGHT_PPE')

    validate_audio = validate_audio_file(args.audio)

    if validate_audio:
        run_detector(GROUNDLIGHT_TOKEN, args.wait)
    else:
        print(f"\nThe audio file is not a valid type. Audio file must be of type .mp3 or .aac.")
