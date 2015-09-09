#! /usr/bin/env python3

import sys
import os
import argparse
import logging
import zipfile

try:
    import requests
except:
    print ("You are missing the requests library, please install it")
    sys.exit(-1)

if __name__ == "__main__":
    print ("STM32 Cube Installation")
    ##
    ## Parse Command Line Arguments
    ##
    parser = argparse.ArgumentParser(
        description='STM32 Cube Installer')
    parser.add_argument("-D", "--debug",
                        help="Debug this script",
                        action="store_true")
    parser.add_argument("--cube4",
                        help="Install STM32F4 Cube",
                        action="store_true")
    parser.add_argument("--cube3",
                        help="Install STM32F3 Cube",
                        action="store_true")    
    parser.add_argument("--log_file",
                        default="cube_install.log",                        
                        help="LOG File of this program",
                        action="store")

    
    args = parser.parse_args()
    if args.debug:
        print (args)

    ##
    ## Start a LOG file of our activities
    ##
    logging.basicConfig(filename=args.log_file,
                        level=logging.DEBUG,
                        format=
                        '%(asctime)s, %(levelname)s, %(message)s',
                        datefmt=
                        '%m/%d/%Y %I:%M:%S %p')
    
    logging.info("Application Started")

    if args.cube3:
        print ("Downloading and Installing Stm32F3 Cube")
        logging.info("Downloading and Installing Stm32F3 Cube")
        dir_list = os.getcwd().split("/")
        dir_str = "/".join(dir_list[:-1])
        print (dir_str)
        URL = "http://www.st.com/st-web-ui/static/active/en/st_prod_software_internet/resource/technical/software/firmware/stm32cubef3.zip"
        response = requests.get(URL)
        zipDocument = zipfile.ZipFile(response.content)
        

    logging.info("Application Terminated")
    sys.exit(0)
