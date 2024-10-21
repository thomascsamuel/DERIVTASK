import subprocess
import os

def run_tests():
    # Execute pytest with the desired options
    result = subprocess.run(['pytest', '--html=reports/test_reports.html'], capture_output=True, text=True)
    
    # Print the output of pytest
    print(result.stdout)
    print(result.stderr)
    
    if result.returncode == 0:
        print("All tests passed.")
    else:
        print("Some tests failed.")

if __name__ == "__main__":
    run_tests()
