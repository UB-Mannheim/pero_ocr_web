import requests
import os
from io import open as image_open
import zipfile




def get_document_folder_path(folder, document_id):
    folder_path = os.path.join(folder, document_id)
    if not os.path.exists(folder_path):
        os.makedirs(folder_path)
    return folder_path


def get_and_save_images(folder, base_url, document_id, images):
    for image in images:
        image_request = requests.get("{}/document/get_image/{}/{}".format(base_url, document_id, image))
        file_type = image_request.headers['content-type'].split('/')[-1]
        path = os.path.join(folder, '{}.{}'.format(image, file_type))
        if image_request.status_code == 200:
            with image_open(path, 'wb') as f:
                f.write(image_request.content)


def get_and_save_xmls(folder, base_url, document_id, images):
    for image in images:
        xml_request = requests.get("{}/document/get_region_xml/{}/{}".format(base_url, document_id, image))
        path = os.path.join(folder, '{}.xml'.format(image))
        if xml_request.status_code == 200:
            with open(path, 'wb') as f:
                f.write(xml_request.content)


def get_and_save_document_images(folder, base_url, route):
    r = requests. get('{}{}'.format(base_url, route))
    return_json = r.json()
    if 'document' in return_json.keys():
        document = return_json['document']
        get_and_save_images(folder, base_url, document['id'], document['images'])
        return return_json['id'], document
    return None, None


def get_and_save_document_xmls(folder, base_url, route):
    r = requests. get('{}{}'.format(base_url, route))
    return_json = r.json()
    if 'document' in return_json.keys():
        document = return_json['document']
        get_and_save_xmls(folder, base_url, document['id'], document['images'])
        return return_json['id'], document
    return None, None


def get_and_save_document_images_and_xmls(images_folder, xmls_folder, base_url, route):
    r = requests. get('{}{}'.format(base_url, route))
    request_json = r.json()
    if 'document' in request_json.keys():
        document = request_json['document']
        get_and_save_images(images_folder, base_url, document['id'], document['images'])
        get_and_save_xmls(xmls_folder, base_url, document['id'], document['images'])
        return request_json['id'], request_json['parse_folder_config_path'], request_json['ocr_json_path'], document
    return None, None, None, None


def get_and_save_request_document_images_and_xmls(base_url, images_folder, xmls_folder, request_json):
    if 'document' in request_json.keys():
        document = request_json['document']
        get_and_save_images(images_folder, base_url, document['id'], document['images'])
        get_and_save_xmls(xmls_folder, base_url, document['id'], document['images'])


def make_post_request_data(output_folder, document):
    data = dict()
    images = document['images']
    for image in images:
        data[image] = open(os.path.join(output_folder, "{}.xml".format(image)), 'rb')
    print('Data:', data)
    return data

def get_models(base_url, route, ocr_name, models_folder):
    r = requests.get('{}{}{}'.format(base_url, route, ocr_name))
    tmp_zip_path = os.path.join(models_folder, "tmp.zip")
    with open(tmp_zip_path, 'wb') as handle:
        handle.write(r.content)
    with zipfile.ZipFile(tmp_zip_path, 'r') as zip_ref:
        zip_ref.extractall(models_folder)
    os.remove(tmp_zip_path)