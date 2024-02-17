import ctypes
import hashlib
import os
import sys
import subprocess
import platform
import time
from termcolor import cprint
from colorama import just_fix_windows_console

OWN_GITHUB_URL = 'https://github.com/Snupai/create-custom-glyphs-help-tools'
SebiAi_Tutorial_URL = 'https://www.youtube.com/watch?v=YlJBqQxSgWA'
Custom_Glyph_tools_GITHUB_URL = 'https://github.com/SebiAi/custom-nothing-glyph-tools'
WINGET_BASE_URL = 'https://github.com/microsoft/winget-cli/releases/latest/download/'
WINGET_PACKAGE = 'Microsoft.DesktopAppInstaller_8wekyb3d8bbwe.msixbundle'
WINGET_HASH = 'Microsoft.DesktopAppInstaller_8wekyb3d8bbwe.txt'
MICROSOFT_VCLIBS_URL = 'https://aka.ms/Microsoft.VCLibs.x64.14.00.Desktop.appx'
MICROSOFT_UI_XAML_URL = 'https://github.com/microsoft/microsoft-ui-xaml/releases/download/v2.8.5/Microsoft.UI.Xaml.2.8.x64.appx'
REFRENV_URL = 'https://raw.githubusercontent.com/badrelmers/RefrEnv/main/refrenv.bat'

def printInfoText():
    print('This script will install all required packages for the custom glyph tools to work')
    print('This script will also install the custom glyph tools itself')
    print('\nYou\'ll need a working internet connection for this script to work')
    print('\nThis script will install the following packages:')
    print(' - ffmpeg')
    print(' - python')
    print(' - pip packages')
    print(' - custom glyph tools')
    print(' - create-custom-glyph.py')
    print('\nThis script will also create the following folders:')
    print(' - custom_glyph_tools')
    print(' - custom_glyph_tools\\venv')
    print('\nOptionally this script will install Audacity.')
    print('\nDo you want to continue? (Y/n)')
    if input().lower() == '' or input().lower() == 'y':
        pass
    else:
        printInfo("Installation aborted")
        sys.exit(0)

def checkIfSubString(string: str, subString: str):
    if subString in string:
        return True
    return False

def LinuxInstallation():
    printError("To be implemented")
    sys.exit(1)

def MacOSInstallation():
    printError("MacOS is not supported")
    sys.exit(1)



