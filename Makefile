bld/fraction: bld/fraction.o
	gcc -o bld/fraction bld/fraction.o

bld/fraction.o: fraction.c
	mkdir -p bld
	gcc -c fraction.c -o bld/fraction.o

clean:
	rm -rf bld/*
