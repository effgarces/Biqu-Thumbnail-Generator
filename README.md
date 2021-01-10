This script is not my work, It was shared over ath https://github.com/bigtreetech/BIGTREETECH-TouchScreenFirmware/issues/1238, please read the issue for all relevant information.

The version shared here is my modified version that adds "_btt" to the gcode file name and preserves the original file extension, instead of enforcing a .gcode file extension.

How to use:
Download and install python 3 (3.9.1 at this moment in time), afterwards, install PyQt5, by going to the command line and issuing `pip install PyQt5`

Next open prusa slicer and add the thumbail generation:
![Captura de ecrã 2021-01-01 124431](https://user-images.githubusercontent.com/1185683/103439342-fad15d00-4c33-11eb-97ca-65bbb512ba31.png)
 

Finaly go to your Print Settings and in Post processing scripts, add the following [python absolute path] [space] [script absolute path] and if any of the paths contain spaces enclose them in "":
![Captura de ecrã 2021-01-01 131206](https://user-images.githubusercontent.com/1185683/103439357-176d9500-4c34-11eb-86e9-630646848e63.png)

Then when saving the gcode, it will be processed by the script that will replace it with a version with the correct thumbnails for our TFT

A compiled exe version, using auto-py-to-exe, is also available in the releases.
