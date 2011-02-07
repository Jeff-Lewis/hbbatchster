# -*- mode: python -*-
a = Analysis([os.path.join(HOMEPATH,'support\\_mountzlib.py'), os.path.join(HOMEPATH,'support\\useUnicode.py'), 'D:\\data\\___small\\HBBatchster\\app.py'],
             pathex=['D:\\data\\___small\\HBBatchster\\repository\\hbbatchster\trunk'], excludes=['doctext', 'pdb', 'unittest', 'difflib', 'inspect', '_ssl'])
pyz = PYZ(a.pure)
exe = EXE(pyz,
          a.scripts,
          exclude_binaries=1,
          name=os.path.join('build\\pyi.win32\\app', 'HBBatchster.exe'),
          debug=False,
          strip=False,
          upx=True,
          icon='D:\\data\\___small\\HBBatchster\\repository\\hbbatchster\\trunk\\handbrakepineapple2.ico',
          version="version.txt",
          console=False )
coll = COLLECT( exe,
               a.binaries,
               a.zipfiles,
               strip=False,
               upx=True,
               name=os.path.join('dist', 'app'))
