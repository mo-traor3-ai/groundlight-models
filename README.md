# PPE Detection with the Groundlight Python SDK

Groundlight makes it simple to build reliable visual applications. In this example, the SDK is used to create a Groundlight detector to discern with computer vision whether Personal Protective Equipment, or PPE, is properly worn.

Read the [full Groundlight documentation here](https://code.groundlight.ai/python-sdk/).

[Read my full blog post](https://medium.com/@mo.traor3/ppe-detection-with-the-groundlight-python-sdk-38396c9f9a66) on the project. I've included a few highlights from my blog post below.

## Computer Vision powered by Natural Language

Our initial goal is to build a working computer vision system powered by natural language in just a few lines of python.

This computer vision system was created to learn whether the person in an image or video stream, such as in the example below, is properly wearing both their hard hat and safety vest.

Example Image:
![A person (me) wearing a hard hat and safety vest.](/assets/original_model_ppe.png)

It is important to note the query should only resolve to "YES" if both PPE items are properly worn. If one is not worn properly, or out of place, the model should return a result, or label, of "NO."

### Running Initial Tests

(1) First, create your virtual environment, and be sure you are running a Python version between `3.7 and 3.12`

Python 3.8 Example (Linux):

```bash
python3.8 venv groundlight

source groundlight/bin/activate

pip install groundlight
```

(2) Head over to [app.groundlight.ai](https://app.groundlight.ai/) and create an account if you haven't already.

(3) Next, create an environment variable for your Groundlight detector. I've titled my environment variable, `GROUNDLIGHT_PPE`. Replace `groundlight_token` in the example below with your own Groundlight API key.

```bash
export GROUNDLIGHT_PPE=groundlight_token
```

(4) Finally, add the code snippet below to a new Python file in your working project directory.

```python
from groundlight import Groundlight


# this variable is useful after setting a system environment variable for GROUNDLIGHT_PPE
GROUNDLIGHT_TOKEN = os.environ.get('GROUNDLIGHT_PPE')

gl = Groundlight(api_token=GROUNDLIGHT_TOKEN)

detector = gl.get_or_create_detector(
    name="ppe",
    query="Is the person in the image wearing both their hard hat and safety vest properly?",
    confidence_threshold=0.7
    )

# in my examples, the images in question are located in /ppe_images and /new_images
img = "./path/to/image.jpg"  # Image can be a file or a Python object
image_query = gl.submit_image_query(detector=detector, image=img)

# Example outputs:
# The answer is Label.NO | Image query confidence = 0.5051044207860879
# The answer is Label.YES | Image query confidence = 0.5026595357619468
print(f"The answer is {image_query.result.label} | Query confidence = {image_query.result.confidence}
```

In the code snippet above, the confidence threshold is set to 0.7, or 70%. My goal is to end up with a model that is at least 70% sure the PPE is properly worn.

This is because in a manufacturing setting, it is better to be safe than sorry when it comes to worker safety. This system can also give us visual data to aid in workplace safety audits, and accident investigations.

* [More Industrial and Manufacturing Applications](https://code.groundlight.ai/python-sdk/docs/building-applications/industrial)

### Creating a Better Model

After running some initial queries, and adding ground truth labels within the Groundlight app, we notice much higher confidence in our query results:

![Terminal Output](/assets/terminal_output.png)

The updated model is beginning to assign labels of "YES" or "NO" at confidences at or above 70% more often!

[Read my blog post](https://medium.com/@mo.traor3/ppe-detection-with-the-groundlight-python-sdk-38396c9f9a66) for a deeper dive on the results and model optimization process.

![Sample Results](/assets/updated-accuracy.png)

### Final Notes

After less than an hour of tinkering, I was able to reliably reach 70%+ confidence with the fastest possible answers and at the lowest latency from the ML system. This is fantastic for those looking to implement solutions for tasks such as increasing worker safety in their factory, warehouse or construction site. And the more you use your model, the better it becomes!

From here, I went on to utilize the ["Dog-on-Couch Detector" example](https://code.groundlight.ai/python-sdk/docs/getting-started/dog-on-couch) from the Groundlight documentation to create my own live feed detector.

After adding my own customizations to the live feed detector, if the person in the worksite area is not properly wearing their safety vest and hardhat, then an audio file is played that prompts them to wear the items, or adjust them so that they are worn properly.

![Terminal Output: Audio Warning for PPE detector](/assets/terminal-output-audio.png)

* As an added bonus, verification of the event is logged to the terminal

Read the "Added Functionality: Warning Sounds" section of the [blog post](https://medium.com/@mo.traor3/ppe-detection-with-the-groundlight-python-sdk-38396c9f9a66) to learn more about my own custom implementation.

Thanks to the Groundlight team for your hard work on the API and SDK!

--------------------------

### More Resources

To learn more about Groundlight, check out the links below:

1. [Code Documentation](https://code.groundlight.ai/python-sdk/docs/getting-started)
2. [Python SDK on PyPi](https://pypi.org/project/groundlight/) or [GitHub](https://github.com/groundlight/python-sdk)
3. [Company](https://www.groundlight.ai/)
4. [Login to Groundlight App](https://app.groundlight.ai/)
