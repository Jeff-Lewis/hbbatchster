import os
from distutils.core import setup
from py2exe.build_exe import py2exe as py2e
import py2exe

class Py2exe(py2e):
    def initialize_options(self):
        # Add a new "upx" option for compression with upx
        py2e.initialize_options(self)
        self.upx = 0

    def copy_file(self, *args, **kwargs):
        # Override to UPX copied binaries.
        (fname, copied) = result = py2e.copy_file(self, *args, **kwargs)

        basename = os.path.basename(fname)
        if (copied and self.upx and
            (basename[:6]+basename[-4:]).lower() != 'python.dll' and
            fname[-4:].lower() in ('.pyd', '.dll')):
            os.system('upx --best "%s"' % os.path.normpath(fname))
        return result

    def patch_python_dll_winver(self, dll_name, new_winver=None):
        # Override this to first check if the file is upx'd and skip if so
        if not self.dry_run:
            if not os.system('upx -qt "%s" >nul' % dll_name):
                if self.verbose:
                    print "Skipping setting sys.winver for '%s' (UPX'd)" % \
                          dll_name
            else:
                py2e.patch_python_dll_winver(self, dll_name, new_winver)
                # We UPX this one file here rather than in copy_file so
                # the version adjustment can be successful
                if self.upx:
                    os.system('upx --best "%s"' % os.path.normpath(dll_name))
                    
origIsSystemDLL = py2exe.build_exe.isSystemDLL
def isSystemDLL(pathname):
        if os.path.basename(pathname).lower() in ("msvcp71.dll", "dwmapi.dll"):
                return 0
        return origIsSystemDLL(pathname)
py2exe.build_exe.isSystemDLL = isSystemDLL

setup(
    cmdclass = {'py2exe': Py2exe},
    windows=[{
                "script":'app.py', 
                "dest_base": "HBBatchster",
                "icon_resources": [(0, "handbrakepineapple2.ico")]
            }], 
    options={
                "py2exe":{
                        #"unbuffered": True,
                        "optimize": 2,
                        "bundle_files":3,
                        #"includes": ["agw"],
                        "upx":True,
                        "compressed":True,
                        "excludes": ['doctext', 'pdb', 'unittest', 'difflib', 'inspect', '_ssl'],
                },
        },
    name="HBBatchster",
)