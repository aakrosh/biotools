
CC = gcc
CFLAGS = -W -Wformat -Wimplicit -Wreturn-type -Wall -Werror \
         -Wunused-variable -Wunused-parameter -Wreturn-type -Wswitch \
         -Wcast-align -Winline -Wextra -g -ggdb

BINARIES = smith_waterman_align

all: $(BINARIES)

smith_waterman_align: asserts.h runtime.h runtime.c utilities.h utilities.c \
					  sequences.h sequences.c smith_waterman_align.c 
		$(CC) -c runtime.c
		$(CC) -c utilities.c
		$(CC) -c sequences.c
		$(CC) -o smith_waterman_align runtime.o utilities.o sequences.o smith_waterman_align.c
	

.PHONY: clean

clean:
	rm *.o $(BINARIES)
