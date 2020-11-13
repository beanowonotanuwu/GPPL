### IMPORTS                                     ###
from enum import Enum
from pdb import set_trace
from typing import  (
    AnyStr,
    Any
)
from warnings import filterwarnings
from easyyaml import load
from yaml import YAMLLoadWarning
from lang.util import cd_back
from sys import exit as exit_
### IMPORTS                                     ###
filterwarnings("ignore", category=YAMLLoadWarning)
### LOADINGS                                    ###
# set_trace()
with cd_back(r'lang\info') as _:
    keywords = load(r'kws.enum.yml')
### LOADINGS                                    ###
### TOKENU                                      ###
class Token(object):
    EOF = 'EOF'
    NEWLINE = 'NEWLINE'
    NUMBER = 'NUMBER'
    STRING = 'STRING'
    CHAR = 'CHAR'
    BOOLEAN = 'BOOLEAN'
    IDENT = 'IDENT'
    ## Keywords                                 ##
    KEYWORDS = [v for v in keywords.values()]
    ## Keywords                                 ##
    ## Symbols                                  ##
    LPAREN = 'LPAREN'
    RPAREN = 'RPAREN'
    ## Symbols                                  ##
    ## Operators                                ##
    EQ = 'EQ'
    PLUS = 'PLUS'
    MINUS = 'MINUS'
    MUL = 'MUL'
    DIV = 'DIV'
    INT_DIV = 'INT_DIV'
    POW = 'POW'
    MOD = 'MOD'
    ROOT = 'ROOT'
    BEQ = 'BEQ'
    NOTBEQ = 'NOTBEQ'
    LT = 'LT'
    LTE = 'LTE'
    GT = 'GT'
    GTE = 'GTE'
    ## Operators                                ##

    def __init__(self, tt, val: AnyStr or None=None): self.tt, self.val = tt, val
    def __repr__(self): return f'{self.tt}' + (f':{self.val}' if self.val else '')

    @classmethod
    def matches(cls, token_a, token_b): """
    Classmethod to see if the provided token matches the desired token
    """; return (token_a.tt == token_b.tt) and (token_a.val == token_b.val)
    
    @staticmethod
    def check_keyword(val):
        for tt in Token.KEYWORDS:
            if val == tt: return tt
        return None
### TOKENU                                      ###
### LEXER                                       ###
class Lexer(object):
    ## Dunder                                       ##
    def __init__(self, src: AnyStr):
        self.src = src + '\n'
        self.char = ''
        self.pos = -1
        self.next()
    ## Dunder                                       ##
    ## Utility                                      ##
    def next(self) -> None:
        self.pos += 1
        self.char = '\0' if self.pos >= len(self.src) else self.src[self.pos]
    def peek(self) -> str: return '\0' if self.pos + 1 >= len(
        self.src
    ) else self.src[self.pos + 1]
    def abort(self, msg: AnyStr): exit_(
        f'LexingError -> {msg}'
    )
    def skip_whitespace(self) -> None:
        while self.char in (' ', '\t' '\r'): self.next()
    def skip_comment(self):
        if self.char == '#':
            while self.char != '\n': self.next()
    def mk(self, tt: Token) -> Token: """
    For making tokens
    """; return Token(tt, self.char)
    ## Utility                                      ##    
    @property
    def token(self) -> Token:
        self.skip_whitespace()
        self.skip_comment()
        token = None

        if self.char    == '+' : token = self.mk(Token.PLUS)
        elif self.char  == '-' : token = self.mk(Token.MINUS)
        elif self.char  == '*' : token = self.mk(Token.MUL)
        elif self.char  == '/' :
            # check for int div
            token = self.mk(Token.DIV)
        elif self.char  == '^' : token = self.mk(Token.POW)
        elif self.char  == '%' : token = self.mk(Token.MOD)
        elif self.char  == '~' : token = self.mk(Token.ROOT)
        elif self.char  == '=' :
            if self.peek() == '=':
                last = self.char
                self.next()
                token = Token(Token.BEQ, last + self.char)
            else: token = self.mk(Token.EQ)
        elif self.char  == '>' :
            if self.peek() == '=':
                last = self.char
                self.next()
                token = Token(Token.GTE, last + self.char)
            else: token = self.mk(Token.GT)
        elif self.char  == '<' :
            if self.peek() == '=':
                last = self.char
                self.next()
                token = Token(Token.LTE, last + self.char)
            else: token = self.mk(Token.LT)
        elif self.char  == '!' :
            if self.peek() == '=':
                last = self.char
                self.next()
                token = Token(Token.NOTBEQ, last + self.char)
            else: self.abort(f"InvalidTokenError: {self.char}")
        elif self.char  == '"' :
            self.next()
            start = self.pos

            while self.char != '"':
                if self.char in ('\r', '\n', '\t', '\\', '%'):
                    self.abort(f"StringError: {self.char} is an illegal character inside a string")
                self.next()
            #set_trace()
            val = self.src[start : self.pos]
            token = Token(Token.STRING, val)
        elif self.char.isdigit():
            start = self.pos
            while self.peek().isdigit(): self.next()
            if self.peek() == '.':
                self.next()

                if not self.peek().isdigit():
                    self.abort(
                        f"IllegalCharacterError: {self.char}"
                    )
                while self.peek().isdigit(): self.next()

            val = self.src[start : self.pos + 1]
            token = Token(Token.NUMBER, val)
        elif self.char.isalpha():
            start = self.pos
            while self.peek().isalnum(): self.next()

            val = self.src[start : self.pos + 1]
            kw = Token.check_keyword(val)
            token = Token(Token.IDENT if kw == None else kw, val)
        elif self.char  == '(' : token = self.mk(Token.LPAREN)
        elif self.char  == ')' : token = self.mk(Token.RPAREN)
        elif self.char  == '\n': token = Token(Token.NEWLINE)
        elif self.char  == '\0': token = Token(Token.EOF)
        else: self.abort(f'UnknownTokenError: {self.char}')

        self.next()
        return token
