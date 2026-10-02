#
# Diagnostic Data Products README File for Large Helical Device (LHD) Fusion Plasma Experiment 
#
# 6 November 2023		First version
# 25 March 2024		Revised with additional information
#
# Task Group of Data Analysis Equipment (DAE) / Academic Research Platform LHD /
#   National Institute for Fusion Science (NIFS), Japan
# 
# -----------------------------------------------------------------------------

Physics diagnostics data acquired from Large Helical Device (LHD) experiments 
are available here at LHD's Fusion Diagnostic Data Repository by NIFS. 
The front page of Open Data Registry on AWS exists at "https://registry.opendata.aws/nifs-lhd/". 
Any users can search and retrieve the data objects complying with the 
"rights and terms of use for data" (https://www-lhd.nifs.ac.jp/pub/RightsTerms.html).

In this open data repository (https://nifs-lhd.s3.ap-northeast-1.amazonaws.com/index.html), 
there are two types of archived data format, i.e. ".dat" and ".zip".

# ----------------------------------------------------------------------------- 
The first generation has the filename structure as

  Diagnostic_name + shot_number + '-' + sub-shot_number + '.dat'

where each shot_number is a 6-digit and each sub-shot_numer is a 3-digit integer
padded with leading '0's, like "Bolometer007012-001.dat". 
These "dat" archives can be dissolved by this python3 script 
(https://w3.lhd.nifs.ac.jp/Experiment/LabcomDataDat.py) 
that users can download and use on the local computers.

# ----------------------------------------------------------------------------- 
The second generation archived files adopts the standard ZIP archive,
whose filename is given as

  Diagnostic_name + '-' + shot_number + '-' + sub-shot_number + '.zip'

like "Bolometer-90912-1.zip". There is no leading '0' in both shot_number and
sub-shot_number, and they could be longer than 6 and 3 digits, respectively.
Those "zip" files can be unzipped by using any "Unzip" utility.

# ----------------------------------------------------------------------------- 
For any inquiries concerning data access, please contact the DAE Task Group at "Comp_DAE@nifs.ac.jp".
