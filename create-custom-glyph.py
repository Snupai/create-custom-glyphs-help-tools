import time
import argparse
from ffmpeg import FFmpeg
import subprocess
import shutil

args_parser = argparse.ArgumentParser(formatter_class=argparse.RawTextHelpFormatter, description="Takes a wav file and outputs a labels file that can be used with SebiAi's custom glyph lighting scripts alongside an ogg audio file.")
args_parser.add_argument("--labels-file", "-l", required=True, help="The label file to be processed. OR the midi file to be processed.")
args_parser.add_argument("--watermark-file", "-w", default=None, help="The watermark file to be processed.")
args_parser.add_argument("--audio-file", "-a", required=True, help="The audio file to be processed.")
args_parser.add_argument("--compatibility-mode", "-c", action="store_true", help="Use this flag if you are using phone 1. Otherwise, leave it out.")
args_parser.add_argument("--title", "-t", default=None, help="Set the title of the glyph. If not specified, the title will be the name of the input audio file.")
# args_parser.add_argument("--visualize", "-v", action="store_true", help="Use this flag if you want to visualize the output. Otherwise, leave it out.")

args = args_parser.parse_args()

def contains(string: str, character):
    if string == None:
        return False
    for char in string:
        if char == character:
            return True
    return False

if contains(args.audio_file, '/'):
    old_file_path = args.audio_file
    args.audio_file = args.audio_file.split("/")[-1]
    shutil.copy(old_file_path, args.audio_file)

if contains(args.labels_file, '/'):
    old_file_path = args.labels_file
    args.labels_file = args.labels_file.split("/")[-1]
    shutil.copy(old_file_path, args.labels_file)

if contains(args.watermark_file, '/'):
    old_file_path = args.watermark_file
    args.watermark_file = args.watermark_file.split("/")[-1]
    shutil.copy(old_file_path, args.watermark_file)
    
if contains(args.audio_file, '\\'):
    old_file_path = args.audio_file
    args.audio_file = args.audio_file.split("\\")[-1]
    shutil.copy(old_file_path, args.audio_file)

if contains(args.labels_file, '\\'):
    old_file_path = args.labels_file
    args.labels_file = args.labels_file.split("\\")[-1]
    shutil.copy(old_file_path, args.labels_file)

if contains(args.labels_file, '\\'):
    old_file_path = args.watermark_file
    args.watermark_file = args.watermark_file.split("\\")[-1]
    shutil.copy(old_file_path, args.watermark_file)

old_file = args.audio_file

if args.audio_file.split(".")[-1] != "ogg":
    (
        FFmpeg()
            .input(args.audio_file)
            .output(
                f'{".".join(args.audio_file.split(".")[:-1])}.ogg',
                acodec='libopus'
            )
    ).execute()
    args.audio_file = f'{".".join(args.audio_file.split(".")[:-1])}.ogg'
    
parameters = [f'{args.labels_file}']
if args.labels_file.split(".")[-1] == "mid":
    file_path = "MidiToLabel.py"
else:
    file_path = "GlyphTranslator.py"
    if args.watermark_file != None:
        parameters = ['--watermark', f'{args.watermark_file}', f'{args.labels_file}']

subprocess.run(["python", file_path] + parameters)

time.sleep(2)

file_path = "GlyphModder.py"
if args.title != None:
    args.title = args.audio_file.split(".")[:-1]
parameters = ['-t', f'{args.title}', '-w', f'{".".join(args.labels_file.split(".")[:-1])}.glypha', f'{".".join(args.labels_file.split(".")[:-1])}.glyphc1', f'{args.audio_file}']

subprocess.run(["python", file_path] + parameters)

import os
import shutil
from datetime import datetime

new_folder = f'{".".join(args.audio_file.split(".")[:-1])}_{datetime.now().strftime("%m-%d-%Y_%H-%M-%S")}'
os.mkdir(new_folder)

end_product = args.audio_file
files = [f'{args.labels_file}', f'{".".join(args.labels_file.split(".")[:-1])}.glypha', f'{".".join(args.labels_file.split(".")[:-1])}.glyphc1']
if args.watermark_file != None:
    files.append(args.watermark_file)
if old_file != args.audio_file:
    files.append(old_file)
for file in files:
    shutil.move(file, new_folder)
shutil.copy(end_product, new_folder)

shutil.make_archive(new_folder, 'zip', new_folder)

shutil.rmtree(new_folder)

if not os.path.exists('Glyphs'):
    os.mkdir('Glyphs')

os.mkdir(f'Glyphs/{new_folder}')
shutil.move(f'{new_folder}.zip', f'Glyphs/{new_folder}')
shutil.move(end_product, f'Glyphs/{new_folder}')

print(f'Your glyphs are ready! They are located in Glyphs/{new_folder}')
