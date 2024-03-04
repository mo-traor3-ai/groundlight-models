# PPE Detection with the Groundlight Python SDK

Groundlight makes it simple to build reliable visual applications. In this example, the SDK is used to create a Groundlight detector to discern with computer vision whether PPE is properly worn.

Read the [full Groundlight documentation here](https://code.groundlight.ai/python-sdk/).

## Computer Vision powered by Natural Language

Build a working computer vision system powered by natural language in just a few lines of python.

This computer vision system was created to learn whether the person in the image is properly wearing both their hard hat and safety vest.

Example Image:
![A person (me) wearing a hard hat and safety vest.](/assets/original_model_ppe.png)

It is important to note the query should only resolve to "yes" if both PPE items are properly worn. If one is not worn properly, or out of place, the model should return a result, or label, of "NO."

```python
import os
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

### Initial Accuracy of the ML System

In the interest of comparing initial results to ground truth labels, or my personal evaluation of queries for each image, I added ground truth labels to the first 18 images I sent to the system via API.

![Original AI system accuracy vs. Ground Truth labels](/assets/original-accuracy.png)

The initial ML system was correct 86% of the time when assigning a label of "YES," and 100% of the time when assigning a label of "NO."

* NOTE: As a reminder, the model is queried with: "Is the person in the image wearing both their hard hat and safety vest properly?"

Unfortunately, the model was less than 70% confident in each prediction, which is below my desired confidence threshold for predictions.

### Testing the Updated Model

Now that I've added ground truth labels to the first 18 images used in model queries, my model should begin to have higher confidence. Again, the reason this is key is because I'd rather be more confident that safety equipment is properly worn, especially if I decide to use this as a real-time verification system, in addition to a post-processing audit system.

Here are my results for queries on my new images, 12 examples were used.

![Example Image](/assets/updated_model_no.png)

![Terminal Output](/assets/terminal_output.png)

The updated model correctly guessed that this image should resolve to "NO" AND at a confidence of 71.4%!

![Overall AI system accuracy vs. Ground Truth labels](/assets/updated-accuracy.png)

After adding updated ground truth labels for images under 70% confidence, you can see in my overall summary my system has a higher "Balanced ML Accuracy," -- 96% vs. the original 93% -- further proof my AI system is progressing nicely!

Overall, our ML system was correct 92% of the time when assigning a label of "YES," and 100% of the time when assigning a label of "NO."

Thanks to the Groundlight team for your hard work!

--------------------------

### More Resources

To learn more about Groundlight, check out the links below:

1. [Code Documentation](https://code.groundlight.ai/python-sdk/docs/getting-started)
2. [Python SDK on PyPi](https://pypi.org/project/groundlight/) or [GitHub](https://github.com/groundlight/python-sdk)
3. [Company](https://www.groundlight.ai/)
4. [Login to Groundlight App](https://app.groundlight.ai/)
