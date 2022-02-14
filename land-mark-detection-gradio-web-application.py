import numpy as np
import pandas as pd

import gradio as gr
import PIL.Image as Image
import tensorflow as tf
import tensorflow_hub as hub


TF_MODEL_URL= 'https://tfhub.dev/google/on_device_vision/classifier/landmarks_classifier_asia_V1/1'
LABEL_MAP_URL= 'https://www.gstatic.com/aihub/tfhub/labelmaps/landmarks_classifier_asia_V1_label_map.csv'
IMAGE_SHAPE=(321,321)

classifier=tf.keras.Sequential([hub.KerasLayer(TF_MODEL_URL,input_shape=IMAGE_SHAPE+(3,),
                                               output_key="predictions:logits")])
df=pd.read_csv(LABEL_MAP_URL)
label_map=dict(zip(df.id,df.name))


class_name=list(label_map.values())
def classify_image(image):
    img=np.array(image)/255.0
    img=img[np.newaxis, ...]
    prediction=classifier.predict(img)
    return  label_map[np.argmax(prediction)]



image=gr.inputs.Image(shape=(321,321))
label=gr.outputs.Label(num_top_classes=1)

gr.Interface(
    classify_image,
    image,
    label,
    capture_session=True).launch(debug=True);
