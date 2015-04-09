#
EXE = mp3
OBJS = parse.o main.o

COMPILER = g++
COMPILER_OPTS = -c -g -O0 -Wall -Werror
LINKER = g++
#LINKER_OPTS = -lpng

all : $(EXE)

$(EXE) : $(OBJS)
	$(LINKER) $(OBJS) -o $(EXE)

parse.o : parse.cpp
	$(COMPILER) -c $(COMPILER_OPTS) parse.cpp

main.o : main.cpp parse.h
	$(COMPILER) -c $(COMPILER_OPTS) main.cpp
	
clean :
	-rm -f *.o $(EXE)
