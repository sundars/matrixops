fraction: fraction.c
	mkdir -p bld
	gcc -c fraction.c -o bld/fraction.o
	gcc -o bld/fraction bld/fraction.o

clean:
	rm -rf bld/*
