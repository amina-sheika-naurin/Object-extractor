# config.py
import os

class Conf:

    MERGE_FOLDER_NAME = 'merge'
    OCR_FOLDER_NAME = 'ocr'
    CURRENT_IMAGE = 'current'
    FEATURE_IMAGE = 'feature'

    def __init__(self):
        self.temp = os.path.join(os.path.dirname(__file__), 'tmp')
        self.temp_folder = None
        self.image_path = None  
        self.feature_json_path = None
        self.current_image_path = None
        self.feature_image_path = None  

        # if not os.path.exists(self.temp):
        #     os.makedirs(self.temp)

    def set_image_path(self, image_path):
        self.image_path = image_path
                              
    def set_temp_folder(self, temp_folder_path):
        self.temp_folder = temp_folder_path

    def set_currentimage_path(self, image_path):
        self.current_image_path = image_path
    
    def set_featureimage_path(self, image_path):
        self.feature_image_path = image_path

    def get_currentimage_path(self):
        return self.current_image_path
    
    def get_featureimage_path(self):
        return self.feature_image_path
                              
    def get_temp(self):
        return self.temp
            
    def get_temp_folder(self):
        return self.temp_folder

    def get_image_path(self):
        return self.image_path
        
    def get_merge_folder(self):
        return os.path.join(self.temp_folder, Conf.MERGE_FOLDER_NAME)

    def get_ocr_folder(self):
        return os.path.join(self.temp_folder, Conf.OCR_FOLDER_NAME)

conf = Conf()