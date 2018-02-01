#!/bin/sh
python stereo.py
sync
mv matched.png /var/www/html/
blender --background --python blender.py
rm bridge_c bridge_z
sync
mogrify -trim rendered.png
sync
mv output.stl /var/www/html/
mv rendered.png /var/www/html/
sync

