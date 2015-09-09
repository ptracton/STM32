#! /usr/bin/env python3
"""
cube_install.py

This application is designed to download and explode a zip file from ST for either the
STM32F3 or F4 ICs.  It will then update the environment.mk file so the build tools can find
the needed files.

"""
import sys
import os
import argparse
import logging
import zipfile
import re

try:
    import requests
except:
    print ("You are missing the requests library, please install it")
    print ("pip install requests")
    sys.exit(-1)

try:
    import wget
except:
    print ("You are missing wget library, please install it")
    print ("pip install wget")
    sys.exit(-1)

def download_and_explode(URL, filename, location):
    """
    Download the URL, store in filename and explode into location
    """
    logging.info (URL)
    logging.info (filename)
    logging.info (location)
    
    if not os.path.exists(filename):
        filename = wget.download(url=URL, out=filename)
        print (filename)
        
    try:
        print("Opening %s" % filename)
        zip_file = zipfile.ZipFile(filename, 'r')
    except:
        print ("error opening zip file")
        logging.error("error opening zip file")
        sys.exit(-1)

    try:
        zip_file.testzip()
    except:
        print ("Failed zip file testing")
        logging.error("Failed zip file testing")
        sys.exit(-1)

    try:
        print ("Unzip to %s" % location)
        zip_file.extractall(path=location)
    except:
        print ("Zip Extraction failed")
        logging.error("Zip Extraction failed")
        sys.exit(-1)

    os.remove(filename)
        
    return

def update_environment(env, cpu, location):
    """
    We need to update the path in environment.mk to point to the
    location of the zip file we just exploded.  
    """
    starting_dir = os.getcwd()
    while ".git" in os.listdir():
        os.chdir("..")
    list_dir = os.listdir()
    
    list_dir = [x for x in list_dir if re.search("STM32Cube" ,x)]
    for x in list_dir:
        y = x.split("_")
        if y[2] == cpu:
            cube_dir =x
            
    print (list_dir)
    print (cube_dir)
    
    os.chdir(starting_dir)
    while ".git" not in os.listdir():
        os.chdir("..")

    try:
        makefile = open('environment.mk')
        lines = makefile.readlines()
        makefile.close()
    except:
        print ("Failed to open and read environment.mk")
        logging.error("Failed to open and read environment.mk")
        sys.exit(-1)

    update = False
    file_out = open ("environment.mk", 'w')
    for line in lines:
        match = re.search(env, line)
        if match:
            update = True
            line_list = line.split('=')
            line_list[1] = location+'/'+cube_dir+'/\n'
            new_line = "=".join(line_list)
            line = '#'+line
            print (new_line)
            file_out.write(new_line)
        file_out.write(line)
        
    if update is False:
        line = "STM32"+cpu+"_CUBE_ROOT_DIR="+location+'/'+cube_dir+'/\n'
        file_out.write(line)
    file_out.close()
    
    return
    
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
    parser.add_argument("--location",
                        help="Where to install the zip files",
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

    starting_dir = os.getcwd()
    if args.location:
        location = args.location
    else:            
        while ".git" not in os.listdir():
            os.chdir("..")
            
        os.chdir("..")
        location = os.getcwd()

    os.chdir(starting_dir)
    if args.cube3:
        print ("Downloading and Installing Stm32F3 Cube")
        logging.info("Downloading and Installing Stm32F3 Cube")
        
        URL = "http://www.st.com/st-web-ui/static/active/en/st_prod_software_internet/resource/technical/software/firmware/stm32cubef3.zip"
        filename = "/tmp/stm32f3cube.zip"
        download_and_explode(URL, filename, location)
        update_environment("STM32F3_CUBE_ROOT_DIR", "F3", location)
        
    if args.cube4:
        print ("Downloading and Installing Stm32F4 Cube")
        logging.info("Downloading and Installing Stm32F4 Cube")
        
        URL = "http://www.st.com/st-web-ui/static/active/en/st_prod_software_internet/resource/technical/software/firmware/stm32cubef4.zip"
        filename = "/tmp/stm32f4cube.zip"
        download_and_explode(URL, filename, location)
        update_environment("STM32F4_CUBE_ROOT_DIR", "F4", location)
        

    logging.info("Application Terminated")
    sys.exit(0)
