# Alias-Effect
This project was realised as part of the "Engineering meets Arts" lecture at TU-Dortmund in 2020-2021.

To setup the app see the followong steps.
1. Install the dependencies for this app (Linux only):
    ```
    sudo apt-get install libportaudio2
    pip3 install sounddevice
    ```


2. Check for the sound device you want to use:
    ```
    python3 -m sounddevice
    ```
3. Change the `self.device` variable to the device Nr. you want to use.
4. Run the App
    ```
    python3 gui.py
    ```