PACKAGE=anno117-modmanager
EXENAME=Anno.117.Mod.Manager
VENVNAME=tamm

##############################################################################
# do this while not in venv
venv:
	python -m venv .$(VENVNAME).venv

venv.clean:
	rd /s /q .$(VENVNAME).venv



##############################################################################
# do these while in venv
run: libs.quiet
	py $(PACKAGE).py


# libs make targets ###########################
libs: requirements.txt
	pip install -r requirements.txt

libs.quiet: requirements.txt
	pip install -q -r requirements.txt

libs.clean:
	pip uninstall -r requirements.txt


# exe make targets ###########################
exe: libs
	pyinstaller --onefile --windowed --add-data "data;data" --icon="app_icon.ico" --version-file="file_version_info.txt" --name $(EXENAME) $(PACKAGE).py

exe.clean:
	-cmd /c rd /s /q build
	-cmd /c rd /s /q dist
	-cmd /c del /q $(EXENAME).spec


# general make targets ###########################

all: libs exe

all.clean: libs.clean exe.clean

clean: all.clean