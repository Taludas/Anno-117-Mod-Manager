PACKAGE=anno117-modmanager
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
	pyinstaller --onefile --windowed --add-data "data;data" --name "Anno 117 Mod Manager" $(PACKAGE).py

exe.clean:
	rd /s /q build
	del /q dist\$(PACKAGE).exe
	del /q $(PACKAGE).spec


# general make targets ###########################

all: libs exe

all.clean: libs.clean exe.clean

clean: all.clean