### IMPORTS                                     ###
from enum import Enum
from pdb import set_trace
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
        STRING = 2
        CHAR = 3
        BOOLEAN = 4
        IDENT = 5
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
    
    @staticmethod
    def check_keyword(val):
        for tt in Token.TT:
            if (tt.name == val) and (200 > tt.value >= 100): return tt
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
    """; return Token(tt.name, self.char)
    ## Utility                                      ##    
    @property
    def token(self) -> Token:
        self.skip_whitespace()
        self.skip_comment()
        token = None

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
                token = Token(Token.TT.BEQ, last + self.char)
            else: token = self.mk(Token.TT.EQ)
        elif self.char  == '>' :
            if self.peek() == '=':
                last = self.char
                self.next()
                token = Token(Token.TT.GTE, last + self.char)
            else: token = self.mk(Token.TT.GT)
        elif self.char  == '<' :
            if self.peek() == '=':
                last = self.char
                self.next()
                token = Token(Token.TT.LTE, last + self.char)
            else: token = self.mk(Token.TT.LT)
        elif self.char  == '!' :
            if self.peek() == '=':
                last = self.char
                self.next()
                token = Token(Token.TT.NOTBEQ, last + self.char)
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
            token = Token(Token.TT.STRING, val)
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
            token = Token(Token.TT.NUMBER, val)
        elif self.char.isalpha():
            start = self.pos
            while self.peek().isalnum(): self.next()

            val = self.src[start : self.pos + 1]
            kw = Token.check_keyword(val)
            token = Token(Token.TT.IDENT if kw == None else kw, val)
        elif self.char  == '\n': token = Token(Token.TT.NEWLINE)
        elif self.char  == '\0': token = Token(Token.TT.EOF)
        else: self.abort(f'UnknownTokenError: {self.char}')

        self.next()
        return token
### LEXER                                       ###
