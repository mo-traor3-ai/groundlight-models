# PPE Detection with the Groundlight Python SDK

Groundlight makes it simple to build reliable visual applications. In this example, the SDK is used to create a Groundlight detector to discern with computer vision whether Personal Protective Equipment, or PPE, is properly worn.

Read the [full Groundlight documentation here](https://code.groundlight.ai/python-sdk/).

[Read my full blog post](https://medium.com/@mo.traor3/ppe-detection-with-the-groundlight-python-sdk-38396c9f9a66) on the project. I've included a few highlights from my blog post below.

## Computer Vision powered by Natural Language

Our goal is to build a working computer vision system powered by natural language in just a few lines of python.

This computer vision system was created to learn whether the person in an image, or video stream, such as in the example below, is properly wearing both their hard hat and safety vest.

Example Image:
![A person (me) wearing a hard hat and safety vest.](/assets/original_model_ppe.png)

It is important to note the query should only resolve to "YES" if both PPE items are properly worn. If one is not worn properly, or out of place, the model should return a result, or label, of "NO."

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

![Terminal Output](/assets/terminal_output.png)

The updated model is beginning to assign labels of "YES" or "NO" at confidences at or above 70% more often!

[Read my blog post](https://medium.com/@mo.traor3/ppe-detection-with-the-groundlight-python-sdk-38396c9f9a66) for a deeper dive on the results.

![Sample Results](/assets/updated-accuracy.png)

### Final Notes

It only took me about 75 labeled images to reliably reach 70%+ confidence with the fastest possible answers from the ML system. This is fantastic for those looking to implement solutions for tasks such as increasing worker safety in your factory, warehouse or construction site. And the more you use your model, the better it becomes!

Thanks to the Groundlight team for your hard work!

--------------------------

### More Resources

To learn more about Groundlight, check out the links below:

1. [Code Documentation](https://code.groundlight.ai/python-sdk/docs/getting-started)
2. [Python SDK on PyPi](https://pypi.org/project/groundlight/) or [GitHub](https://github.com/groundlight/python-sdk)
3. [Company](https://www.groundlight.ai/)
4. [Login to Groundlight App](https://app.groundlight.ai/)
