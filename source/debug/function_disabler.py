import types

class FunctionDisabler:
    def __init__(self):
        self.disabled_functions = {}

    def disable(self, func_name):
        self.disabled_functions[func_name] = True

    def enable(self, func_name):
        self.disabled_functions[func_name] = False

    def is_disabled(self, func_name):
        return self.disabled_functions.get(func_name, False)

    def create_wrapper(self, func):
        def wrapper(self, *args, **kwargs):
            if disabler.is_disabled(func.__name__):  # Call is_disabled on disabler, not self
                # print(f"Function {func.__name__} is disabled")
                return None
            return func(self, *args, **kwargs)
        return wrapper

    def __str__(self):
        return str(self.disabled_functions)

disabler = FunctionDisabler()

def auto_disable(cls):
    original_init = cls.__init__
    def new_init(self, *args, **kwargs):
        original_init(self, *args, **kwargs)
        for name, method in cls.__dict__.items():
            if callable(method) and name != '__init__':
                setattr(self, name, types.MethodType(disabler.create_wrapper(method), self))
    cls.__init__ = new_init
    return cls

@auto_disable
class Test:
    def __init__(self):
        disabler.disable('test_func')  # Pass the method name as a string

    def test_func(self):
        print("test_func executed")

    def test_func1(self):
        print("test_func1 executed")

    def update(self):
        self.test_func()
        self.test_func1()
        print ("_____________________________________")

def main():
    # Usage:
    test = Test()

    # Try calling the disabled function
    test.update()  # This will print: "Function test_func is disabled"

    # Enable the function and try again
    disabler.enable('test_func')  # Pass the method name as a string
    test.update()  # This will print: "Test function executed"

if __name__ == "__main__":
    main()
