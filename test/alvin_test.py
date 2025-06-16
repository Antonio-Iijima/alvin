import os
import subprocess



def test(directory='.', args=[]):
    
    # Execute all test files
    for item in os.listdir(directory):
        if item.endswith('.alv'):
            print(f"\nFILE: {item}")
            subprocess.run(f"coverage run --parallel-mode ../src/main.py {directory}/{item} {" ".join(args)}", shell=True)
            print()

        elif os.path.isdir(item):
            print(f"\n\nFOLDER: {item}/\n\n")
            test(f"{directory}/{item}", args)


def main(withFlags=False):
    print("\nRunning without flags\n")
    test("../examples")

    if withFlags:
        for flag in ["-i", "-d", "-p", "-z"]:
            print(f"Running with {flag} flag")
            test("../examples", args = [flag])

    subprocess.run("coverage combine", shell=True)
    print()
    subprocess.run("coverage report", shell=True)
    print()
    subprocess.run("coverage html", shell=True)

    #print("Last things")
    #test(args = ["-p", "final_test.alv"])


if __name__ == "__main__": main()
