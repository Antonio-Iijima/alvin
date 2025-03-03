
# List of all currently defined extensions
EXTENSIONS = {name : fun for (name, fun) in locals().items() if callable(fun)}