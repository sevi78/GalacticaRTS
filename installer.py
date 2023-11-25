import os
import sys
from fuzzywuzzy import fuzz
import subprocess
import tkinter as tk


class Installer:
    """
    Summary
    The Installer class is responsible for checking and installing missing dependencies for a Python application. It generates a requirements.txt file by analyzing the import statements in the Python files of the application. It then checks if the required dependencies are already installed and displays a message indicating the missing dependencies. If there are missing dependencies, the class provides an option to install them using pip.
    Example Usage
    installer = Installer()
    The above code creates an instance of the Installer class and starts the dependency checking process. If there are missing dependencies, a window is displayed showing the missing dependencies and an option to install them. If all dependencies are already installed, a message is displayed indicating that.
    Code Analysis
    Main functionalities
    Analyzing import statements in Python files to generate a requirements.txt file.
    Checking if the required dependencies are already installed.
    Displaying a message indicating the missing dependencies.
    Providing an option to install the missing dependencies using pip.

    Methods
    __init__(self): Initializes the Installer class by creating a Tkinter window and setting up the UI elements.
    generate_requirements_file(self): Generates a requirements.txt file by analyzing the import statements in the Python files of the application.
    check_for_dependencies(self) -> bool: Checks if the required dependencies are already installed and returns a boolean indicating the result.
    install(self): Installs the missing dependencies using pip.
    start_game(self): Closes the Tkinter window and starts the main application.

    Fields
    root: The Tkinter root window.
    message: A string variable to store the message to be displayed in the UI.
    install_button: A Tkinter button to trigger the installation of missing dependencies.
    cancel_button: A Tkinter button to cancel the installation process.
    missing_dependencies: A list to store the names of the missing dependencies.

    """

    def __init__(self):
        self.root = tk.Tk()
        self.root.title('Missing Dependencies')
        self.message = ""

        self.install_button = tk.Button(self.root, text='Install', command=lambda: self.install())
        self.install_button.pack(side=tk.LEFT, padx=5, pady=5)
        self.cancel_button = tk.Button(self.root, text='Cancel', command=lambda: self.root.destroy())
        self.cancel_button.pack(side=tk.RIGHT, padx=5, pady=5)

        self.missing_dependencies = []
        self.check_for_dependencies()
        self.label = tk.Label(self.root, text=self.message)
        self.label.pack()

        self.root.mainloop()

    def generate_requirements_file(self):
        path = os.path.dirname(os.path.realpath(__file__))
        pyfiles = []

        for root, dirs, files in os.walk(path):
            for file in files:
                if file.endswith('.py'):
                    pyfiles.append(os.path.join(root, file))

        stopWords = ['from', 'import', ',', '.']
        importables = []

        for file in pyfiles:
            with open(file) as f:
                content = f.readlines()

                for line in content:
                    if "import" in line:
                        for sw in stopWords:
                            line = ' '.join(line.split(sw))

                        importables.append(line.strip().split(' ')[0])

        subprocess.call(f"pip freeze > {path}/requirements.txt", shell=True)

        with open(path + '/requirements.txt') as req:
            modules = req.readlines()
            modules = {m.split('=')[0].lower(): m for m in modules}

        notList = [''.join(i.split('_')) for i in sys.builtin_module_names] + ['os']

        new_requirements = []
        for req_module in importables:
            try:
                new_requirements.append(modules[req_module])

            except KeyError:
                for k, v in modules.items():
                    if len(req_module) > 1 and req_module not in notList:
                        if fuzz.partial_ratio(req_module, k) > 90:
                            new_requirements.append(modules[k])

        new_requirements = [i for i in set(new_requirements)]

        with open(path + '/requirements.txt', 'w') as req:
            req.write(''.join(new_requirements))

    def check_for_dependencies(self) -> bool:
        if os.path.exists('requirements.txt'):
            os.remove('requirements.txt')  # Delete the old requirements.txt file

        self.generate_requirements_file()  # Generate a new requirements.txt file

        with open('requirements.txt') as f:
            dependencies = f.read().splitlines()

        for dependency in dependencies:
            try:
                __import__(dependency)
            except ImportError:
                self.missing_dependencies.append(dependency)

        if self.missing_dependencies:
            self.message = "The following dependencies are missing:\n\n" + "\n".join(self.missing_dependencies)
            return False
        else:
            self.message = 'All dependencies are already installed.'
            return True

    def install(self):
        subprocess.call(['pip', 'install', '-r', 'requirements.txt'])
        self.start_game()

    def start_game(self):
        self.root.destroy()
        import main
        main.main()


if __name__ == '__main__':
    installer = Installer()
