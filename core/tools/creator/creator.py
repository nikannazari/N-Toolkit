"""
creator.py - Core logic of Creator
"""

import os
import json
from pprint import pprint
from pathlib import Path
import subprocess
import venv
import shlex
from colorama import Fore , Style

from src.services.custom_input import CustomInput

TOOL_DIR = os.path.dirname(os.path.abspath(__file__))
PROJECT_ROOT = os.path.abspath(os.path.join(TOOL_DIR, "..", "..", ".."))

# ===========================================
# Terminal Color
# ===========================================

def info(msg):  print(f"{Fore.CYAN}{msg}{Style.RESET_ALL}")
def ok(msg):    print(f"{Fore.GREEN}✔ {msg}{Style.RESET_ALL}")
def warn(msg):  print(f"{Fore.YELLOW}⚡ {msg}{Style.RESET_ALL}")
def err(msg):   print(f"{Fore.RED}✘ {msg}{Style.RESET_ALL}")
def ok_2(msg): print(f"{Fore.GREEN}{msg}{Style.RESET_ALL}")
def warn_2(msg): print(f"{Fore.YELLOW}{msg}{Style.RESET_ALL}")
def err_2(msg): print(f"{Fore.RED}{msg}{Style.RESET_ALL}")


# ===========================================
# Main Tool Functions
# ===========================================


