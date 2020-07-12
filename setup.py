from cx_Freeze import setup, Executable

base = None

executables = [Executable("findingAPI.py", base=base)]

packages = ["idna", "ebaysdk.finding", "ebaysdk.trading"]
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
