import os
import sys
import subprocess



def test(filepath='.', args=[]):

    if os.path.isfile(filepath) and filepath.endswith('.alv'):
        print(f"\nFILE: {filepath}")
        subprocess.run(f"coverage run --parallel-mode ../src/main.py {filepath} {" ".join(args)}", shell=True)
        print()

    elif os.path.isdir(filepath):
        for file in os.listdir(filepath): 
            if file not in ["htmlcov"]: test(f"{filepath}/{file}", args)


def main(initialDirectory = "../test", withFlags=False):
    print("\nRunning without flags\n")
    test(initialDirectory)

    if withFlags:
        for flag in ["-i", "-d", "-p", "-z"]:
            print(f"Running with {flag} flag")
            test(initialDirectory, args = [flag])

    subprocess.run("coverage combine", shell=True)
    print()
    subprocess.run("coverage report", shell=True)
    print()
    subprocess.run("coverage html", shell=True)



if __name__ == "__main__": main(*sys.argv[1:])
