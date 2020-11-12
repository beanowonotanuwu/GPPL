### IMPORTS                                     ###
from enum import Enum
from pdb import set_trace
from typing import  (
    AnyStr,
    Any
)
from easyyaml import load
from lang.util import cd_back
from sys import exit as exit_
### IMPORTS                                     ###
### LOADINGS                                    ###
# set_trace()
with cd_back(r'lang\info') as _:
    keywords = load(r'kws.enum.yml')
### LOADINGS                                    ###
### TOKENU                                      ###
class Token(object):
    EOF = -1
    NEWLINE = 0
    NUMBER = 1
    STRING = 2
    CHAR = 3
    BOOLEAN = 4
    IDENT = 5
    ## Keywords                                 ##
    KEYWORDS = [v for v in keywords.values()]
    ## Keywords                                 ##
    ## Operators                                ##
    EQ = 201  
    PLUS = 202
    MINUS = 203
    MUL = 204
    DIV = 205
    INT_DIV = 206
    POW = 207
    MOD = 208
    ROOT = 209
    BEQ = 210
    NOTBEQ = 211
    LT = 212
    LTE = 213
    GT = 214
    GTE = 215
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
    """; return Token(name, self.char)
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
        elif self.char  == '\n': token = Token(Token.NEWLINE)
        elif self.char  == '\0': token = Token(Token.EOF)
        else: self.abort(f'UnknownTokenError: {self.char}')

        self.next()
        return token
### LEXER                                       ###
