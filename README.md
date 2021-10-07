# Image processing assignment 1

Source code for first assignment in Image processing course at Polytech Paris-Saclay engineering school.

It replaces fragments of the famous fresco *[The Creation of Adam](https://en.wikipedia.org/wiki/The_Creation_of_Adam)* by Michelangelo, using a ready-made solution, to introduce OpenCV library.

This file contains instructions for using it (report extract).

Clone the project first :

```sh
git clone https://github.com/furtivesock/img-prc-assignment1.git
```

## Exercise 1

> The goal of this exercise is to replace fragments on the fresco.

1. Move to the `src/` directory

```sh
cd img-prc-assignment1/src/
```

2. Run the script

```sh
python3 ex1.py
```

If you are on a Unix-like operating system, you can also make it executable :

```sh
chmod +x ex1.py
./ex1.py
```
            
After a few seconds of processing, the final image should appear.

## Exercise 2

> The goal of this exercise is to compute solution precision in comparison with the right solution (seen in the previous exercise). 

1. Move to the `src/` directory

```sh
cd img-prc-assignment1/src/
```

2. Generate the different solutions

```sh
python3 solution_generator.py
ls ../solutions # to see the solutions content
```

3. Run the script

```sh
python3 ex2.py
```

or

```
chmod +x ex2.py
./ex2.py
```