import ctypes
import gc
import inspect
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

    def delete_references(self, obj):
        """
        Delete all references to the given object.

        Args:
            obj: The object for which references should be deleted.

        Returns:
            None
        """
        # Get a list of objects that reference the input object
        referrers = gc.get_referrers(obj)

        # Iterate over the referrers
        for ref in referrers:
            # Check if the referrer is a dictionary
            if isinstance(ref, dict):
                # Iterate over the dictionary items
                for key, value in list(ref.items()):
                    if value is obj:
                        # Delete the reference by setting the value to None
                        ref[key] = None

            # Check if the referrer is a list or a set
            elif isinstance(ref, (list, set, tuple)):
                # Create a new container without the reference
                new_container = [item for item in ref if item is not obj]
                # Replace the old container with the new one
                if isinstance(ref, list):
                    ref[:] = new_container
                else:
                    ref_type = type(ref)
                    ctypes.pythonapi.PyTypeReplaceObject(ctypes.py_object(ref), ctypes.py_object(ref_type(new_container)))

            # Check if the referrer is an object with attributes
            elif hasattr(ref, "__dict__"):
                # Iterate over the object's attributes
                for attr, value in list(vars(ref).items()):
                    if value is obj:
                        # Delete the reference by setting the attribute to None
                        setattr(ref, attr, None)

        # Trigger garbage collection
        gc.collect()

    def get_memory_usage(self):
        process = psutil.Process(os.getpid())
        mem_info = process.memory_info()
        mem_usage_in_MB = mem_info.rss / (1024 ** 2)
        return mem_usage_in_MB

    def show_references(self, obj, max_depth=3, depth=0):
        """
        Show all references to the given object.

        Args:
            obj: The object for which references should be shown.
            max_depth (int): The maximum depth to traverse the reference tree.
            depth (int): The current depth in the reference tree (used for recursion).

        Returns:
            None
        """
        # Get a list of objects that reference the input object
        referrers = gc.get_referrers(obj)

        # Print the current object and its type
        print(f"{'  ' * depth}Object: {obj} ({type(obj)})")

        # Recursively show references for each referrer
        if depth < max_depth:
            for ref in referrers:
                # Check if the referrer is a module, class, or function
                if inspect.ismodule(ref) or inspect.isclass(ref) or inspect.isfunction(ref):
                    # Print the module, class, or function name
                    print(f"{'  ' * (depth + 1)}Referenced by: {ref.__name__} ({type(ref)})")
                else:
                    # Recursively show references for the referrer
                    self.show_references(ref, max_depth, depth + 1)


garbage_handler = GarbageHandler()
