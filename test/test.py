import os
import sys



def test(filepath: str = '.', args: list = []):

    if os.path.isfile(filepath) and filepath.endswith('.alv'):
        os.system(f"echo '\nFILE: {filepath}'")
        os.system(f"coverage run --parallel-mode ../src/main.py {filepath} {" ".join(args)} && echo")

    elif os.path.isdir(filepath):
        for file in sorted(os.listdir(filepath)): 
            if file not in ["htmlcov"]: test(f"{filepath}/{file}", args)


def main(initialDirectory: str = "../test", *flags):

    os.system("echo '\nRunning without flags\n'")
    test(initialDirectory)
    
    for flag in flags:
        os.system(f"echo 'Running with {flag} flag'")
        test(initialDirectory, args = [flag])

    os.system("coverage combine")

    os.system("coverage report")

    os.system("coverage html")



if __name__ == "__main__": main(*sys.argv[1:])
