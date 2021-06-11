#!/bin/sh

#installing dependencies
sudo apt install -y libportaudio2 libatlas-base-dev python3-qtpy llvm-9
pip3 install sounddevice matplotlib
pip3 install -U numpy
LLVM_CONFIG=llvm-config-9 pip3 install llvmlite
pip3 install numba

#get Repository
cd /home/pi
git clone https://github.com/nilhoel1/EmA-Alias-Effect.git
cd EmA-Alias-Effect

#create autostart file
touch alias.desktop
echo "[Desktop Entry]" > alias.desktop
echo "Type=Application" >> alias.desktop
echo "Name=Alias" >> alias.desktop
echo "Exec=/bin/sh /home/pi/EmA-Alias-Effect/start.sh" >> alias.desktop

#ask for audio device
python3 -m sounddevice
echo "Pleas input the number of the Default AudioDevice of the System:"
read input

#create start.sh
touch start.sh
echo "#!/bin/sh" > start.sh
echo "cd /home/pi/EmA-Alias-Effect/" >> start.sh
echo python3 gui.py $input >> start.sh

#move file to autostart
mkdir /home/pi/.config/autostart
mv alias.desktop /home/pi/.config/autostart

#installing audio tweaks for debian
echo "Insalling sound tweaks for stability"
wget https://github.com/dynobot/Linux-Audio-Adjustments/raw/master/basic-install.sh
chmod 755 basic-install.sh
sudo ./basic-install.sh
