# Alias-Effect
This project was realised as part of the "Engineering meets Arts" lecture at TU-Dortmund in 2020-2021.

To setup the app on RPi see the followong steps.
1. Make sure the audio device you want to use is installed.
2. Make sure the Pi has a connection to the internet.
3. Configure your input and output devices in the Pi's audio menue.
4. Download the install.sh to the Pis home folder.
     ```
    cd /home/pi
    git clone https://github.com/nilhoel1/EmA-Alias-Effect.git
    ```
5. Run the script and follow the instructions:
    ```
    cd EmA-Alias-Effect
    ./install.sh
    ```

6. The script will reboot and the App should auto start.