def WindowsInstallation():
    printInfoText()
    subprocess.run(['curl', '-L', REFRENV_URL, '-o', 'refrenv.bat'])

    def removeShit(exitCode = 1):
        printInfo("Removing temporary files")
        try:
            os.remove('refrenv.bat')
            os.remove('requirements.txt')
        except:
            pass
        printInfo("Press any key to continue")
        input()
        sys.exit(exitCode)

    def refreshEnv():
        printInfo("Refreshing environment variables")
        subprocess.run(['refrenv.bat'])

    def wingetInstall():
        try:
            printInfo("Downloading winget")
            subprocess.run(['curl', '-L', WINGET_BASE_URL + WINGET_PACKAGE, '-o', WINGET_PACKAGE])
            subprocess.run(['curl', '-L', WINGET_BASE_URL + WINGET_HASH, '-o', WINGET_HASH])
            # get hash from file and compare with hash in the text file
            with open(WINGET_HASH, 'r') as f:
                winget_hash = f.read().split(' ')[0]
            if winget_hash != hashlib.sha256(open(WINGET_PACKAGE, 'rb').read()).hexdigest():
                printError("Hashes don't match")
                sys.exit(1)
            # download and install vclibs and microsoft ui xaml
            printInfo("Downloading vclibs")
            subprocess.run(['curl', '-L', MICROSOFT_VCLIBS_URL, '-o', 'Microsoft.VCLibs.x64.14.00.Desktop.appx'])
            printInfo("Downloading microsoft ui xaml")
            subprocess.run(['curl', '-L', MICROSOFT_UI_XAML_URL, '-o', 'Microsoft.UI.Xaml.2.8.x64.appx'])
            printInfo("Installing winget")
            # TODO: this is not working didn't install winget and failed silently
            subprocess.run(['powershell', 'Add-AppxPackage', '-Path', WINGET_PACKAGE, '-DependencyPath', '"Microsoft.VCLibs.x64.14.00.Desktop.appx, Microsoft.UI.Xaml.2.8.x64.appx"'])
            os.remove(WINGET_PACKAGE)
            os.remove(WINGET_HASH)
            os.remove('Microsoft.VCLibs.x64.14.00.Desktop.appx')
            os.remove('Microsoft.UI.Xaml.2.8.x64.appx')
        except:
            printError("winget installation failed")
            printInfo("Please install winget manually")
            os.system('start ms-windows-store://pdp/?ProductId=9nblggh4nns1')
            printInfo("Press any key to continue")
            input()
            try:
                refreshEnv()
                subprocess.run(['winget', '--version'])
            except:
                printError("Error: winget installation failed")
                removeShit()
            printInfo("Manual winget installation successful")

    printInfo("Checking if Windows build is 16299 or higher")
    win_build = platform.win32_ver()[1].split('.')[len(platform.win32_ver()[1].split('.')) - 1]
    printInfo("Windows build number: " + win_build)
    if int(win_build) < 16299:
        printError("Windows build 16299 or higher is required")
        removeShit()

    printInfo("Checking if script is running as administrator")
    if not ctypes.windll.shell32.IsUserAnAdmin():
        printError("Run as administrator")
        removeShit()
    printInfo("Running as administrator")

    printInfo("Checking if winget is installed")
    try:
        subprocess.run(['winget', '--version'])
        printInfo("winget installation found")
    except:
        printError("winget is not installed")
        printInfo("Do you want to install winget? (Y/n)")
        if input().lower() == '' or input().lower() == 'y':
            wingetInstall()
        else:
            printCriticalError("winget is required")
            removeShit()
    else:
        printInfo("trying to update the sources")
        try:
            response = subprocess.run(['winget', 'source', 'update'], capture_output=True).stdout.decode('utf-8')
            if checkIfSubString('Cancelled', response):
                raise Exception("winget source update failed")
        except:
            printCriticalError("winget source can't be updated")
            printInfo("Do you want to try manually update winget? (Y/n)")
            if input().lower() == '' or input().lower() == 'y':
                wingetInstall()

    printInfo("Checking if Audacity is installed")
    if not os.path.isfile('C:\\Program Files\\Audacity\\audacity.exe'):
        printWarning("No Audacity installation found in \"C:\\Program Files\\\".")
        printInfo("Do you want to install Audacity? (Y/n)")
        if input().lower() == '' or input().lower() == 'y':
            try:
                subprocess.run(['winget', 'install', 'Audacity.Audacity'])
            except:
                printError("Audacity installation failed")
                printInfo("Please install Audacity manually")
                printInfo("Press any key to continue")
                input()
        else:
            printWarning("Audacity is recommended but not required")
            printInfo("continuing installation")
            time.sleep(2)
    else:
        printInfo("Audacity installation found")

    printInfo("Checking if ffmpeg is installed")
    try:
        subprocess.run(['ffmpeg', '-version'])
    except:
        printWarning("No ffmpeg installation found.")
        printInfo("Do you want to install ffmpeg? (Y/n)")
        if input().lower() == '' or input().lower() == 'y':
            subprocess.run(['winget', 'install', 'Gyan.FFmpeg'])
        else:
            printError("ffmpeg is required")
            removeShit()
    printInfo("ffmpeg installation found")

    printInfo("Checking if python is installed")
    try:
        response = subprocess.run(['python', '--version'], capture_output=True).stdout.decode('utf-8')
        if checkIfSubString('Python was not found', response):
            raise Exception("Python was not found")
    except:
        printWarning("No python installation found.")
        printInfo("Do you want to install python? (Y/n)")
        if input().lower() == '' or input().lower() == 'y':
            try:
                subprocess.run(['winget', 'install', 'Python.Python.3.12'])
            except:
                printError("python installation failed")
                printInfo("Please install python manually")
                printInfo("Press any key to continue")
                input()
        else:
            printError("python is required")
            removeShit()
    printInfo("python installation found")

    refreshEnv()

    printInfo("Checking if pip is installed")
    try:
        # make new cmd instance with refrenv to refresh the environment variables and then run pip in that instance
        # subprocess.run(['refrenv.bat', 'cmd', '/c', 'pip', '--version'])
        #TODO: this is not working even with refrenv maybe relaunch the script with parameter --skip-to-pip
        subprocess.run(['pip', '--version'])
    except:
        printError("No pip found.")
        if os.path.isfile('python.exe'):
            printInfo("Do you want to install pip? (Y/n)")
            if input().lower() == '' or input().lower() == 'y':
                subprocess.run(['python', '-m', 'pip', '--version'])
            else:
                printError("pip is required")
                removeShit()
        else:
            printError("python has not been installed properly")
            removeShit()
    printInfo("pip installation found")

    printInfo("Creating custom_glyph_tools folder")
    if not os.path.isdir('custom_glyph_tools'):
        os.mkdir('custom_glyph_tools')

    printInfo("Creating virtual environment")
    subprocess.run(['python', '-m', 'venv', 'custom_glyph_tools\\venv'])

    printInfo("Downloading requirements.txt")
    subprocess.run(['curl', '-L', Custom_Glyph_tools_GITHUB_URL + '/raw/main/requirements.txt', '-o', 'requirements.txt'])
    printInfo("Checking if pip packages are installed")
    subprocess.run(['custom_glyph_tools\\venv\\Scripts\\pip.exe', 'install', '-r', 'requirements.txt'])
    subprocess.run(['custom_glyph_tools\\venv\\Scripts\\pip.exe', 'install', 'python-ffmpeg'])

    printInfo("Downloading custom glyph tools")
    subprocess.run(['curl', '-L', Custom_Glyph_tools_GITHUB_URL + '/raw/main/GlyphModder.py', '-o', 'custom_glyph_tools\\GlyphModder.py'])
    subprocess.run(['curl', '-L', Custom_Glyph_tools_GITHUB_URL + '/raw/main/GlyphTranslator.py', '-o', 'custom_glyph_tools\\GlyphTranslator.py'])
    subprocess.run(['curl', '-L', Custom_Glyph_tools_GITHUB_URL + '/raw/main/MidiToLabel.py', '-o', 'custom_glyph_tools\\MidiToLabel.py'])
    subprocess.run(['curl', '-L', OWN_GITHUB_URL + '/raw/master/create-custom-glyph.py', '-o', 'custom_glyph_tools\\create-custom-glyph.py'])

    printInfo("Creating start.bat")
    start_bat = '@echo off\necho Usage:  \'python GlyphTranslator.py MyLabelFile.txt\'\necho\t\t\'python GlyphModder.py -t MyCustomTitle -w MyLabelFile.glypha MyLabelFile.glyphc1 MyGlyphCreation.ogg\'\necho\t\t\'python MidiToLabel.py MyMidiFile.mid\'\necho Alternatively you can use the script create-custom-glyph\necho\t\t\'python create-custom-glyph.py -l MyLabelsFile.txt -a MyAudioFile.ogg\'\necho\t\t\'pyhton create-custom-glyph.py -l MyLabelsFile.mid -a MyAudioFile.ogg\'\necho Info for the create-custom-glyph.py: Audio file should not be required to be .ogg, will be converted automatically.\necho.\necho IMPORTANT: You need to put "" around the arguments if your file names have spaces. e.g. "My Label File.txt"\ncall .\\venv\\Scripts\\activate.bat\ncmd /k\n@echo on'
    with open('custom_glyph_tools\\start.bat', 'w') as f:
        f.write(start_bat)

    printInfo("Creating SebiAi's github shortcut")
    with open('custom_glyph_tools\\SebiAi\'s github page.url', 'w') as f:
        f.write('[InternetShortcut]\nURL=' + Custom_Glyph_tools_GITHUB_URL)
    with open('custom_glyph_tools\\SebiAi\'s Tutorial.url', 'w') as f:
        f.write('[InternetShortcut]\nURL=' + SebiAi_Tutorial_URL)

    cprint("\nInstallation successful\n", color='green', attrs=['bold'])
    printInfo("To start using the custom glyph tools, just run \"start.bat\" in the \"custom_glyph_tools\" folder by double clicking it.")
    # open explorer in the custom_glyph_tools folder
    os.system('explorer custom_glyph_tools')
    removeShit(0)


# Print critical error message and exit
def printCriticalError(message: str, exitCode: int = 1):
    printError(message)
    #raise Exception(message)
    sys.exit(exitCode)

# Print error message
def printError(message :str):
    cprint("ERROR: " + message, color="red", attrs=["bold"], file=sys.stderr)

# Print warning message
def printWarning(message: str):
    cprint("WARNING: " + message, color="yellow", attrs=["bold"])

# Print info message
def printInfo(message: str):
    cprint("INFO: " + message, color="cyan")



match os.name:
    case 'nt':
        just_fix_windows_console()
        printInfo("Windows detected")
        WindowsInstallation()
    case 'posix':
        printInfo("Linux detected")
        LinuxInstallation()
    case 'darwin':
        printInfo("MacOS detected")
        MacOSInstallation()
    case default:
        printError("Unsupported operating system")
        sys.exit(1)
