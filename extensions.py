def loop(for_, i, in_, range_, start, stop, step, contents):
   import interpreter
   for i in range(start, stop, step):
      interpreter.evaluate(contents)


FUNCTIONS = {name : fun for (name, fun) in locals().items() if callable(fun)}