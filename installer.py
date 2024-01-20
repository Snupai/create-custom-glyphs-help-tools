import ctypes
import hashlib
import os
import sys
import subprocess
import platform

OWN_GITHUB_URL = 'https://github.com/Snupai/create-custom-glyphs-help-tools'
Custom_Glyph_tools_GITHUB_URL = 'https://github.com/SebiAi/custom-nothing-glyph-tools'
WINGET_BASE_URL = 'https://github.com/microsoft/winget-cli/releases/latest/download/'
WINGET_PACKAGE = 'Microsoft.DesktopAppInstaller_8wekyb3d8bbwe.msixbundle'
WINGET_HASH = 'Microsoft.DesktopAppInstaller_8wekyb3d8bbwe.txt'
MICROSOFT_VCLIBS_URL = 'https://aka.ms/Microsoft.VCLibs.x64.14.00.Desktop.appx'
MICROSOFT_UI_XAML_URL = 'https://github.com/microsoft/microsoft-ui-xaml/releases/download/v2.8.5/Microsoft.UI.Xaml.2.8.x64.appx'
REFRENV_URL = 'https://raw.githubusercontent.com/badrelmers/RefrEnv/main/refrenv.bat'

def printInfo():
    print('This script will install all required packages for the custom glyph tools to work')
    print('This script will also install the custom glyph tools')
    print('\nYou\'ll need a working internet connection for this script to work')
    print('\nThis script will install the following packages:')
    print(' - ffmpeg')
    print(' - python')
    print(' - pip packages')
    print(' - custom glyph tools')
    print('\nThis script will also create the following folders:')
    print(' - custom_glyph_tools')
    print(' - custom_glyph_tools\\venv')
    print('Optionally this script will install Audacity.')


def LinuxInstallation(): 
    print('Error: To be implemented')
    sys.exit(1)

def MacOSInstallation():
    print('Error: MacOS is not supported')
    sys.exit(1)



