# wiktors way of creating test functions automatically, no asserts just the function name, makes it easier to create tests

get_filename = "/home/wiktor/Desktop/project/monitoring.py"
target_filename = "/home/wiktor/Desktop/project/test/test_monitoring.py"

functions = []
with open(file=get_filename, mode="r") as f:
    for line in f.readlines():
        line = line.lstrip()
        if line.startswith("def"):
            if line != "__init__" or line != "__repr":
                functions.append(line.split("(")[0].split(" ")[1])


with open(file=target_filename, mode="a") as f:
    for function in functions:
        f.write(f"def test_{function}():\n\tpass\n\n")

