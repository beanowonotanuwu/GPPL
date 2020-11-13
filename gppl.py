import sys
import lang.lang as lang
if __name__ == "__main__":
    if len(sys.argv) < 2:
        sys.exit(
            "CompilerError: Needs source file arg"
        )
    with open(sys.argv[1], 'r') as io: src = io.read()

    lexer = lang.Lexer(src)
    emitter = lang.Emitter("out.py")
    parser = lang.Parser(lexer, emitter)

    parser.program()
    emitter.write()
    print("Compiling completed")