class Creator:

    def __init__(self, directory) -> None:
        self.directory = Path(directory).expanduser()

    # ==============================
    # Input Handler
    # ==============================

    def python_input(self):
        project_name = input(
            f"{Fore.CYAN}Enter your project directory name : {Style.RESET_ALL}"
        ).strip()

        return project_name

    # ==============================
    # Virtual Environment
    # ==============================

    def create_venv(self, project_path):
        venv_path = project_path / ".venv"

        if venv_path.exists():
            warn(f"Virtual environment already exists: {venv_path}")
            return venv_path

        venv.create(venv_path, with_pip=True)

        ok(f"Virtual environment created: {venv_path}")

        return venv_path

    # ==============================
    # Python Project
    # ==============================

    def python(self):

        project_name = self.python_input()

        # Create workspace directory
        self.directory.mkdir(parents=True, exist_ok=True)

        project_path = self.directory / project_name

        if project_path.exists():
            err(f"Project already exists: {project_path}")
            return

        # Create project directories
        (project_path / "src").mkdir(parents=True)

        # Create project files
        files = {
            "main.py": '''def main():
    print("Hello, World!")


if __name__ == "__main__":
    main()
''',

            "src/__init__.py": "",

            "requirements.txt": "",

            "README.md": f"# {project_name}\n\nA Python project.\n",

            ".gitignore": '''__pycache__/
*.py[cod]
.venv/
venv/
.env
.pytest_cache/
.idea/
.vscode/
'''
        }

        for filename, content in files.items():
            file_path = project_path / filename
            file_path.write_text(content, encoding="utf-8")

        # Create virtual environment
        self.create_venv(project_path)

        ok(f"Project created successfully: {project_path}")

        return project_path

    # ==============================
    # Django Server Runner
    # ==============================

    def run_django(self, project_path):

        python = project_path / ".venv/bin/python"

        process = subprocess.Popen(
            [str(python), "manage.py", "runserver"],
            cwd=project_path
        )

        info("Django server is running.")
        warn_2("Type 'q', 'quit', or 'exit' to stop the server.")

        while True:
            user_input = input("> ").strip().lower()

            if user_input in ["q", "quit", "exit"]:
                process.terminate()
                process.wait()
                ok("Django server stopped.")
                break

            elif process.poll() is not None:
                warn("Django server has already stopped.")
                break

            else:
                warn_2("Unknown command. Type q, quit, or exit to stop.")

    # ==============================
    # Django Project
    # ==============================

    def django(self, project_name="DjangoProject"):

        project_name = self.python_input()

        # Create workspace directory
        self.directory.mkdir(parents=True, exist_ok=True)

        project_path = self.directory / project_name

        if project_path.exists():
            err(f"Project already exists: {project_path}")
            return

        # Create project directory
        project_path.mkdir(parents=True)

        # Create virtual environment
        self.create_venv(project_path)

        python = project_path / ".venv/bin/python"

        # Install Django
        try:
            subprocess.run(
                [str(python), "-m", "pip", "install", "django"],
                check=True
            )

        except subprocess.CalledProcessError:
            err("Django installation failed.")
            return

        # Generate Django project
        try:
            subprocess.run(
                [
                    str(python),
                    "-m",
                    "django",
                    "startproject",
                    project_name,
                    str(project_path)
                ],
                check=True
            )

        except subprocess.CalledProcessError:
            err("Django project creation failed.")
            return

        # Create additional files
        files = {
            "requirements.txt": "Django\n",

            "README.md": (
                f"# {project_name}\n\n"
                "A Django web application.\n\n"
                "## Run\n\n"
                "```bash\n"
                "python manage.py runserver\n"
                "```\n"
            ),

            ".gitignore": '''__pycache__/
*.py[cod]
.venv/
venv/
.env
db.sqlite3
staticfiles/
.idea/
.vscode/
'''
        }

        for filename, content in files.items():
            file_path = project_path / filename
            file_path.write_text(content, encoding="utf-8")

        ok(f"Django project created: {project_path}")

        # Ask to run server
        warn_2("Do you want to run it? [y/n]")
        user_input = input("> ").strip().lower()

        if user_input in ["y", "yes"]:
            self.run_django(project_path)

        elif user_input in ["n", "no"]:
            info("Skipping server startup.")

        else:
            err("Invalid command.")

        return project_path

    def flask(self):
        project_name = self.python_input()

        self.directory.mkdir(parents=True, exist_ok=True)
        project_path = self.directory / project_name

        if project_path.exists():
            err(f"Project already exists: {project_path}")
            return

        project_path.mkdir(parents=True)

        self.create_venv(project_path)
        python = project_path / ".venv/bin/python"

        subprocess.run(
            [str(python), "-m", "pip", "install", "flask"],
            check=True
        )

        files = {
            "app.py": '''from flask import Flask

app = Flask(__name__)

@app.route("/")
def home():
    return "Hello, Flask!"

if __name__ == "__main__":
    app.run(debug=True)
    ''',

            "requirements.txt": "flask\n",

            "README.md": f"# {project_name}\n\nA Flask project.\n",

            ".gitignore": '''__pycache__/
    *.py[cod]
    .venv/
    venv/
    .env
    .pytest_cache/
    .idea/
    .vscode/
    '''
        }

        for filename, content in files.items():
            (project_path / filename).write_text(content, encoding="utf-8")

        ok(f"Flask project created: {project_path}")

        run = input(f"{Fore.CYAN}Run Flask project? (y/n): {Style.RESET_ALL}").strip().lower()

        if run == "y":
            subprocess.Popen([str(python), "app.py"], cwd=project_path)


    def fastapi(self):
        project_name = self.python_input()

        self.directory.mkdir(parents=True, exist_ok=True)
        project_path = self.directory / project_name

        if project_path.exists():
            err(f"Project already exists: {project_path}")
            return

        project_path.mkdir(parents=True)

        self.create_venv(project_path)
        python = project_path / ".venv/bin/python"

        subprocess.run(
            [str(python), "-m", "pip", "install", "fastapi", "uvicorn"],
            check=True
        )

        files = {
            "main.py": '''from fastapi import FastAPI

    app = FastAPI()

    @app.get("/")
    def home():
        return {"message": "Hello, FastAPI!"}

    @app.get("/health")
    def health():
        return {"status": "ok"}
    ''',

            "requirements.txt": "fastapi\nuvicorn\n",

            "README.md": f"# {project_name}\n\nA FastAPI project.\n",

            ".gitignore": '''__pycache__/
    *.py[cod]
    .venv/
    venv/
    .env
    .pytest_cache/
    .idea/
    .vscode/
    '''
        }

        for filename, content in files.items():
            (project_path / filename).write_text(content, encoding="utf-8")

        ok(f"FastAPI project created: {project_path}")

        run = input(f"{Fore.CYAN}Run FastAPI project? (y/n): {Style.RESET_ALL}").strip().lower()

        if run == "y":
            subprocess.Popen(
                [
                    str(python),
                    "-m",
                    "uvicorn",
                    "main:app",
                    "--reload"
                ],
                cwd=project_path
            )

    def react(self):
        project_name = self.python_input()

        self.directory.mkdir(parents=True, exist_ok=True)
        project_path = self.directory / project_name

        if project_path.exists():
            err(f"Project already exists: {project_path}")
            return

        try:
            subprocess.run(
                [
                    "npm",
                    "create",
                    "vite@latest",
                    project_name,
                    "--",
                    "--template",
                    "react"
                ],
                cwd=self.directory,
                check=True
            )

            ok(f"React project created: {project_path}")

            subprocess.run(
                ["npm", "install"],
                cwd=project_path,
                check=True
            )

            ok("Dependencies installed successfully.")

            info("Starting React development server...")

            process = subprocess.Popen(
                ["npm", "run", "dev"],
                cwd=project_path
            )

            warn_2("Press Ctrl+C to stop the development server.")

            try:
                process.wait()

            except KeyboardInterrupt:
                warn("Stopping React development server...")
                process.terminate()

                try:
                    process.wait(timeout=5)
                except subprocess.TimeoutExpired:
                    process.kill()
                    process.wait()

                ok("React development server stopped.")

        except subprocess.CalledProcessError as e:
            err(f"Command failed with exit code: {e.returncode}")

        except FileNotFoundError:
            err("npm was not found. Please install Node.js and npm.")


    def vue(self):
        project_name = self.python_input()

        self.directory.mkdir(parents=True, exist_ok=True)
        project_path = self.directory / project_name

        if project_path.exists():
            err(f"Project already exists: {project_path}")
            return

        try:
            subprocess.run(
                [
                    "npm",
                    "create",
                    "vite@latest",
                    project_name,
                    "--",
                    "--template",
                    "vue"
                ],
                cwd=self.directory,
                check=True
            )

            ok(f"Vue project created: {project_path}")

            subprocess.run(
                ["npm", "install"],
                cwd=project_path,
                check=True
            )

            ok("Dependencies installed successfully.")

            info("Starting Vue development server...")

            process = subprocess.Popen(
                ["npm", "run", "dev"],
                cwd=project_path
            )

            warn_2("Press Ctrl+C to stop the development server.")

            try:
                process.wait()

            except KeyboardInterrupt:
                warn("Stopping Vue development server...")
                process.terminate()

                try:
                    process.wait(timeout=5)
                except subprocess.TimeoutExpired:
                    process.kill()
                    process.wait()

                ok("Vue development server stopped.")

        except subprocess.CalledProcessError as e:
            err(f"Command failed with exit code: {e.returncode}")

        except FileNotFoundError:
            err("npm was not found. Please install Node.js and npm.")

    def node(self):
        project_name = self.python_input()

        self.directory.mkdir(parents=True, exist_ok=True)
        project_path = self.directory / project_name

        if project_path.exists():
            err(f"Project already exists: {project_path}")
            return

        project_path.mkdir(parents=True)
        (project_path / "src").mkdir()

        files = {
            "src/index.js": '''console.log("Hello, Node.js!");
    ''',

            "package.json": f'''{{
    "name": "{project_name.lower().replace(" ", "-")}",
    "version": "1.0.0",
    "description": "A Node.js project",
    "main": "src/index.js",
    "scripts": {{
        "start": "node src/index.js"
    }}
    }}
    ''',

            "README.md": f"# {project_name}\n\nA Node.js project.\n",

            ".gitignore": '''node_modules/
    .env
    dist/
    '''
        }

        for filename, content in files.items():
            (project_path / filename).write_text(content, encoding="utf-8")

        ok(f"Node.js project created: {project_path}")

        run = input(f"{Fore.CYAN}Run Node.js project? (y/n): {Style.RESET_ALL}").strip().lower()

        if run == "y":
            subprocess.Popen(["npm", "start"], cwd=project_path)


    def rust(self):
        project_name = self.python_input()

        self.directory.mkdir(parents=True, exist_ok=True)
        project_path = self.directory / project_name

        if project_path.exists():
            err(f"Project already exists: {project_path}")
            return

        subprocess.run(
            ["cargo", "new", project_name, "--bin"],
            cwd=self.directory,
            check=True
        )

        ok(f"Rust project created: {project_path}")

        run = input(f"{Fore.CYAN}Run Rust project? (y/n): {Style.RESET_ALL}").strip().lower()

        if run == "y":
            subprocess.Popen(["cargo", "run"], cwd=project_path)


    def cpp(self):
        project_name = self.python_input()

        self.directory.mkdir(parents=True, exist_ok=True)
        project_path = self.directory / project_name

        if project_path.exists():
            err(f"Project already exists: {project_path}")
            return

        (project_path / "src").mkdir(parents=True)
        (project_path / "include").mkdir()

        files = {
            "src/main.cpp": '''#include <iostream>

    int main() {
        std::cout << "Hello, C++!" << std::endl;
        return 0;
    }
    ''',

            "CMakeLists.txt": f'''cmake_minimum_required(VERSION 3.20)

    project({project_name})

    set(CMAKE_CXX_STANDARD 17)
    set(CMAKE_CXX_STANDARD_REQUIRED ON)

    add_executable({project_name} src/main.cpp)
    ''',

            "README.md": f"# {project_name}\n\nA C++ project using CMake.\n",

            ".gitignore": '''build/
    cmake-build-*/
    '''
        }

        for filename, content in files.items():
            (project_path / filename).write_text(content, encoding="utf-8")

        ok(f"C++ project created: {project_path}")

        run = input(f"{Fore.CYAN}Build and run C++ project? (y/n): {Style.RESET_ALL}").strip().lower()

        if run == "y":
            build_path = project_path / "build"
            build_path.mkdir(exist_ok=True)

            subprocess.run(
                ["cmake", "-S", str(project_path), "-B", str(build_path)],
                check=True
            )

            subprocess.run(
                ["cmake", "--build", str(build_path)],
                check=True
            )

            subprocess.Popen(
                [str(build_path / project_name)],
                cwd=project_path
            )


    def cli(self):
        project_name = self.python_input()

        self.directory.mkdir(parents=True, exist_ok=True)
        project_path = self.directory / project_name

        if project_path.exists():
            err(f"Project already exists: {project_path}")
            return

        (project_path / "src").mkdir(parents=True)

        files = {
            "main.py": '''import argparse

def main():
    parser = argparse.ArgumentParser(
        description="CLI application"
    )

    parser.add_argument(
        "--name",
        default="World",
        help="Name to greet"
    )

    args = parser.parse_args()

    print(f"Hello, {args.name}!")

if __name__ == "__main__":
    main()
''',

            "src/__init__.py": "",

            "requirements.txt": "",

            "README.md": f"# {project_name}\n\nA Python CLI project.\n",

            ".gitignore": '''__pycache__/
    *.py[cod]
    .venv/
    venv/
    .env
    '''
        }

        for filename, content in files.items():
            (project_path / filename).write_text(content, encoding="utf-8")

        self.create_venv(project_path)
        python = project_path / ".venv/bin/python"

        ok(f"CLI project created: {project_path}")

        run = input(f"{Fore.CYAN}Run CLI project? (y/n): {Style.RESET_ALL}").strip().lower()

        if run == "y":
            subprocess.Popen([str(python), "main.py"], cwd=project_path)
        
