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
p.strip_dirs().sort_stats(1).print_stats()
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
                                                  
┏━━━━━━━━━━━━━━━┳━━━━━━━┳━━━━━━━┳━━━━━━━┳━━━━━━┳━━━━━━━━━┳━━━━━━┓
┃ Language      ┃ Files ┃     % ┃  Code ┃    % ┃ Comment ┃    % ┃
┡━━━━━━━━━━━━━━━╇━━━━━━━╇━━━━━━━╇━━━━━━━╇━━━━━━╇━━━━━━━━━╇━━━━━━┩
│ JSON          │    37 │   2.3 │ 42802 │ 83.5 │       0 │  0.0 │
│ Python        │   196 │  12.0 │ 19508 │ 62.2 │    6187 │ 19.7 │
│ Text only     │     5 │   0.3 │    48 │ 70.6 │       0 │  0.0 │
│ Markdown      │     1 │   0.1 │    35 │ 63.6 │       0 │  0.0 │
│ __unknown__   │     9 │   0.6 │     0 │  0.0 │       0 │  0.0 │
│ __empty__     │     1 │   0.1 │     0 │  0.0 │       0 │  0.0 │
│ __duplicate__ │   810 │  49.6 │     0 │  0.0 │       0 │  0.0 │
│ __binary__    │   575 │  35.2 │     0 │  0.0 │       0 │  0.0 │
├───────────────┼───────┼───────┼───────┼──────┼─────────┼──────┤
│ Sum           │  1634 │ 100.0 │ 62393 │ 75.4 │    6187 │  7.5 │
└───────────────┴───────┴───────┴───────┴──────┴─────────┴──────┘



"""