### LEXER                                       ###
### PARSER                                      ###
class Parser(object):
    def __init__(self, lexer: Lexer, emitter):
        self.lexer = lexer
        self.emitter = emitter

        self.symbols = set()

        self.ctok = None
        self.ptok = None
        self.next()
        self.next()
    def check_token(self, tt): """
    Return true if the current token matches
    """; return tt == self.ctok.tt
    def check_tokens(self, tts: list): """
    Returns true if the current token matches any tokens in the list
    """; return self.ctok.tt in tts
    def check_peek(self, tt): """
    Return true if the next token matches
    """; return tt == self.ptok.tt
    def match(self, tt):
        """ Try to match current token. If not, error. Advances the current token """
        if not self.check_token(tt): self.abort(
            f"Expected {tt}, got {self.ctok.tt}"
        )
        self.next()
    def next(self):
        """Advances the current token"""
        self.ctok = self.ptok
        self.ptok = self.lexer.token
    def abort(self, message): exit_(f"ParsingError -> {message}")
    
    def is_comparison_op(self): return self.check_tokens([
        Token.GT, Token.GTE,
        Token.LT, Token.LTE,
        Token.BEQ, Token.NOTBEQ
        ]
    )

    def program(self):

        while self.check_token(Token.NEWLINE): self.next()

        while not self.check_token(Token.EOF): self.statement()

    def statement(self):
        if self.check_token(keywords['print']):
            self.next()

            if self.check_token(Token.STRING):
                self.emitter.emit_line(
                    f'print("{self.ctok.val}")'
                )
                self.next()
            else:
                self.emitter.emit_line(
                    f'print("{self.expression}")'
                )
            
        elif self.check_token(keywords['if']):
            print("STATEMENT-IF")
            self.next()
            self.comparison()

            self.match(Token.LPAREN)
            self.nl()
            
            while not self.check_token(Token.RPAREN): self.statement()
            self.match(Token.RPAREN)

        elif self.check_token(keywords['while']):
            print("STATEMENT-WHILE")
            self.next()
            self.comparison()
            
            self.match(Token.LPAREN)
            self.nl()

            while not self.check_token(Token.RPAREN): self.statement()

            self.match(Token.RPAREN)

        elif self.check_token(keywords['let']):
            print("STATEMENT-LET")
            self.next()
            if self.ctok.val not in self.symbols:
                self.symbols.add(self.ctok.val)
            self.match(Token.IDENT)
            self.match(Token.EQ)

            self.expression()

        elif self.check_token(keywords['input']):
            print("STATEMENT-INPUT")
            self.next()
            if self.ctok.val not in self.symbols:
                self.symbols.add(self.ctok.val)
            
            self.match(Token.IDENT)

        else: self.abort(f"InvalidStatement: {self.ctok.val} ({self.ctok.tt})")
        self.nl()

    def comparison(self):
        print("COMPARISON")

        self.expression()

        if self.is_comparison_op():
            self.next()
            self.expression()
        else: self.abort(
            f"Expected comparison operator at: {self.ctok.val}"
        )

        while self.is_comparison_op():
            self.next()
            self.expression()

    def expression(self):
        print("EXPRESSION")

        self.term()

        while self.check_tokens([Token.PLUS, Token.MINUS]):
            self.next()
            self.term()

    def term(self):
        print("TERM")

        self.unary()

        while self.check_tokens([Token.MUL, Token.DIV]):
            self.next()
            self.unary()

    def unary(self):
        print("UNARY")

        if self.check_tokens([Token.PLUS, Token.MINUS]): self.next()

        self.primary()

    def primary(self):
        print(f"PRIMARY ({self.ctok.val})")

        if self.check_token(Token.NUMBER): self.next()
        elif self.check_token(Token.IDENT):
            if self.ctok.val not in self.symbols:
                self.abort(
                    f"Referencing variable before assignment, {self.ctok.val}"
                )
            self.next()
        else: self.abort(
            f"UnexpectedTokenError: {self.ctok.val}"
        )

    def nl(self):
        print("NEWLINE")
        self.match(Token.NEWLINE)
        while self.check_token(Token.NEWLINE): self.next()
### PARSER                                      ###
### EMITTER                                     ###
class Emitter(object):
    def __init__(self, path: str):
        self.path = path
        self.code = ""

    def emit(self, code): self.code += code

    def emit_line(self, code): self.emit(
        code + '\n'
    )

    def write(self):
        with open(self.path, 'w') as out:out.write(self.code)

### EMITTER                                     ###