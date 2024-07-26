pyinstaller --onefile any2h264.py -y
sys_arch=$(arch)
mv dist/any2h264 dist/any2h264_$sys_arch
sudo cp dist/any2h264_$sys_arch /usr/bin/any2h264
sudo chmod +x /usr/bin/any2h264