class JsonManager:
    def create(self , json_file):
        self.workspace_name = str(json_file) + ".json"
        self.workspace_json = Path(__file__).resolve().parents[3] / "saved_data" / "creator" / self.workspace_name

        data = {
            "workspaces": []
        }

        with self.workspace_json.open("w", encoding="utf-8") as file:
            json.dump(data, file, indent=4)

        ok("json file created successfully")
    
    def delete(self , json_file):
        workspace_name = str(json_file) + ".json"
        workspace_json = Path(__file__).resolve().parents[3] / "saved_data" / "creator" / workspace_name
        
        if not workspace_json.exists():
            err("File is not exists")
            return
        creator_input = CustomInput()  
        prompt = "Are you sure? [y/n] :"
        user_input = creator_input.get_input(prompt).strip()
        if not user_input in ["Yes","yes","y","Y","No","no","N","n"]:
            err("Wrong input")
            return

        elif user_input in ["No","no","N","n"]:
            warn("Cancled")
            return

        subprocess.run([
            "rm",
            workspace_json.resolve()
        ])

        ok_2("Json file sucessfully removed")
    def list(self):
        creator_dir = Path(__file__).resolve().parents[3] / "saved_data" / "creator"

        if not creator_dir.exists():
            err("No creator directory found.")
            return

        json_files = list(creator_dir.glob("*.json"))

        if not json_files:
            err("No workspaces found.")
            return

        ok_2("Available Workspaces:")

        for index, file in enumerate(json_files, start=1):
            print(f"   {Fore.YELLOW}{index}{Fore.RED}. {Fore.CYAN}{file.stem}{Style.RESET_ALL}")
            
    def available_list(self , target_json):
        creator_dir = Path(__file__).resolve().parents[3] / "saved_data" / "creator"

        if not creator_dir.exists():
            err("No creator directory found.")
            return

        json_files = list(creator_dir.glob("*.json"))

        if not json_files:
            err("No workspaces found.")
            return
        
        is_exist = any(file.stem == target_json for file in json_files)

        if not is_exist:
            err("Json file not found")
            self.list
            return False
        
        else:
            return True

    def execute_command(self , command , args , json_file):
        Manager = WorkspaceManager(json_file)

        if command == "load":
            if len(args) != 1:
                err("Wrong usage")
                warn("   load <path to project or project name>")
                return

            path_or_name = args[0]
            Manager.load_workspace(path_or_name)

        elif command == "list":
            Manager.list_workspaces()
            
        elif command == "create":
            if len(args) != 2:
                err("Wrong usage")
                warn("   create <path> <name>")
                return

            directory = args[0]
            name = args[1]
            Manager.create_workspace(directory , name)  
            
        elif command == "delete":
            if len(args) != 1:
                err("Wrong usage")
                warn("   delete <name>")
                return
            
            name = args[0]
            Manager.delete_workspace(name)
        
        else:
            err("Command not found, please type help or ? to see available commands.")    
            
    def load(self,json_file):
        self.workspace_name = str(json_file) + ".json"
        self.workspace_json = Path(__file__).resolve().parents[3] / "saved_data" / "creator" / self.workspace_name

        creator_input = CustomInput()
    
        while True:
            try:
                prompt = f"{Fore.MAGENTA}{json_file}{Style.RESET_ALL}{Fore.YELLOW} ❯ {Style.RESET_ALL}"
                    
                user_input = creator_input.get_input(prompt).strip()
            except (EOFError, KeyboardInterrupt):
                print(f"\n{Fore.CYAN}  Returning to Tool...{Style.RESET_ALL}\n")
                return True

            if not user_input:
                continue
            
            parts = shlex.split(user_input)
            command = parts[0].lower()
            command_args = parts[1:]
            
            if command in ["exit" , "quit" , "q" , "test"]:
                print(f"\n{Fore.CYAN}  Returning to Tool...{Style.RESET_ALL}\n")
                return True
            
            if command in ["help" , "?"]:
                print(f"\n{Fore.CYAN}{Style.BRIGHT}Creator Tool Help{Style.RESET_ALL}")
                print(f"  {Fore.YELLOW}{'─' * 50}{Style.RESET_ALL}")
                
                print(f"  {Fore.MAGENTA}Json file Commands:{Style.RESET_ALL}")
                print(f"  {Fore.YELLOW}create{Style.RESET_ALL}                    Create workspaces")
                print(f"  {Fore.YELLOW}delete{Style.RESET_ALL}                    Delete workspaces")
                print(f"  {Fore.YELLOW}list{Style.RESET_ALL}                      List workspaces")
                print(f"  {Fore.YELLOW}load{Style.RESET_ALL}                      Load workspaces")
                print(f"\n  {Fore.MAGENTA}System:{Style.RESET_ALL}")
                print(f"  {Fore.YELLOW}help{Style.RESET_ALL}                      Show this help")
                print(f"  {Fore.YELLOW}clear{Style.RESET_ALL}                     Clear screen")
                print(f"  {Fore.YELLOW}exit{Style.RESET_ALL}                      Return to N-Toolkit")

                print(f"  {Fore.YELLOW}{'─' * 50}{Style.RESET_ALL}\n")
                continue
            
            if command == "clear":
                os.system("clear" if os.name == "posix" else "cls")    
                continue

            self.execute_command(command , command_args , json_file)
        
