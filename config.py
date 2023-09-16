"""

Designed and Developed by-
Udayraj Deshmukh 
https://github.com/Udayraj123

"""

"""
Constants
"""
display_height = int(640)
display_width = int(640)
windowWidth = 1280
windowHeight = 720

saveMarked = 1
saveCropped = 1
showimglvl = 4
saveimglvl = 0
PRELIM_CHECKS = 0

explain = 0
# autorotate=1

BATCH_NO = 1000
NO_MARKER_ERR = 12
MULTI_BUBBLE_WARN = 15

# name of template file
TEMPLATE_FILE_180 = 'template_180.json'
TEMPLATE_FILE_150 = 'template_150.json'
TEMPLATE_FILE_50 = 'template_50.json'
TEMPLATE_FILE_75 = 'template_75.json'
TEMPLATE_FILE_10= 'template_10.json'
TEMPLATE_FILE_20= 'template_20.json'
TEMPLATE_FILE_20_QUIZ= 'template_20_quiz.json'
TEMPLATE_FILE_30= 'template_30.json'
TEMPLATE_FILE_40= 'template_40.json'
TEMPLATE_FILE_45 = 'template_45.json'
TEMPLATE_FILE_100 = 'template_100.json'
MARKER_FILE = "omr_marker.png"

# For preProcessing
GAMMA_LOW = 0.7
GAMMA_HIGH = 1.25

ERODE_SUB_OFF = 1

# For new ways of determining threshold
MIN_GAP, MIN_STD = 30, 25
MIN_JUMP = 15
# If only not confident, take help of globalTHR
CONFIDENT_JUMP = MIN_JUMP + 15
JUMP_DELTA = 30
# MIN_GAP : worst case gap of black and gray

# Templ alignment parameters
ALIGN_RANGE = range(-5, 6, 1)
# TODO ^THIS SHOULD BE IN LAYOUT FILE AS ITS RELATED TO DIMENSIONS
# ALIGN_RANGE  = [-6,-4,-2,-1,0,1,2,4,6]

# max threshold difference for template matching
thresholdVar = 0.41

# TODO: remove unnec variables here-
thresholdCircle = 0.3
marker_rescale_range = (35, 100)
marker_rescale_steps = 10

# Presentation variables
uniform_height = int(1231 / 1.5)
uniform_width = int(1000 / 1.5)
# Original dims are about (3527, 2494)

# Any input images should be resized to this--
uniform_width_hd = int(uniform_width * 1.5)
uniform_height_hd = int(uniform_height * 1.5)

TEXT_SIZE = 0.95
CLR_BLACK = (50, 150, 150)
CLR_WHITE = (250, 250, 250)
CLR_GRAY = (130, 130, 130)
# CLR_DARK_GRAY = (190,190,190)
CLR_DARK_GRAY = (100, 100, 100)

MIN_PAGE_AREA = 80000

# Filepaths
class Paths:
    def __init__(self, output):
        self.output = output
        self.saveMarkedDir = f'{output}/CheckedOMRs/'
        self.resultDir = f'{output}/Results/'

