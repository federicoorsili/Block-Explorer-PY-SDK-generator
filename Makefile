generate:
	python3 Classes/generator/generator.py -a ./abis
	python3 generate_structures.py
	rm generate_structures.py

clear:
	python3 Classes/generator/cleaner.py -a ./abis

run:
	python3 main.py