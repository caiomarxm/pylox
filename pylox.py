import sys
import os

from lox.lexer import Lexer


class PyLox:
    def __init__(self) -> None:
        self._had_error = False


    def start(self):
        """
        Starts the interpreter reading args fro sys.argv
        """
        if len(sys.argv) > 2:
            print("Usage: pylox [script]")
            return 64
        elif len(sys.argv) == 2:
            return self.run_file(sys.argv[1])
        else:
            return self.run_prompt()


    def run_file(self, file_path:str) -> int:
        # Correcting file path if is relative
        file_path = self.get_absolute_file_path(file_path)

        with open(file_path) as file:
            source = file.buffer.read()
            print(source)
            self.run(source)

            if self._had_error:
                return 65
        return 64


    # Defines the REPL
    def run_prompt(self) -> int:
        while True:
            try:
                line = input("> ")
                self.run(line)
                self._had_error = False
            except EOFError as error:
                # Adding a newline to prompt
                print()
                break
        return 0


    def run(self, source:str) -> None:
        lexer = Lexer(source, self.error)
        tokens = lexer.scan_tokens()

        for token in tokens:
            print(token)


    def get_absolute_file_path(self, file_name:str) -> str:
        """
        Returns the absolute path to the given file

        Args:
            file_name (str): string containing the relative or absolute lox file to run
            :param file_loc: str

        Returns: 
            str: the absolute file path
        """
        if file_name[0] == '/':
            return file_name
        return f"{os.getcwd()}/{file_name}"


    def error(self, line:int, message:str) -> None:
        self.report(line, "", message)


    def report(self, line:int, where:str, message:str):
        print(f"[line '{line}'] Error{where}: {message}")
        self._had_error = True



if __name__ == "__main__":
    code = PyLox().start()
    print(f"Process ended with code {code}")
