# -*- coding: utf-8 -*-

import os
from pyCGM2.Tools import btkTools


if __name__ == "__main__":

    c3dFilename = ""
    DATA_PATH = os.getcwd() + "//"

    btkAcq = btkTools.smartReader(DATA_PATH+c3dFilename)
    btkAcqUn = btkTools.changeSubjectName(btkAcq,subjectName)
    btkTools.smartWriter(btkAcqUn, DATA_PATH+c3dFilename[:-4]+"-Anonymised.c3d")
