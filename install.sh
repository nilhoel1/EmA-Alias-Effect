#!/bin/sh

#installing dependencies
sudo apt install -y libportaudio2 libatlas-base-dev python3-qtpy
pip3 install sounddevice matplotlib
pip3 install -U numpy

#get Repository
git clone https://github.com/nilhoel1/EmA-Alias-Effect.git
cd EmA-Alias-Effect

#create autostart file
touch alias.desktop
echo "[Desktop Entry]" > alias.desktop
echo "Type=Application" >> alias.desktop
echo "Name=Alias" >> alias.desktop
echo "Exec=/home/pi/EmA-Alias-Effect/start.sh" >> alias.desktop

#ask for audio device
python3 -m sounddevice
echo "Pleas input the number of the AudioDevice you want to use:"
read input
echo input

#create start.sh
touch start.sh
echo "#!/bin/sh!" > start.sh
echo "cd /home/pi/EmA-Alias-Effect/" >> start.sh
echo python3 gui.py $input >> start.sh

#move file to autostart
mkdir /home/pi/.config/autostart
mv alias.desktop /home/pi/.config/autostart