def WindowsInstallation():
    subprocess.run(['curl', '-L', REFRENV_URL, '-o', 'refrenv.bat'])

    def removeShit(exitCode = 1):
        print('Removing temporary files')
        try:
            os.remove('refrenv.bat')
            os.remove('requirements.txt')
        except:
            pass
        sys.exit(exitCode)

    def refreshEnv():
        print('Refreshing environment variables')
        subprocess.run(['refrenv.bat'])

    def wingetInstall():
        try:
            print('Downloading winget')
            subprocess.run(['curl', '-L', WINGET_BASE_URL + WINGET_PACKAGE, '-o', WINGET_PACKAGE])
            subprocess.run(['curl', '-L', WINGET_BASE_URL + WINGET_HASH, '-o', WINGET_HASH])
            # get hash from file and compare with hash in the text file
            with open(WINGET_HASH, 'r') as f:
                winget_hash = f.read().split(' ')[0]
            if winget_hash != hashlib.sha256(open(WINGET_PACKAGE, 'rb').read()).hexdigest():
                print('Error: Hashes don\'t match')
                sys.exit(1)
            # download and install vclibs and microsoft ui xaml
            print('Downloading vclibs')
            subprocess.run(['curl', '-L', MICROSOFT_VCLIBS_URL, '-o', 'Microsoft.VCLibs.x64.14.00.Desktop.appx'])
            print('Downloading microsoft ui xaml')
            subprocess.run(['curl', '-L', MICROSOFT_UI_XAML_URL, '-o', 'Microsoft.UI.Xaml.2.8.x64.appx'])
            print('Installing winget')
            subprocess.run(['Add-AppxPackage', '-Path', WINGET_PACKAGE, '-DependencyPath', '"Microsoft.VCLibs.x64.14.00.Desktop.appx, Microsoft.UI.Xaml.2.8.x64.appx"'])
            print('Removing temporary files')
            os.remove(WINGET_PACKAGE)
            os.remove(WINGET_HASH)
            os.remove('Microsoft.VCLibs.x64.14.00.Desktop.appx')
            os.remove('Microsoft.UI.Xaml.2.8.x64.appx')
        except:
            print('Error: winget installation failed')
            print('Please install winget manually')
            os.system('start ms-windows-store://pdp/?ProductId=9nblggh4nns1')
            print('Press any key to continue')
            input()
            try:
                refreshEnv()
                subprocess.run(['winget', '--version'])
            except:
                print('Error: winget installation failed')
                sys.exit(1)
            print('Manual winget installation successful')

    print('Checking if Windows build is 16299 or higher')
    win_build = platform.win32_ver()[1].split('.')[len(platform.win32_ver()[1].split('.')) - 1]
    print('Windows build number: ' + win_build)
    if int(win_build) < 16299:
        print('Error: Windows build 16299 or higher is required')
        removeShit()

    print('Checking if script is running as administrator')
    if not ctypes.windll.shell32.IsUserAnAdmin():
        print('Error: Run as administrator')
        removeShit()
    print('Running as administrator')

    print('Checking if winget is installed')
    try:
        subprocess.run(['winget', '--version'])
        print('winget installation found')
    except:
        print('Error: winget is not installed')
        print('Do you want to install winget? (Y/n)')
        if input().lower() == '' or input().lower() == 'y':
            wingetInstall()
        else:
            print('Error: winget is required')
            removeShit()

    print('Checking if Audacity is installed')
    if not os.path.isfile('C:\\Program Files\\Audacity\\audacity.exe'):
        print('No Audacity installation found in "C:\\Program Files\\".')
        print('Do you want to install Audacity? (Y/n)')
        # if input is y or empty install audacity
        if input().lower() == '' or input().lower() == 'y':
            subprocess.run(['winget', 'install', 'Audacity'])
        else:
            print('Error: Audacity is required')
            removeShit()
    print('Audacity installation found')

    print('Checking if ffmpeg is installed')
    try:
        subprocess.run(['ffmpeg', '-version'])
    except:
        print('No ffmpeg installation found.')
        print('Do you want to install ffmpeg? (Y/n)')
        if input().lower() == '' or input().lower() == 'y':
            subprocess.run(['winget', 'install', 'Gyan.FFmpeg'])
        else:
            print('Error: ffmpeg is required')
            removeShit()
    print('ffmpeg installation found')

    print('Checking if python is installed')
    try:
        subprocess.run(['python', '--version'])
    except:
        print('No python installation found.')
        print('Do you want to install python? (Y/n)')
        if input().lower() == '' or input().lower() == 'y':
            subprocess.run(['winget', 'install', 'Python.Python.3.11'])
        else:
            print('Error: python is required')
            removeShit()
    print('python installation found')

    refreshEnv()

    print('Checking if pip is installed')
    try:
        subprocess.run(['pip', '--version'])
    except:
        print('No pip found.')
        if os.path.isfile('python.exe'):
            print('Do you want to install pip? (Y/n)')
            if input().lower() == '' or input().lower() == 'y':
                subprocess.run(['python', '-m', 'ensurepip'])
            else:
                print('Error: pip is required')
                removeShit()
        else:
            print('Error: python has not been installed properly')
            removeShit()
    print('pip installation found')

    # create a folder for the custom glyph tools
    if not os.path.isdir('custom_glyph_tools'):
        os.mkdir('custom_glyph_tools')
    # run command python -m venv custom_glyph_tools\venv
    print('Creating virtual environment')
    subprocess.run(['python', '-m', 'venv', 'custom_glyph_tools\\venv'])

    print('Downloading requirements.txt')
    subprocess.run(['curl', '-L', Custom_Glyph_tools_GITHUB_URL + '/raw/main/requirements.txt', '-o', 'requirements.txt'])
    print('Checking if pip packages are installed')
    subprocess.run(['custom_glyph_tools\\venv\\Scripts\\pip.exe', 'install', '-r', 'requirements.txt'])
    subprocess.run(['custom_glyph_tools\\venv\\Scripts\\pip.exe', 'install', 'python-ffmpeg'])

    # download custom glyph tools
    print('Downloading custom glyph tools')
    subprocess.run(['curl', '-L', Custom_Glyph_tools_GITHUB_URL + '/raw/main/GlyphModder.py', '-o', 'custom_glyph_tools\\GlyphModder.py'])
    subprocess.run(['curl', '-L', Custom_Glyph_tools_GITHUB_URL + '/raw/main/GlyphTranslator.py', '-o', 'custom_glyph_tools\\GlyphTranslator.py'])
    subprocess.run(['curl', '-L', Custom_Glyph_tools_GITHUB_URL + '/raw/main/MidiToLabel.py', '-o', 'custom_glyph_tools\\MidiToLabel.py'])
    subprocess.run(['curl', '-L', OWN_GITHUB_URL + '/raw/main/create-custom-glyph.py', '-o', 'custom_glyph_tools\\create-custom-glyph.py'])

    # create a file to spawn new shell with virtual environment
    print('Creating run.bat')
    run_bat = '@echo off\necho Usage:  \'python GlyphTranslator.py MyLabelFile.txt\'\necho\t\t\'python GlyphModder.py -t MyCustomTitle -w MyLabelFile.glypha MyLabelFile.glyphc1 MyGlyphCreation.ogg\'\necho\t\t\'python MidiToLabel.py MyMidiFile.mid\'\nAlternatively you can use the script create-custom-glyph\necho\t\t\'python create-custom-glyph.py -l MyLabelsFile.txt -a MyAudioFile.ogg\'\necho\t\t\'pyhton create-custom-glyph.py -l MyLabelsFile.mid -a MyAudioFile.ogg\'\necho Info: Audio file should not be required to be .ogg, will be converted automatically.\necho.\necho IMPORTANT: You need to put "" around the arguments if your file names have spaces. e.g. "My Label File.txt"\ncall .\\venv\\Scripts\\activate.bat\ncmd /k\n@echo on'
    # create file and write to it
    with open('custom_glyph_tools\\run.bat', 'w') as f:
        f.write(run_bat)

    print('\nInstallation successful\n')
    print('To start using the custom glyph tools, just run "run.bat" in the "custom_glyph_tools" folder by double clicking it.')
    print('Press any key to continue')
    input()
    removeShit(0)






match os.name:
    case 'nt':
        print('Windows detected')
        printInfo()
        WindowsInstallation()
    case 'posix':
        print('Linux detected')
        printInfo()
        LinuxInstallation()
    case 'darwin':
        print('MacOS detected')
        printInfo()
        MacOSInstallation()
    case default:
        print('Error: Unsupported operating system')
        sys.exit(1)
