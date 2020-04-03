from cx_Freeze import setup, Executable
import sys, os

os.environ['TCL_LIBRARY'] = r'C:\\Users\\dasoc\\AppData\\Local\\Programs\\Python\\Python36-32\\tcl\\'
os.environ['TK_LIBRARY'] = r'C:\\Users\\dasoc\\AppData\\Local\\Programs\\Python\\Python36-32\\tcl\\'
#base = 'Win32GUI' if sys.platform == 'win32' else None

#productName = "ProductName"
#if 'bdist_msi' in sys.argv:
#    sys.argv += ['--initial-target-dir', 'E:\\RocketLeagueHoops\\OverlayGenerator\\' + productName]
#    sys.argv += ['--install-script', 'OverlayGenerator.py']

#exe = Executable(
#      script="OverlayGenerator.py",
#      base=base,
#      targetName="OverlayGenerator.exe"
#     )
#setup(
#      name="OverlayGenerator.exe",
#      version="1.0",
#      author="Me",
#      description="Copyright 2012",
#      executables=[exe]
#      )

base = None


executables = [Executable("OverlayGenerator.py", base=base)]

#packages = ["PIL, tkinter"]
build_exe_options = {
    'packages': ["tkinter","os","sys","PIL"],
    'include_files': ["img/rhicon.png"]
}

setup(
    name = "OverlayGenerator",
    options = {"build_exe": build_exe_options},
    version = "1.0",
    description = 'OverlayGenerator',
    executables = executables
)