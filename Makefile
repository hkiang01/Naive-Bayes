#
EXE = mp3
OBJS = digit.o main.o

COMPILER = g++
COMPILER_OPTS = -c -g -O0 -Wall -Werror
LINKER = g++
#LINKER_OPTS = -lpng

all : $(EXE)

$(EXE) : $(OBJS)
	$(LINKER) $(OBJS) -o $(EXE)

digit.o : digit.cpp
	$(COMPILER) -c $(COMPILER_OPTS) digit.cpp

main.o : main.cpp digit.h
	$(COMPILER) -c $(COMPILER_OPTS) main.cpp
	
clean :
	-rm -f *.o $(EXE)
