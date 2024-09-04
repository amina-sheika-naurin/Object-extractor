from flask import Flask, request, jsonify
from datetime import datetime
from detect_compo import ip_region_proposal as ip
from cnn.CNN import CNN

from conf import conf
import base64
import shutil
import cv2
import os



app = Flask(__name__)

@app.route("/")
def greet():
    return "Object extractor"

def resize_height_by_longest_edge(img_path, resize_length=800):
    org = cv2.imread(img_path)
    height, width = org.shape[:2]
    if height > width:
        return resize_length
    else:
        return int(resize_length * (height / width))

def extract_feature_sync(input_path_img):
    try:
        key_params = {'min-grad': 10, 'ffl-block': 5, 'min-ele-area': 50,
                      'merge-contained-ele': True, 'merge-line-to-paragraph': False, 'remove-bar': True}
        resized_height = resize_height_by_longest_edge(input_path_img, resize_length=800)


        compo_classifier = {}
        compo_classifier['Elements'] = CNN('Elements')
        detected_compo = ip.compo_detection(input_path_img, key_params,
                               classifier=compo_classifier, resize_by_height=resized_height, show=False)
        
        return  detected_compo

    except Exception as e:
        print("An error occurred:", e)
   



@app.route('/features-extraction', methods=['POST'])
def fetch_features():
    try:
        data = request.json
        if 'image' not in data:
            return 'No image data found in payload', 400

        image_data = base64.b64decode(data['image'])

        current_datetime = datetime.now().strftime("%Y%m%d%H%M%S")

        temp_folder = os.path.join(conf.get_temp(), current_datetime)
        os.makedirs(temp_folder)
        
        conf.set_temp_folder(temp_folder)

        temp_image_file_path = os.path.join(conf.get_temp_folder(), f'{current_datetime}.jpg')
        with open(temp_image_file_path, 'wb') as f:
            f.write(image_data)

        conf.set_image_path(temp_image_file_path)

        extracted_features = extract_feature_sync( conf.get_image_path())
        
        if extracted_features:
            response = jsonify(extracted_features)
        else:
            response = 'No JSON data found', 404
        return response
    except Exception as e:
        return 'An unexpected error occurred', 500
    finally:
        shutil.rmtree(conf.get_temp_folder())


if __name__ == "__main__":
    app.run(host='0.0.0.0')
