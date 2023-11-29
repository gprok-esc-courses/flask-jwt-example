# What is args and kwargs

def example(a, *args, **kwargs):
    print("a=", a)
    print("args", args)
    print("kwargs", kwargs)


example("test", 1, 2, 3, 4, 5, width=4, height=5, color='blue')