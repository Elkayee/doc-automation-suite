# Build both entrypoints against one dependency graph and one resource folder.
from pathlib import Path

from PyInstaller.utils.hooks import collect_all

root = Path(SPECPATH).parent
datas = [
    (str(root / 'templates'), 'templates'),
    (str(root / 'assets'), 'assets'),
    (str(root / 'src/ui/visual_builder/styles.css'), 'src/ui/visual_builder'),
    (str(root / 'src/core/lo_refresh.py'), 'src/core'),
]
binaries, hiddenimports = [], ['uvicorn.logging', 'uvicorn.loops.auto', 'uvicorn.protocols.http.auto', 'uvicorn.lifespan.on']
for package in ['tkinterweb', 'tkinterweb_tkhtml']:
    package_datas, package_binaries, package_imports = collect_all(package)
    datas += package_datas
    binaries += package_binaries
    hiddenimports += package_imports

a = Analysis([str(root / 'main.py'), str(root / 'automation.py')], pathex=[str(root)],
             binaries=binaries, datas=datas, hiddenimports=hiddenimports)
pyz = PYZ(a.pure)
hooks = [script for script in a.scripts if script[0] not in {'main', 'automation'}]
gui_scripts = hooks + [script for script in a.scripts if script[0] == 'main']
cli_scripts = hooks + [script for script in a.scripts if script[0] == 'automation']
gui = EXE(pyz, gui_scripts, [], exclude_binaries=True, name='DocAutomationSuite',
          console=False, icon=str(root / 'assets/app.ico'), upx=False)
cli = EXE(pyz, cli_scripts, [], exclude_binaries=True, name='DocAutomationCLI',
          console=True, icon=str(root / 'assets/app.ico'), upx=False)
bundle = COLLECT(gui, cli, a.binaries, a.datas, name='DocAutomationSuite', upx=False)
