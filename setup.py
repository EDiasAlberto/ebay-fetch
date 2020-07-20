from cx_Freeze import setup, Executable

base = None

executables = [Executable("main.py", base=base)]

packages = ["idna", "ebaysdk.finding", "ebaysdk.trading", "tkinter", "random", "time", "tkinter.messagebox", "ebaysdk.trading.Connection"]
options = {
    'build_exe': {
        'packages':packages,
    },
}

setup(
    name = "EbayFetch",
    options = options,
    version = "1.0",
    description = 'Does what it says on the tin.',
    executables = executables
)
