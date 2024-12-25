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
pygount --format=summary ./your-directory

                                                  
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


┏━━━━━━━━━━━━━━━┳━━━━━━━┳━━━━━━━┳━━━━━━━━┳━━━━━━┳━━━━━━━━━┳━━━━━━┓                                                                                                                                                                    
┃ Language      ┃ Files ┃     % ┃   Code ┃    % ┃ Comment ┃    % ┃
┡━━━━━━━━━━━━━━━╇━━━━━━━╇━━━━━━━╇━━━━━━━━╇━━━━━━╇━━━━━━━━━╇━━━━━━┩
│ JSON          │    72 │   4.1 │  97673 │ 83.8 │      21 │  0.0 │
│ Python        │   409 │  23.1 │  43938 │ 61.5 │   14671 │ 20.5 │
│ Text only     │     5 │   0.3 │     48 │ 70.6 │       0 │  0.0 │
│ Markdown      │     1 │   0.1 │     35 │ 63.6 │       0 │  0.0 │
│ __unknown__   │    10 │   0.6 │      0 │  0.0 │       0 │  0.0 │
│ __empty__     │     1 │   0.1 │      0 │  0.0 │       0 │  0.0 │
│ __duplicate__ │   680 │  38.4 │      0 │  0.0 │       0 │  0.0 │
│ __binary__    │   591 │  33.4 │      0 │  0.0 │       0 │  0.0 │
├───────────────┼───────┼───────┼────────┼──────┼─────────┼──────┤
│ Sum           │  1769 │ 100.0 │ 141694 │ 75.3 │   14692 │  7.8 │
└───────────────┴───────┴───────┴────────┴──────┴─────────┴──────┘


┏━━━━━━━━━━━━━━━┳━━━━━━━┳━━━━━━━┳━━━━━━━━┳━━━━━━┳━━━━━━━━━┳━━━━━━┓
┃ Language      ┃ Files ┃     % ┃   Code ┃    % ┃ Comment ┃    % ┃      
┡━━━━━━━━━━━━━━━╇━━━━━━━╇━━━━━━━╇━━━━━━━━╇━━━━━━╇━━━━━━━━━╇━━━━━━┩    
│ JSON          │    91 │   3.3 │ 142850 │ 83.4 │      21 │  0.0 │
│ Python        │   424 │  15.5 │  45865 │ 61.3 │   15627 │ 20.9 │
│ Text only     │     5 │   0.2 │     48 │ 70.6 │       0 │  0.0 │
│ Markdown      │     1 │   0.0 │     35 │ 63.6 │       0 │  0.0 │
│ __unknown__   │    10 │   0.4 │      0 │  0.0 │       0 │  0.0 │
│ __empty__     │     1 │   0.0 │      0 │  0.0 │       0 │  0.0 │
│ __duplicate__ │  1556 │  56.9 │      0 │  0.0 │       0 │  0.0 │
│ __binary__    │   645 │  23.6 │      0 │  0.0 │       0 │  0.0 │
├───────────────┼───────┼───────┼────────┼──────┼─────────┼──────┤
│ Sum           │  2733 │ 100.0 │ 188798 │ 76.7 │   15648 │  6.4 │
└───────────────┴───────┴───────┴────────┴──────┴─────────┴──────┘



"""
