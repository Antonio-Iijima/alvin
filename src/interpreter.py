"""Manage interaction with the interpreter command-line."""



import os
import math
import random
import importlib

import config as cf
import extensions as ext



class Interpreter():
    """Interpreter command-line management."""

    def __init__(self):
        """Initialize exposed commands."""

        self.INTERPRETER = {
            "help"          : self.help,
            "keywords"      : self.show_keywords,
            "exit"          : self.quit,
            "quit"          : self.quit,
            "flags"         : self.flags,
            "clear"         : self.clear,
            "dev.info"      : self.show_dev,
            "dev.closures"  : self.show_closures,
            "dev.globals"   : self.show_globals,
            "dev.imports"   : self.show_imports,
            "dev.env"       : self.show_env
        }


    def prompt(self, text=None) -> None:
        """Prints the interpreter prompt."""
        text = cf.config.PROMPT if text is None else cf.config.set_color(text); print(text, flush=True, end='')


    def welcome(self) -> None:
        """Display a welcome text box."""

        display = """Welcome to the Alvin  
Programming Language"""

        self.text_box(display, centered=True)

        cf.config.iFlag and print(f"Alvin v{cf.config.VERSION}, running in interactive mode", end='\n'*(not cf.config.dFlag))
        cf.config.dFlag and print(" with debugging")
        cf.config.pFlag and print("Permanent extensions enabled")

        print("Enter 'help' to show further information")

        cf.config.zFlag and print(f"{cf.config.RED}WARNING: Random keyword deletion enabled.{cf.config.PURPLE} Proceed at your own risk.{cf.config.END_COLOR}")


    def help(self) -> None:
        """Display help information."""

        display = f"""The Alvin programming language was developed as an independent research project,
which began during CSCI 370: Programming Languages at Ave Maria University.
        
Documentation can be found on GitHub:
https://github.com/Antonio-Iijima/Alvin

{cf.config.PROMPT_SYMBOL} clear     : clear the terminal 
{cf.config.PROMPT_SYMBOL} exit/quit : exit the interpreter
{cf.config.PROMPT_SYMBOL} python *. : evaluate *. using Python
{cf.config.PROMPT_SYMBOL} flags     : display interpreter flags
{cf.config.PROMPT_SYMBOL} keywords  : display all language keywords
{cf.config.PROMPT_SYMBOL} dev.info  : useful development/debugging tools"""
        
        self.text_box(display)


    def clear(self) -> None:
        """Clear the terminal."""
        os.system('cls' if os.name == 'nt' else 'clear') or self.welcome()


    def quit(self) -> None:
        """Exit the interactive interpreter."""

        self.exit_extensions()

        if cf.config.zFlag:
            net = cf.config.ERROR_COUNTER - (len(cf.config.KEYWORDS) - cf.config.INITIAL_KEYWORD_NUM)
            print(f"\n{cf.config.PURPLE}You made {cf.config.ERROR_COUNTER} error{"s"*(cf.config.ERROR_COUNTER!=1)} with a net loss of {net} function{"s"*(abs(net)!=1)}.{cf.config.END_COLOR}")

        self.text_box("""Arrivederci!""", centered=True) or exit()


    def flags(self) -> None:
        """Display current active and inactive flags."""

        display = f"""Flags"""
        for flag in cf.config.FLAGS: display += f"\n{flag} : {cf.config.FLAGS[flag]}"

        self.text_box(display, centered=True)


    def show_closures(self) -> None:
        """Display the current closures."""
        
        print()
        if cf.config.CLOSURES:
            for entry, env in cf.config.CLOSURES.items():
                print(f"{entry}:\n{env}")  
        else: print("No function environments found.")
        print()
              

    def show_globals(self) -> None:
        """Display all global variables."""

        print()
        if cf.config.GLOBALS:
            print("Global variables:")
            for var, val in cf.config.GLOBALS.items():
                print(f" {var} : {val}")
        else: print("No global variables found.")
        print()


    def show_imports(self) -> None:
        """Display all currently imported modules and libraries."""

        print()
        if cf.config.IMPORTS:
            print("Imported modules:")
            for alias, module in cf.config.IMPORTS.items():
                print(f" {alias}") if alias == module.__name__ else print(f" {module.__name__} alias {alias}")
        else: print("No imported modules found.")
        print()


    def show_env(self):
        "Display current environment."
        print(cf.config.ENV)


    def show_dev(self) -> None:
        """Display useful dev tools."""

        display = f"""useful tools
                
{cf.config.PROMPT_SYMBOL} dev.closures : closures
{cf.config.PROMPT_SYMBOL} dev.env      : environment
{cf.config.PROMPT_SYMBOL} dev.globals  : global variables
{cf.config.PROMPT_SYMBOL} dev.imports  : imported modules"""
        
        self.text_box(display)


    def show_keywords(self) -> None:
        """Display all language keywords."""

        if not cf.config.KEYWORDS: print(f"{cf.config.RED}No keywords found."); return

        display = f"""KEYWORDS ({len(cf.config.KEYWORDS)}/{cf.config.INITIAL_KEYWORD_NUM})\n\n"""

        categories = {
            f"REGULAR ({len(cf.config.REGULAR)})"         : sorted(cf.config.REGULAR),
            f"IRREGULAR ({len(cf.config.IRREGULAR)})"     : sorted(cf.config.IRREGULAR),
            f"BOOLEAN ({len(cf.config.BOOLEAN)})"         : sorted(cf.config.BOOLEAN),
            f"SPECIAL ({len(cf.config.SPECIAL)})"         : sorted(cf.config.SPECIAL),
            f"ENVIRONMENT ({len(cf.config.ENVIRONMENT)})" : sorted(cf.config.ENVIRONMENT),
            f"EXTENSIONS ({len(cf.config.EXTENSIONS)})"   : sorted(cf.config.EXTENSIONS)
            }

        # Calculate the required character limit of each word
        offset = max(len(key) for key in cf.config.KEYWORDS) + 2

        # Iterate through each category
        for section_idx, section_title in enumerate(categories):

            # Add spacing between categories
            if section_idx > 0: display += "\n\n"

            # Add the section title
            display += f"{section_title}\n"

            # Iterate through the keywords in the section to organize into columns
            for keyword_idx, keyword in enumerate(categories[section_title]):

                # Move to the next row every three keywords
                if keyword_idx % 3 == 0: display += "\n"

                # Add each keyword along with the necessary amount of whitespace to justify the columns
                display += f"{keyword}{' ' * (offset-len(keyword))}"

                # If it is the end of a section and the keywords need to be justified
                column = (keyword_idx + 1) % 3
                if keyword_idx == len(categories[section_title]) - 1 and column != 0:
                    # Replace the 'missing words' with whitespace to complete the columns
                    display += ' ' * 2 * offset if column == 1 else ' ' * 1 * offset

        # Print the display
        self.text_box(display, centered=True)


    def text_box(self, text: str, centered: bool = False) -> None:
        """Display the provided string of `text` in a colorful printed box, either left-justified (default) or centered."""

        text = text.split("\n")
        
        # Maximum line length provides the necessary text justification 
        width = len(max(text, key=len))
        
        # Name components of the box for readability; add color to post
        bar, post = chr(9552), cf.config.set_color(chr(9553))
        top = f"{chr(9556)}" + bar*(width+2) + f"{chr(9559)}"
        bottom = f"{chr(9562)}" + bar*(width+2) + f"{chr(9565)}"
        
        # Print the top layer
        print()
        print(cf.config.set_color(top))

        for line in text:

            # Calculate required line offset
            offset = width - len(line)

            # Center if specified
            if centered: 
                offset /= 2
                line = f"{post} {' ' * math.floor(offset)}{line}{' ' * math.ceil(offset)} {post}"
            
            # Otherwise left-justify
            else: line = f"{post} {line}{' '*offset} {post}"
            
            print(line)
        
        # Print bottom layer
        print(cf.config.set_color(bottom))
        print()

        
    def extend(self, code: str, writable: bool = True) -> None:
        """Add extensions in Python to Alvin."""    

        # Segment code into list of strings by individual extension
        include, *exclude = code.removeprefix("@start").removesuffix("@end").strip().split("#EXCLUDE")
        
        # Remove leading empty string
        ext_list = include.split("#INCLUDE ")[1:]

        # Add individual extensions
        for extension in ext_list:

            # Separate <name> as <alias>
            name, alias = extension[:extension.find("\n")].split(" as ")

            if writable:
                
                extension = f"#INCLUDE {extension}\n\n\n"    
                
                # Get the current contents of the extensions.py file
                contents = open(f"{cf.config.PATH}/src/extensions.py").read()

                with open(f"{cf.config.PATH}/src/extensions.py", "w") as file: 
                    file.writelines(extension + contents)
                    
                # Reload extension file to show changes
                importlib.reload(ext)

            index = 0 if writable else len(cf.config.EXTENSION_LOG)

            # Add entry to log
            cf.config.EXTENSION_LOG.insert(index, (alias))

            # Create index entry
            cf.config.EXTENSION_INDEX.insert(index, (alias, len(extension.splitlines())))

            # Add entry to keywords
            cf.config.EXTENSIONS[alias] = ext.EXTENSIONS.get(name)
            cf.config.KEYWORDS.add(alias)
            

    def exit_extensions(self) -> None:
        """Safely save or remove any extensions added in an interactive interpreter session."""

        # Print informational text if saving new extensions
        if cf.config.pFlag:
            print(cf.config.GOLD)

            if len(cf.config.EXTENSION_LOG) > 0:
                print("The following extensions have been saved:")
                for ext in cf.config.EXTENSION_LOG: print(ext)
            else: print("No extensions saved.")

            print(cf.config.END_COLOR, end='')

        # Otherwise overwrite back to original
        else:
            with open(f"{cf.config.PATH}/src/extensions.py", "w") as file:
                file.writelines(cf.config.ORIGINAL_EXTENSIONS)
    

    def del_random_keyword(self) -> None:
        """Delete a random keyword from the language for the duration of the interpreter instance if the user makes a mistake."""

        keywords = [
            cf.config.REGULAR, 
            cf.config.IRREGULAR,
            cf.config.BOOLEAN, 
            cf.config.SPECIAL,
            cf.config.EXTENSIONS,
            cf.config.ENVIRONMENT
        ]
        
        keywords = [category for category in keywords if len(category) > 0]

        print(cf.config.PURPLE, end='')

        if keywords:
            category = None
            while not category: category = random.choice(keywords)
            item = random.choice(list(category))

            category.pop(item) if isinstance(category, dict) else category.discard(item)
            cf.config.KEYWORDS.remove(item)
                             
            print(f"You just lost the '{item}' function. Number of keywords remaining: {len(cf.config.KEYWORDS)}")

        else: print(f"You have nothing left to lose. The language is now utterly and completely broken. Congratulations.")
        
        cf.config.ERROR_COUNTER += 1
        
        print(cf.config.END_COLOR, end='')



interpreter = Interpreter()
