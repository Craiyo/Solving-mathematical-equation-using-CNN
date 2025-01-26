import subprocess

# List of required packages
required_packages = ['tensorflow', 'keras', 'customTkinter', 'tkinter']


# Function to install packages using pip
def install_packages():
    for package in required_packages:
        try:
            subprocess.check_call(['pip', 'install', package])
        except subprocess.CalledProcessError as e:
            print(f"Error installing package {package}: {e}")


# Check if packages are installed and install them if not
def check_and_install_packages():
    installed_packages = subprocess.check_output(['pip', 'freeze']).decode('utf-8').split('\n')
    for package in required_packages:
        if package not in installed_packages:
            print(f"Package '{package}' not found. Installing...")
            install_packages()


def run_main_py():
    try:
        subprocess.run(["python", "main.py"]) # Replace "main.py" with the name of your main script
    except FileNotFoundError:
        print("Error: main.py not found.")
    except Exception as e:
        print(f"Error: {e}")


if __name__ == "__main__":
    check_and_install_packages()
    run_main_py()
