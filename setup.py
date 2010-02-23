from distutils.core import setup
import py2exe,sys,os

origIsSystemDLL = py2exe.build_exe.isSystemDLL
def isSystemDLL(pathname):
        if os.path.basename(pathname).lower() in ["sdl_ttf.dll"]:
                return 0
        return origIsSystemDLL(pathname)
py2exe.build_exe.isSystemDLL = isSystemDLL

setup(
        windows=['main.py'],
		zipfile=None,
        options={
                "py2exe":{
                        "unbuffered": True,
                        "optimize": 2,
						"bundle_files": 1
                }
        },
		MODULE_EXCLUDES =[
			'email',
			'AppKit',
			'Foundation',
			'bdb',
			'difflib',
			'tcl',
			'Tkinter',
			'Tkconstants',
			'curses',
			'distutils',
			'setuptools',
			'urllib',
			'urllib2',
			'urlparse',
			'BaseHTTPServer',
			'_LWPCookieJar',
			'_MozillaCookieJar',
			'ftplib',
			'gopherlib',
			'_ssl',
			'htmllib',
			'httplib',
			'mimetools',
			'mimetypes',
			'rfc822',
			'tty',
			'webbrowser',
			'socket',
			'hashlib',
			'base64',
			'compiler',
			'pydoc']
)