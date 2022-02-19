ifdef OS
	# Windows
	RM = del /q
	TS = Get-Date -UFormat "%s"
else
	# Linux
   	ifeq ($(shell uname), Linux)
    	RM = rm -f
		TS = date
   	endif
endif