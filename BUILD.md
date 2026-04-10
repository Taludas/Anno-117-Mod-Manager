### Build and Installation Steps:
The anno117-modmanager utility makes use of a virtual python environment, and creates a standalone executable, which can be copied to a local directory such as /usr/local/bin or similar.

The build process is controlled via a makefile.

Build steps:
```
git clone git@github.com:ewjax/Anno-117-Mod-Manager.git
cd Anno-117-Mod-Manager
make venv
```
Activate the python virtual environment, then continue the build process:
```
(unix): source .tamm.venv/bin/activate
(windows): .tamm.venv\Scripts\activate
make all
Executable will be placed in ./dist subdirectory
```
Test the executable, by running it with the 'help' option:
```
./dist/anno117-modmanagerg -h
```
Assuming it shows a list of command line options, indicating it built successfully, copy the anno117-modmanagerg (or anno117-modmanagerg.exe) executable from the /dist subdirectory to somewhere in your path.

Cleanup steps:
```
(while still in the python virtual environment): 
make clean
deactivate
make venv.clean
```