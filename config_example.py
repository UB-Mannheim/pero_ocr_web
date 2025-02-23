import os

pero_ocr_web_data = os.environ['HOME'] + '/data/pero_ocr_web_data'
database_url = 'postgresql://postgres:pero@localhost:5432/pero_ocr_web'
# database_url = 'sqlite:///' + pero_ocr_web_data + '/db.sqlite'

class Config(object):
    DEBUG = True
    UPLOADED_IMAGES_FOLDER = pero_ocr_web_data + '/uploaded_images/'
    PREVIEW_IMAGES_FOLDER = pero_ocr_web_data + '/preview_images/'
    LAYOUT_RESULTS_FOLDER = pero_ocr_web_data + '/layout_analysis_results/'
    OCR_RESULTS_FOLDER = pero_ocr_web_data + '/ocr_results/'
    MODELS_FOLDER = pero_ocr_web_data + '/models'
    LAYOUT_DETECTORS_FOLDER = pero_ocr_web_data + '/layout_detectors'
    KEYBOARD_FOLDER = pero_ocr_web_data + '/keyboard'
    EXTENSIONS = ('jpg', 'png', 'pdf', 'jpeg', 'jp2')
    SECRET_KEY = '35q0HKGItx35FvnC4G3uUrXXXzH8RBZ3'
    JSONIFY_PRETTYPRINT_REGULAR = False
    JSON_SORT_KEYS = False
    # EMAIL_NOTIFICATION_ADDRESSES =
    # MAIL_SERVER =
    # MAIL_SENDER =
