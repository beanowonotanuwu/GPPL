### IMPORTS                             ###
import lang
### IMPORTS                             ###
if __name__ == "__main__":
    while True:
        src = input('>>> ')
        lexer = lang.lang.Lexer(src)
        tok = lexer.token
        while tok.tt != lang.lang.Token.EOF:
            print(tok)
            tok = lexer.token