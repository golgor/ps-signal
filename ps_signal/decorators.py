from functools import wraps


class VerbosePrinter:
    def __init__(self, timer: bool = False, text: str = None) -> None:
        self.timer = timer
        self.text = text

    def __call__(self, fn):
        @wraps(fn)
        def inner(*args, **kwargs):
            from time import perf_counter

            if self.text:
                print(self.text.center(50, "="))

            if self.timer:
                start = perf_counter()

            ret = fn(*args, **kwargs)

            if self.timer:
                elapsed_time = perf_counter() - start
                print(f"Elapsed time: {elapsed_time:.2f} seconds")
            print("="*50)
            return ret
        return inner


# Experimental decorator factory for decorating
# functions with extra attributes.
def attributes(**attrs):
    def decorator(f):
        @wraps(f)
        def wrapper(*args, **kwargs):
            return f(*args, **kwargs)

        for attr_name, attr_value in attrs.items():
            setattr(wrapper, attr_name, attr_value)

        return wrapper

    return decorator


"""

class A:
    def __init__(self):
        self.size = 0

    @attributes(modifies='size')
    def change_size(self, new):
        self.size = new


test = A()
print(A.change_size.modifies)


"""
