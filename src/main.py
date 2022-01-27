import sys
from scanner import Scanner
from lox_parser import Parser
from interpreter import Interpreter
from resolver import Resolver


def read_in_file(file_name: str) -> str:
    with open(file_name) as file:
        return file.read()


def print_error(err: str):
    print(f"\033[91m{err}\033[0m")


def main(argv: list):
    if len(argv) != 2:
        print("File not provided")
        return

    source_code = read_in_file(argv[1])
    scanner = Scanner(source_code)
    scanner_result = scanner.scan_tokens()

    if scanner_result.failure:
        print_error("Scanner failed!")
        for err in scanner_result.error:
            print(err.message)
        return

    parser = Parser(scanner_result.value)
    parser_result = parser.parse()

    if parser_result.failure:
        print_error("Parser failed!")
        for err in parser_result.error:
            print(err.message)
        return

    try:
        interpreter = Interpreter()
        resolver = Resolver(interpreter)
        resolver._resolve_stmts(parser_result.value)
        interpreter.interpret(parser_result.value)
    except Exception as err:
        print(err)


if __name__ == "__main__":
    main(sys.argv)
