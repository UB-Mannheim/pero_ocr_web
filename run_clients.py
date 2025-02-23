import configparser
import time
import sys
import requests
import argparse
import safe_gpu
import logging

from client_helper import log_in
from layout_client.run_client import check_and_process_layout_request
from ocr_client.run_client import check_and_process_ocr_request

logging.basicConfig(format='%(asctime)s %(levelname)-8s %(message)s', level=logging.INFO, datefmt='%Y-%m-%d %H:%M:%S')
module_logger = logging.getLogger('pero_ocr_web.run_clients')


def get_args():
    """
    method for parsing of arguments
    """
    parser = argparse.ArgumentParser()
    parser.add_argument("--time-limit", default=-1, type=float, help="Exit when running longer than time-limit hours.")
    parser.add_argument("--gpu-mode", action='store_true', help="If set, jobs will run only if GPU is available.")
    args = parser.parse_args()

    return args


def main():
    args = get_args()
    start_time = time.time()

    layout_config = configparser.ConfigParser()
    layout_config.read("layout_client/config.ini")
    ocr_config = configparser.ConfigParser()
    ocr_config.read("ocr_client/config.ini")
    timeout = 4

    with requests.Session() as session:
        if not log_in(session, layout_config['SETTINGS']['login'], layout_config['SETTINGS']['password'],
                      layout_config['SERVER']['base_url'],
                      layout_config['SERVER']['authentication'], layout_config['SERVER']['login_page']):
            module_logger.error('Unable to log into server')
        else:
            while True:
                if args.time_limit > 0 and args.time_limit * 3600 < time.time() - start_time:
                    return
                nothing = True
                if check_and_process_layout_request(layout_config, session, args.gpu_mode):
                    nothing = False
                if check_and_process_ocr_request(ocr_config, session, args.gpu_mode):
                    nothing = False
                if nothing:
                    time.sleep(timeout)


if __name__ == '__main__':
    sys.exit(main())
