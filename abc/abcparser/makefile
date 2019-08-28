CC=gcc
CFLAGS=-c -DANSILIBS
LNK=gcc

all : abc2midi

abc2midi : parseabc.o store.o genmidi.o queues.o parser2.o
	$(LNK) -o abc2midi parseabc.o store.o genmidi.o queues.o \
	parser2.o

parseabc.o : parseabc.c abc.h parseabc.h
	$(CC) $(CFLAGS) parseabc.c 

parser2.o : parser2.c abc.h parseabc.h parser2.h
	$(CC) $(CFLAGS) parser2.c

store.o : store.c abc.h parseabc.h genmidi.h
	$(CC) $(CFLAGS) store.c

queues.o : queues.c genmidi.h
	$(CC) $(CFLAGS) queues.c

clean :
	rm -f *.o abc2midi
