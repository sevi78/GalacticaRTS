import pstats

"""
how to use:
paste this:
    python -m cProfile -o output_file main.py
into the console.

the game will start and the profiler counts the function calls

to show the output file, run this script.

-1  = Ordered by: standard name
0   = Ordered by: call count
1   = Ordered by: internal time
2   = Ordered by: cumulative time


"""
p = pstats.Stats(r'C:\Users\sever\Documents\Galactica-RTS_zoomable1.107\output_file')

p.calc_callees()
p.strip_dirs().sort_stats(0).print_stats()

