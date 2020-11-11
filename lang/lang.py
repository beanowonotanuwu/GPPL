### IMPORTS                                     ###
from enum import Enum
from typing import  (
    AnyStr,
    Any
)

from sys import exit as exit_
### IMPORTS                                     ###
### TOKENU                                      ###
class Token(object):
    """
    Token class for Token Types (Token.TT) and creating Token objects
    """
    class TT(Enum):
        """
        Token Type class containing sub classes (enums to be more percise)
        """
        EOF = -1
        NEWLINE = 0
        NUMBER = 1
        IDENT = 2
        STRING = 3
        ## Keywords                                 ##
        prt = 101
        inp = 102
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
    def skip_comment(self): pass
    def mk(self, tt: Token) -> Token: """
    For making tokens
    """; return Token(tt.name, self.char)
    ## Utility                                      ##    
    @property
    def token(self) -> Token:
        token = None
        self.skip_whitespace()
        self.skip_comment()

        if self.char    == '+' : token = self.mk(Token.TT.PLUS)
        elif self.char  == '-' : token = self.mk(Token.TT.MINUS)
        elif self.char  == '*' : token = self.mk(Token.TT.MUL)
        elif self.char  == '/' :
            # check for int div
            token = self.mk(Token.TT.DIV)
        elif self.char  == '^' : token = self.mk(Token.TT.POW)
        elif self.char  == '%' : token = self.mk(Token.TT.MOD)
        elif self.char  == '~' : token = self.mk(Token.TT.ROOT)
        elif self.char  == '=' :
            if self.peek() == '=':
                last = self.char
                self.next()
                token = Token(last + self.char, Token.TT.BEQ)
            else: token = Token(self.char, Token.TT.EQ)
        elif self.char  == '\n': token = self.mk(Token.TT.NEWLINE)
        elif self.char  == '\0': token = Token(Token.TT.EOF)
        else: self.abort(f'UnknownTokenError: {self.char}')

        self.next()
        return token
### LEXER                                       ###
