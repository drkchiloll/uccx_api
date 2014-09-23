UCCX_API
=========

Cisco Unified Contact Center
Express Configuration API

###############################################################
ResourceGroup Configuration: rsrcgrp_v01.py, rsrc_grp.csv

Used to Add, Modify, and Delete (permenantly) ResourceGroups
using the Express Configuration API in Bulk using a Comma
Separated Value file.

Run from the Command Line Interface using the following syntax:

Computer:ResourceGroups samwomack$ python rsrcgrp_v01.py -h
Usage: rsrcgrp_v01.py [options]

Options:
  -h, --help     show this help message and exit
  -f INPUT_FILE  CSV Path + FileName

There are no current limitations to this that I can tell at
this point.

CSV Header:
RG_NAME, Add, Modify, Delete, NEW_NAME
###############################################################