class WorkspaceManager:
    def __init__(self , json_file) -> None:
        json_file = str(json_file) + ".json"
        self.workspace_json = Path(__file__).resolve().parents[3] / "saved_data" / "creator" / json_file
        
    def create_workspace(self , directory , name):
        with self.workspace_json.open("r",encoding="utf-8") as file:
            data = json.load(file)

        directory_path = Path(directory)
        if not directory_path.exists():
            user_input = input("Directory does not exists are you sure? [y/n]: ")
            if user_input in ["n","N","No","no"]:
                warn("Cancled")
                return
        
        new_workspace = {
            "id": "ws_001",
            "name": name,
            "path": directory
        }

        data["workspaces"].append(new_workspace)

        with self.workspace_json.open("w") as file:
            json.dump(data, file, indent=4)
            
        ok("New workspace has created succesfully")
    
    def list_workspaces(self):
        with self.workspace_json.open("r", encoding="utf-8") as file:
            data = json.load(file)

        info("Workspaces : ")
        warn_2("─"*80)
        for i in data["workspaces"]:
            print(f"    {Fore.CYAN}{i["name"]}{Style.RESET_ALL} {Fore.RED}==>{Style.RESET_ALL} {Fore.YELLOW}{i["path"]}{Style.RESET_ALL}")
            
    def delete_workspace(self , name):
        with self.workspace_json.open("r",encoding="utf-8") as file:
            data = json.load(file)

        for i in data["workspaces"]:
            if i["name"] == name:
                data["workspaces"].remove(i)
                ok("Removed")
        

        with self.workspace_json.open("w") as file:
            json.dump(data, file, indent=4)

    def load_workspace(self , path_or_name):
        with self.workspace_json.open("r" ,encoding="utf-8") as file:
            data = json.load(file)
            
        workspace = {}
        for i in data["workspaces"]:
            if i["path"] == path_or_name or i["name"] == path_or_name:
                workspace = i
                break    
            
        if not workspace:
            err("Workspace not found , type list for available workspaces or type create for create a workspace")
            return

        prompt = f"{Fore.YELLOW}{workspace["name"]}{Fore.CYAN}>>>{Style.RESET_ALL} "
        creator = Creator(workspace["path"])
        creator_input = CustomInput()
        
        while True:
            try:
                user_input = creator_input.get_input(prompt).strip()
                
            except(EOFError , KeyboardInterrupt):
                print(f"\n{Fore.CYAN}  Returning to json...{Style.RESET_ALL}\n")
                return
            
            if not user_input:
                continue

            if user_input in ["exit","quit","q"]:
                print(f"\n{Fore.CYAN}  Returning to json...{Style.RESET_ALL}\n")
                break
            
            if user_input in ["help" , "?"]:
                print(f"\n{Fore.CYAN}{Style.BRIGHT}Creator Tool Help{Style.RESET_ALL}")
                print(f"  {Fore.YELLOW}{'─' * 50}{Style.RESET_ALL}")

                print(f"  {Fore.MAGENTA}Commads:{Style.RESET_ALL}")
                print(f"  {Fore.YELLOW}python{Style.RESET_ALL}                    Create a Python project")
                print(f"  {Fore.YELLOW}django{Style.RESET_ALL}                    Create a Django project")
                print(f"  {Fore.YELLOW}flask{Style.RESET_ALL}                     Create a Flask project")
                print(f"  {Fore.YELLOW}fastapi{Style.RESET_ALL}                   Create a FastAPI project")
                print(f"  {Fore.YELLOW}react{Style.RESET_ALL}                     Create a React project")
                print(f"  {Fore.YELLOW}vue{Style.RESET_ALL}                       Create a Vue project")
                print(f"  {Fore.YELLOW}node{Style.RESET_ALL}                      Create a Node.js project")
                print(f"  {Fore.YELLOW}rust{Style.RESET_ALL}                      Create a Rust project")
                print(f"  {Fore.YELLOW}cpp{Style.RESET_ALL}                       Create a C++ project")
                print(f"  {Fore.YELLOW}cli{Style.RESET_ALL}                       Create a CLI tool project")

                print(f"\n  {Fore.MAGENTA}System:{Style.RESET_ALL}")
                print(f"  {Fore.YELLOW}help{Style.RESET_ALL}                      Show this help")
                print(f"  {Fore.YELLOW}clear{Style.RESET_ALL}                     Clear screen")
                print(f"  {Fore.YELLOW}exit{Style.RESET_ALL}                      Return to N-Toolkit")

                print(f"  {Fore.YELLOW}{'─' * 50}{Style.RESET_ALL}\n")

                continue
            
            if user_input == "clear":
                os.system("clear" if os.name == "posix" else "cls")
                continue

            command = getattr(creator , user_input , None)
            
            if callable(command):
                command()

            if not callable(command):
                err("Command not found , type help or ? for see the help")
            