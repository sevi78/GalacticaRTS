import subprocess
import tkinter as tk


class Installer:
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
