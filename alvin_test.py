import main
import os

def test(directory='test_cases', args=[]):

    # Execute all test files
    for file in os.listdir(directory):
        if file.endswith('.alv'):
            print(f"TESTING: {file}")
            main.main(args + [f"{directory}/{file}"])
            print("\n\n")
        else:
            print(f"ENTERING FOLDER: {file}/\n\n\n")
            test(f"{directory}/{file}", args)


print("Running without files")
main.main(args = ['main.py'])

print("\n\nRunning without flags")
test(args = ['main.py'])


for flag in main.FLAGS:
    print(f"Running with {flag} flag")
    test(args = ['main.py', flag])

print("Last things")
test(args = ['main.py', "-p", "final_test.alv"])