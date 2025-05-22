def loop(for_, i, in_, range_, start, stop, step, contents):
   from evaluate import evaluate
   for i in range(start, stop, step):
      evaluate(contents)
      


# List of all currently defined extensions
EXTENSIONS = {name : fun for (name, fun) in locals().items() if callable(fun)}
