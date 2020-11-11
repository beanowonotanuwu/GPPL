### IMPORTS                             ###
import lang
### IMPORTS                             ###
if __name__ == "__main__":
    src = input('>>> ')
    lexer = lang.lang.Lexer(src)

    tok = lexer.token
    while tok.tt != lang.lang.Token.TT.EOF:
        print(tok)
        tok = lexer.token