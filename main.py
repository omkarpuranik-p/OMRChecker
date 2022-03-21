"""

Designed and Developed by-
Udayraj Deshmukh
https://github.com/Udayraj123

"""
import re
import os
import cv2
# import argparse
import numpy as np
import pandas as pd

import config
import utils
from template import Template

# Local globals
filesMoved=0
filesNotMoved=0

from glob import glob
from csv import QUOTE_NONNUMERIC
from time import time

def process_dir(root_dir, subdir, templateCode, test_img):
    curr_dir = os.path.join(root_dir, subdir)

    if int(templateCode, 10) == 150:
        fileUrl = config.TEMPLATE_FILE_150
    elif int(templateCode, 10) == 75:
        fileUrl = config.TEMPLATE_FILE_75
    elif int(templateCode, 10) == 50:
        fileUrl = config.TEMPLATE_FILE_50
    elif int(templateCode, 10) == 20:
        fileUrl = config.TEMPLATE_FILE_20
    else:
        fileUrl = config.TEMPLATE_FILE_180

    # Look for template in current dir
    template_file = os.path.join(curr_dir, fileUrl)
    template = Template(template_file)

    # look for images in current dir to process
    paths = config.Paths(os.path.join('outputs', subdir))
    exts = ('*.png', '*.jpg', '*.jpeg')
    omr_files = sorted(
        [f for ext in exts for f in glob(os.path.join(curr_dir, ext))])

    # Exclude marker image if exists
    if(template and template.marker_path):
        omr_files = [f for f in omr_files if f != template.marker_path]

    subfolders = sorted([file for file in os.listdir(
        curr_dir) if os.path.isdir(os.path.join(curr_dir, file))])
    if omr_files:
        utils.setup_dirs(paths)
#         output_set = setup_output(paths, template)
        temp_out = process_files(omr_files, template, test_img)
        return temp_out

    for folder in subfolders:
        var_temp = process_dir(root_dir, os.path.join(subdir, folder), templateCode, test_img)
        return var_temp


def checkAndMove(error_code, filepath, filepath2):
    # print("Dummy Move:  "+filepath, " --> ",filepath2)
    global filesNotMoved
    filesNotMoved += 1
    return True

    global filesMoved
    if(not os.path.exists(filepath)):
        print('File already moved')
        return False
    if(os.path.exists(filepath2)):
        print('ERROR : Duplicate file at ' + filepath2)
        return False

    print("Moved:  " + filepath, " --> ", filepath2)
    os.rename(filepath, filepath2)
    filesMoved += 1
    return True


def processOMR(template, omrResp):
    # Note: This is a reference function. It is not part of the OMR checker
    # So its implementation is completely subjective to user's requirements.
    csvResp = {}

    # symbol for absent response
    UNMARKED_SYMBOL = ' '

    # Multi-column/multi-row questions which need to be concatenated
    for qNo, respKeys in template.concats.items():
        csvResp[qNo] = ''.join([omrResp.get(k, UNMARKED_SYMBOL)
                                for k in respKeys]).strip()

    # Single-column/single-row questions
    for qNo in template.singles:
        csvResp[qNo] = omrResp.get(qNo, UNMARKED_SYMBOL)

    # Note: Concatenations and Singles together should be mutually exclusive
    # and should cover all questions in the template(exhaustive)
    # TODO: ^add a warning if omrResp has unused keys remaining
    return csvResp


def report(
        Status,
        streak,
        scheme,
        qNo,
        marked,
        ans,
        prevmarks,
        currmarks,
        marks):
    print(
        '%s \t %s \t\t %s \t %s \t %s \t %s \t %s ' % (qNo,
                                                       Status,
                                                       str(streak),
                                                       '[' + scheme + '] ',
                                                       (str(prevmarks) + ' + ' + str(currmarks) + ' =' + str(marks)),
                                                       str(marked),
                                                       str(ans)))

# check sectionwise only.


def process_files(omr_files, template, test_img):
    start_time = int(time())
    filesCounter = 0
    filesNotMoved = 0

    for filepath in omr_files:
        filesCounter += 1
        # For windows filesystem support: all '\' will be replaced by '/'
        filepath = filepath.replace(os.sep, '/')

        # Prefixing a 'r' to use raw string (escape character '\' is taken
        # literally)
        finder = re.search(r'.*/(.*)/(.*)', filepath, re.IGNORECASE)
        if(finder):
            inputFolderName, filename = finder.groups()
        else:
            print("Error: Filepath not matching to Regex: " + filepath)
            continue
        # set global var for reading

#         inOMR = cv2.imread(filepath, cv2.IMREAD_GRAYSCALE)

        inOMR = test_img
        print(
            '\n[%d] Processing image: \t' %
            (filesCounter),
            filepath,
            "\tResolution: ",
            inOMR)

        OMRCrop = utils.getROI(inOMR, filename, noCropping=True)

#         if(OMRCrop is None):
#             # Error OMR - could not crop
#             newfilepath = out.paths.errorsDir + filename
#             out.OUTPUT_SET.append([filename] + out.emptyResp)
#             if(checkAndMove(config.NO_MARKER_ERR, filepath, newfilepath)):
#                 err_line = [filename, filepath,
#                             newfilepath, "NA"] + out.emptyResp
#                 pd.DataFrame(
#                     err_line,
#                     dtype=str).T.to_csv(
#                     out.filesObj["Errors"],
#                     quoting=QUOTE_NONNUMERIC,
#                     header=False,
#                     index=False)
#             continue

        if template.marker is not None:
            OMRCrop = utils.handle_markers(OMRCrop, template.marker, filename)

        # if(args["setLayout"]):
            # templateLayout = utils.drawTemplateLayout(
            #     OMRCrop, template, shifted=False, border=2)
            # utils.show("Template Layout", templateLayout, 1, 1)
            # continue

        # uniquify
        file_id = inputFolderName + '_' + filename
        savedir = 'outputs'
        OMRresponseDict, final_marked, MultiMarked, multiroll = \
            utils.readResponse(template, OMRCrop, name=file_id,
                         savedir=savedir, autoAlign=True)

        # concatenate roll nos, set unmarked responses, etc
        # Required JSON
        resp = processOMR(template, OMRresponseDict)
        # print("\nRead Response: \t", resp)
        return resp

        newfilepath = savedir + file_id
        # # Enter into Results sheet-
        results_line = [filename, filepath, newfilepath, score] + respArray

