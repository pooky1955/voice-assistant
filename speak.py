import os
import subprocess
import datetime
import shlex

def program_exists(program_name):
    try:
        subprocess.call(["pico2wave","--help"],stdout=subprocess.DEVNULL)
        return True
    except FileNotFoundError:
        return False

def run_command(command):
    subprocess.check_call(shlex.split(command),stdin=subprocess.DEVNULL, stdout=subprocess.DEVNULL)

def speak(text):
    now = datetime.datetime.now().strftime("%Y-%m-%d-%H-%M-%S")
    filename = f"output-{now}.wav" 
    run_command(f'pico2wave -w {filename} "{text}"')
    run_command(f"mpv {filename} --speed 1.1")
    os.remove(filename)


assert program_exists("pico2wave"), "The PICO's TTS program was not available on the PATH. Please make sure to install it and add it to the path."

