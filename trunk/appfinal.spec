# -*- mode: python -*-
a = Analysis([os.path.join(HOMEPATH,'support\\_mountzlib.py'), os.path.join(HOMEPATH,'support\\useUnicode.py'), 'D:\\data\\Fragster\\FDH\\app.py'],
             pathex=['D:\\data\\Fragster\\FDH\\pyinstaller\\final'],
             )
pyz = PYZ(a.pure)
exe = EXE(pyz,
          a.scripts,
          exclude_binaries=1,
          name=os.path.join('build\\pyi.win32\\app', 'FDHClient.exe'),
          debug=False,
          strip=False,
          upx=True,
          console=False,
          windowed = True,
          icon='D:\\data\\Fragster\\FDH\\media\\fdh.ico',
          #upx_binaries=1,
          )
exe2 = EXE(pyz,
          a.scripts,
          exclude_binaries=1,
          name=os.path.join('build\\pyi.win32\\appdbg', 'FDHClient_Debug.exe'),
          debug=True,
          strip=False,
          upx=True,
          console=True,
          windowed = False,
          icon='D:\\data\\Fragster\\FDH\\media\\fdh.ico',
          #upx_binaries=1,
          )
coll = COLLECT( exe,
               a.binaries,
               a.zipfiles,
               strip=False,
               #upx=True,
               #upx_binaries=1,
               name=os.path.join('distfinal', 'app'))

coll = COLLECT( exe2,
               strip=False,
               #upx=True,
               #upx_binaries=1,
               name=os.path.join('distfinal_debug', 'app'))