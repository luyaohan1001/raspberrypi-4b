all: helloworld


helloworld: clean
	as helloworld.s -o helloworld.o
	ld helloworld.o -o helloworld

clean:
	rm -rf helloworld.o helloworld
