#!/usr/bin/env python
"""This module installs sample data for use in G-OnRamp"""

import argparse

from time import sleep
from os.path import isfile, join
from os import listdir, stat

from bioblend import galaxy

#-------------------------------------------------------------------
#   Argument enumeration and parsing
PARSER = argparse.ArgumentParser(description='Install G-OnRamp Library Data')
# required arguments
PARSER.add_argument('-a', type=str,
                    help="the address of the target host running Galaxy",
                    required=True)
PARSER.add_argument('-k', type=str,
                    help="your Galaxy instance API key", required=True)
PARSER.add_argument('-l', type=str,
                    help="the folder you wish to upload to your library from",
                    required=True)

ARGS = PARSER.parse_args()

GI = galaxy.GalaxyInstance(url=ARGS.a, key=ARGS.k)
LC = galaxy.libraries.LibraryClient(GI)

LIB_NAME = "Intro to G-OnRamp"

EXTANT_LIBS = LC.get_libraries(name=LIB_NAME)

INSTALL = True

if EXTANT_LIBS:
    for lib in EXTANT_LIBS:
        if lib["deleted"] == "False":
            INSTALL = False
            break

if INSTALL:
    LIB_DATA = LC.create_library("Intro to G-OnRamp",
                                 "Sample data sets for G-OnRamp's introductory walk-through")

    FILES = [join(ARGS.l, lf) for lf in listdir(ARGS.l) \
            if isfile(join(ARGS.l, lf))]

    for f in FILES:
        megabytes = stat(f).st_size / ( 1024 * 1024)
        mps = 2
        print("{0}:{1} @ {2} seconds".format(f,megabytes,megabytes/mps))
        LC.upload_file_from_local_path(LIB_DATA["id"], f)
        sleep( megabytes / mps )
