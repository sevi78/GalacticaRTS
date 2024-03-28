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
p.strip_dirs().sort_stats(2).print_stats()
# get screen info
# pygame.init()
# print (pygame.display.Info())


# event count to find out wich events are called the most
event_counts = {}


def profile_events(events):
    for event in events:
        if event.type not in event_counts:
            event_counts[event.type] = 0
        event_counts[event.type] += 1
    return event_counts

# print (f"event count {profile_events(events)}")



"""

use pygount to get a summary of the code

PS C:\Users\sever\Documents\Galactica-RTS_zoomable1.107> pygount --format=summary                                                       
┏━━━━━━━━━━━━━━━┳━━━━━━━┳━━━━━━━┳━━━━━━━━┳━━━━━━┳━━━━━━━━━┳━━━━━━┓
┃ Language      ┃ Files ┃     % ┃   Code ┃    % ┃ Comment ┃    % ┃
┡━━━━━━━━━━━━━━━╇━━━━━━━╇━━━━━━━╇━━━━━━━━╇━━━━━━╇━━━━━━━━━╇━━━━━━┩
│ JSON          │    88 │   6.0 │  95434 │ 83.9 │       0 │  0.0 │
│ Python        │   358 │  24.5 │  32842 │ 62.0 │   10121 │ 19.1 │
│ C             │     1 │   0.1 │  12633 │ 77.1 │    2005 │ 12.2 │
│ Cython        │     1 │   0.1 │    197 │ 51.7 │      64 │ 16.8 │
│ Text only     │     5 │   0.3 │     48 │ 70.6 │       0 │  0.0 │
│ Markdown      │     1 │   0.1 │     35 │ 66.0 │       0 │  0.0 │
│ __unknown__   │    10 │   0.7 │      0 │  0.0 │       0 │  0.0 │
│ __empty__     │     1 │   0.1 │      0 │  0.0 │       0 │  0.0 │
│ __duplicate__ │   392 │  26.8 │      0 │  0.0 │       0 │  0.0 │
│ __binary__    │   607 │  41.5 │      0 │  0.0 │       0 │  0.0 │
├───────────────┼───────┼───────┼────────┼──────┼─────────┼──────┤
│ Sum           │  1464 │ 100.0 │ 141189 │ 76.9 │   12190 │  6.6 │
└───────────────┴───────┴───────┴────────┴──────┴─────────┴──────┘


"""
