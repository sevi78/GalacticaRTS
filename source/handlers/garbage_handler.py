import gc
import os

import psutil


class GarbageHandler:
    def delete_all_references(self, obj, obj1):  # smooth reference deleter

        for key, value in obj.__dict__.items():
            if obj1 == value:
                setattr(obj, key, None)
            if type(value) == list:
                if obj1 in value:
                    value.remove(obj1)
        try:
            for key, value in obj1.__dict__.items():
                if obj == value:
                    setattr(obj1, key, None)
                if type(value) == list:
                    if obj in value:
                        value.remove(obj)
        except AttributeError:
            pass

    def delete_all_references_from(self, obj):  # stupid ki function
        referrers = gc.get_referrers(obj)
        for referrer in referrers:
            if isinstance(referrer, dict):
                for key, value in list(referrer.items()):
                    if value is obj:
                        del referrer[key]
            elif isinstance(referrer, list):
                while obj in referrer:
                    referrer.remove(obj)
            # Add more cases for other container types if needed

        # Check if the object is still referenced
        remaining_referrers = gc.get_referrers(obj)
        if len(remaining_referrers) > 0:
            print("Warning: Some references could not be removed.", remaining_referrers)

    def get_memory_usage(self):
        process = psutil.Process(os.getpid())
        mem_info = process.memory_info()
        mem_usage_in_MB = mem_info.rss / (1024 ** 2)
        return mem_usage_in_MB


garbage_handler = GarbageHandler()
