# voice-assistant
voice-assistant is an attempt at making my whole computer controllable by voice using Kaldi recognizer and Dragonfly.
The kaldi recognizer is from kaldi-active-grammar

This project uses sox play and pico2wave to produce speaker output.

Download them (if on Ubuntu-based flavours) by using:
```bash
sudo apt-get install libttspico0 libttspico-utils libttspico-data # this downloads the TTS pico2wave module
sudo apt-get install sox # this downloads sox and play
sudo apt-get install portaudio19-dev # this downloads the engine needed to get mic input
```

# Commands to get this running
1. Install Anaconda or Miniconda on your system using the following guide: https://docs.conda.io/en/latest/miniconda.html

2. In the shell, run 
```{sh}
./install.sh
``` 
for Linux and MacOS or
```{sh}
./install.bat
``` 
for Windows

Alternatively, you can run the following commands should the installation scripts above not work.
```bash
conda env create -n speech-env python==3.8.5
conda activate speech-env
conda install pip
pip install 'dragonfly2[kaldi]'
```

3. Download any speech to text model and extract them to a folder called kaldi_model from here: https://github.com/daanzu/kaldi-active-grammar/blob/master/docs/models.md

I used the first one: kaldi_model_daanzu_20211030-biglm

4. Run the main file: python web_assistant.py

NOTE: I am using the Vimium C in firefox, which allows me to have the voice assistant input keyboard commands to control my firefox tab.
Make sure to have installed Vimium C if you wish to continue.

Thank you and have fun!
