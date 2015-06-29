# updating & upgrading
sudo apt-get update
sudo apt-get upgrade

# dependencies
sudo apt-get install libjpeg8-dev imagemagick libv4l-dev
sudo ln -s /usr/include/linux/videodev2.h /usr/include/linux/videodev.h

# mjpg-streamer
sudo apt-get install subversion
cd ~
svn co https://svn.code.sf.net/p/mjpg-streamer/code/mjpg-streamer/ mjpg-streamer
cd mjpg-streamer
make mjpg_streamer input_file.so input_uvc.so output_http.so
sudo cp mjpg_streamer /usr/local/bin
sudo cp output_http.so input_file.so input_uvc.so /usr/local/lib/
sudo cp -R www /usr/local/www


# create log dir
sudo mkdir /var/log/xm

# run using 
# echo "export LD_LIBRARY_PATH=/usr/local/lib/"
# mjpg_streamer -i "/usr/local/lib/input_uvc.so -d /dev/video0 -n -y -r 320x240 -f 5" -o "/usr/local/lib/output_http.so -p 8090 -w /usr/local/www"
