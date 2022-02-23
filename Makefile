ifdef OS
	# Windows
	MKFILE_PATH := $(abspath $(lastword $(MAKEFILE_LIST)))
	MKFILE_DIR := $(dir $(MKFILE_PATH))
	SETUP_FILE = "$(MKFILE_DIR)setup.cfg"
	RM=del /q
	TS=Get-Date -UFormat "%s"
else
	# Linux
   	ifeq ($(shell uname), Linux)
    	RM = rm -f
		TS = date "+%s"
		VERSION = grep version setup.cfg | awk '{split(arr," ",$1);print arr[3];}'
   	endif
endif


build:
	python3 -m build -o output/dist/v0-0-3

install:
	python -m pip install .\output\dist\v0-0-3\tasktracker-0.0.3.tar.gz

version:
	(Get-Content "setup.cfg" | Select-String -Pattern "version" | Out-String) -replace "version = ","")
	$(VERSION)
	