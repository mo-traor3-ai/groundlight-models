import os
import glob
import argparse
from groundlight import Groundlight


def img_source(evaluation: str, pattern="*.jpg"):
    """
    This function takes a folder path containing images to return for use in queries to the Groundlight SDK.
    """
    if evaluation == "original":
        folder_path = "./ppe_images"
    elif evaluation == "updated":
        folder_path = "./new_images"
    
    pattern = pattern
    image_files = glob.glob(os.path.join(folder_path, pattern))

    return image_files


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Initiate image evaluation with the Groundlight SDK and source images.")
    parser.add_argument("--evaluation", type=str, choices=['original', 'updated'],
                        help="Options: 'original' or 'updated'. Run an evaluation on the initial set of images, or the updated set.")
    args = parser.parse_args()

    # this variable is useful after setting a system environment variable for GROUNDLIGHT_PPE
    # GROUNDLIGHT_TOKEN is your Groundlight API key (accessible in "Api tokens")
    GROUNDLIGHT_TOKEN = os.environ.get('GROUNDLIGHT_PPE')

    gl = Groundlight(api_token=GROUNDLIGHT_TOKEN)

    detector = gl.get_or_create_detector(
        name="ppe",
        query="Is the person in the image wearing both their hard hat and safety vest properly?",
        confidence_threshold=0.7
        )

    image_files = img_source(args.evaluation)
    print("\n")

    for img_file_path in image_files:
        image_query = gl.submit_image_query(
            detector=detector,
            image=img_file_path,
            wait=12.0,
            patience_time=12.0,
            confidence_threshold=0.7,
            human_review="ALWAYS"
            )

        print(f"* Processing image: {img_file_path} *")
        print(f"The answer is {image_query.result.label} | Query confidence = {image_query.result.confidence}")
