import subprocess
import sys


class AbstractEnvUpdater:

    def install(self, package: str):
        raise ValueError("must be implemented by subclass")

    @staticmethod
    def check_installed(name: str):
        try:
            subprocess.check_call([sys.executable, "-m", "pip", "show", "-q", name])
            print("package is installed")
        except Exception as e:
            print(f"Exception show package {e}")

    @staticmethod
    def uninstall(name: str):
        try:
            subprocess.check_call([sys.executable, "-m", "pip", "uninstall", "-y", name])
            print("package uninstalled")
        except Exception as e:
            print(f"Exception installing package {e}")


class GitHubEnvUpdater(AbstractEnvUpdater):
    def __init__(
            self,
            gitrepo: str,
    ):
        """
        Updates virtual environment from a remote git repository
        :param gitrepo: the remote git repository
        """
        self.gitrepo = gitrepo

    def install(self, subdir: str):
        import json

        if self.gitrepo == "" or subdir == "":
            raise ValueError("git repo and subdir cannot be empty strings")
        try:
            command = [sys.executable, "-m", "pip", "install", "--exists-action", "i", self.gitrepo + "#subdirectory=" + subdir]
            result = subprocess.check_call(command)
            [sys.executable, "-m", "pip", "install", "--importlib.invalidate_caches()", "i", self.gitrepo + "#subdirectory=" + subdir]

            print(f"package  is installed")
        except Exception  as e:
            print(f"Command '{command}' returned non-zero exit status {e.returncode}")
            print(f"Exception installing package {e}")


class LocalRepositoryEnvUpdater(AbstractEnvUpdater):
    def __init__(
            self,
            gitrepo: str,
    ):
        """
        Updates virtual environment from a local git repository
        :param gitrepo: the local git repository
        """
        self.gitrepo = gitrepo

    def install(self, subdir: str):
        if self.gitrepo == "" or subdir == "":
            raise ValueError("git repo and subdir cannot be empty strings")
        try:
            subprocess.check_call([sys.executable, "-m", "pip", "install", "-e", self.gitrepo + subdir])
            print("package installed")
        except Exception as e:
            print(f"Exception installing package {e}")
