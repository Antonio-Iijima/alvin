import os
import sys
import subprocess



def test(directory='.', args=[]):
    
    # Execute all test files
    for item in os.listdir(directory):
        if item in ["exceptions"]: continue
        if item.endswith('.alv'):
            print(f"\nFILE: {directory}/{item}")

            subprocess.run(f"coverage run --parallel-mode ../src/main.py {directory}/{item} {" ".join(args)}", shell=True)
            print()

        elif os.path.isdir(item) and item != "htmlcov": test(f"{directory}/{item}", args)


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
