import sys
import lang.lang as lang
import pdb
if __name__ == "__main__":
    if len(sys.argv) < 2:
        sys.exit(
            "CompilerError: Needs source file arg"
        )
    # pdb.set_trace()
    with open(sys.argv[1], 'r') as io: src = io.read()

    lexer = lang.Lexer(src)
    parser = lang.Parser(lexer)

    parser.program()
    print("Parsing completed")