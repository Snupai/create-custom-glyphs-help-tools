import time
import argparse
from ffmpeg import FFmpeg
import subprocess

args_parser = argparse.ArgumentParser(formatter_class=argparse.RawTextHelpFormatter, description="Takes a wav file and outputs a labels file that can be used with SebiAi's custom glyph lighting scripts alongside an ogg audio file.")
args_parser.add_argument("--labels", "-l", required=True, help="The label file to be processed. OR the midi file to be processed.")
args_parser.add_argument("--audio-file", "-a", required=True, help="The audio file to be processed.")
args_parser.add_argument("--compatibility-mode", "-c", action="store_true", help="Use this flag if you are using phone 1. Otherwise, leave it out.")
args_parser.add_argument("--output", "-o", help="The output file name. If not specified, the output will match the name of the input.")
#args_parser.add_argument("--visualize", "-v", action="store_true", help="Use this flag if you want to visualize the output. Otherwise, leave it out.")

args = args_parser.parse_args()

if args.FILE.split(".")[-1] != "ogg":
    old_file = args.FILE
    (
        FFmpeg()
            .input(args.FILE)
            .output(
                f'{".".join(args.FILE.split(".")[:-1])}.ogg',
                acodec='libopus'
            )
    ).execute()
    
if args.labels.split(".")[-1] == "mid":
    file_path = "MidiToLabel.py"
    parameters = [f'-f {args.labels}', f'-o {".".join(args.labels.split(".")[:-1])}.txt']
else:
    file_path = "GlyphTranslator.py"
    parameters = [f'{".".join(args.FILE.split(".")[:-1])}.txt']

subprocess.run(["python", file_path] + parameters)

time.sleep(2)

file_path = "GlyphModder.py"

parameters = [f'-t {(args.FILE.split(".")[:-1])}', f'-w', f'{".".join(args.FILE.split(".")[:-1])}.glypha', f'{".".join(args.FILE.split(".")[:-1])}.glyphc1', f'{".".join(args.FILE.split(".")[:-1])}.ogg']

subprocess.run(["python", file_path] + parameters)

import os
import shutil
from datetime import datetime

new_folder = f'{".".join(args.FILE.split(".")[:-1])}_{datetime.now().strftime("%m-%d-%Y_%H-%M-%S")}'
os.mkdir(new_folder)

end_product = f'{".".join(args.FILE.split(".")[:-1])}.ogg'
files = [f'{".".join(args.FILE.split(".")[:-1])}.txt', f'{".".join(args.FILE.split(".")[:-1])}.glypha', f'{".".join(args.FILE.split(".")[:-1])}.glyphc1', f'{args.FILE}']
if old_file != args.FILE:
    files.append(old_file)
for file in files:
    shutil.move(file, new_folder)
shutil.copy(end_product, new_folder)

shutil.make_archive(new_folder, 'zip', new_folder)

shutil.rmtree(new_folder)

os.mkdir(f'Glyphs/{new_folder}')
shutil.move(f'{new_folder}.zip', f'Glyphs/{new_folder}')
shutil.move(end_product, f'Glyphs/{new_folder}')

print(f'Your glyphs are ready! They are located in Glyphs/{new_folder}')

#def glyph_visualization():
#    print("to be implemented")
#    pass
#    #TODO: Wait for SebiAi to implement command line file parsing for GlyphVisualizer.exe
#    subprocess.run(["GlyphVisualizer.exe", '-f', f'{".".join(args.FILE.split(".")[:-1])}.ogg'])
#    pass

#if args.visualize:
#    print("Visualizing glyphs...")
#    glyph_visualization()
