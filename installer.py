import subprocess
import tkinter as tk


class Installer:
    """
    Summary
    The Installer class is responsible for checking and installing missing dependencies for a Python application.
    Example Usage
    installer = Installer()
    The above code creates an instance of the Installer class, which checks for missing dependencies by reading the requirements.txt file. If any dependencies are missing, a message is displayed. The user can then choose to install the missing dependencies by clicking the "Install" button. If all dependencies are already installed, a message indicating this is displayed. The user can cancel the installation process by clicking the "Cancel" button.
    Code Analysis
    Main functionalities
    Checking for missing dependencies by reading the requirements.txt file.
    Displaying a message indicating the missing dependencies, if any.
    Allowing the user to install the missing dependencies.
    Displaying a message indicating that all dependencies are already installed.
    Starting the main application after the installation process.

    Methods
    __init__(self): Initializes the Installer class by creating the main window and setting up the buttons, label, and event handlers.
    check_for_dependencies(self) -> bool: Reads the requirements.txt file and checks for missing dependencies. Returns True if all dependencies are already installed, and False otherwise.
    install(self): Installs the missing dependencies using the pip command and starts the main application.
    start_game(self): Destroys the main window and starts the main application.

    Fields
    root: The main window of the application.
    message: The message to be displayed to the user.
    install_button: The button for installing the missing dependencies.
    cancel_button: The button for canceling the installation process.
    missing_dependencies: The list of missing dependencies.

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

    def check_for_dependencies(self) -> bool:
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
