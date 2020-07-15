class VerbosePrinter:
    def __init__(self, timer: bool = False, text: str = None) -> None:
        self.timer = timer
        self.text = text

    def __call__(self, fn):
        def inner(*args, **kwargs):
            from time import perf_counter

            if self.timer:
                start = perf_counter()

            ret = fn(*args, **kwargs)

            if self.text:
                print(self.text.center(50, "="))

            if self.timer:
                elapsed_time = perf_counter() - start
                print(f"Elapsed time: {elapsed_time} seconds")
            print("="*50)
            return ret
        return inner
