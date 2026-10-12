class LexicalError(Exception):
    pass

class ParsingError(Exception):
    pass

class TokenType:
    INTEGER = "INTEGER"
    PLUS = "PLUS"
    MINUS = "MINUS"
    MUL = "MUL"
    DIV = "DIV"
    LPAREN = "LPAREN"
    RPAREN = "RPAREN"
    EOF = "EOF"  # кінець вхідного рядка

class Token:
    def __init__(self, type, value):
        self.type = type
        self.value = value

    def __str__(self):
        return f"Token({self.type}, {repr(self.value)})"

class Lexer:
    def __init__(self, text):
        self.text = text
        self.pos = 0
        self.current_char = self.text[self.pos] if self.text else None

    def advance(self):
        # Переміщуємо 'вказівник' на наступний символ вхідного рядка
        self.pos += 1
        if self.pos > len(self.text) - 1:
            self.current_char = None  # кінець введення
        else:
            self.current_char = self.text[self.pos]

    def skip_whitespace(self):
        # Пропускаємо пробільні символи
        while self.current_char is not None and self.current_char.isspace():
            self.advance()

    def integer(self):
        # Повертаємо ціле число, зібране з послідовності цифр
        result = ""
        while self.current_char is not None and self.current_char.isdigit():
            result += self.current_char
            self.advance()
        return int(result)

    def get_next_token(self):
        # Лексичний аналізатор, що розбиває вхідний рядок на токени
        while self.current_char is not None:
            if self.current_char.isspace():
                self.skip_whitespace()
                continue

            if self.current_char.isdigit():
                return Token(TokenType.INTEGER, self.integer())

            if self.current_char == "+":
                self.advance()
                return Token(TokenType.PLUS, "+")

            if self.current_char == "-":
                self.advance()
                return Token(TokenType.MINUS, "-")

            if self.current_char == "*":
                self.advance()
                return Token(TokenType.MUL, "*")

            if self.current_char == "/":
                self.advance()
                return Token(TokenType.DIV, "/")

            if self.current_char == "(":
                self.advance()
                return Token(TokenType.LPAREN, "(")

            if self.current_char == ")":
                self.advance()
                return Token(TokenType.RPAREN, ")")

            raise LexicalError("Помилка лексичного аналізу")

        return Token(TokenType.EOF, None)

class AST:
    pass

class BinOp(AST):
    def __init__(self, left, op, right):
        self.left = left
        self.op = op
        self.right = right

class Num(AST):
    def __init__(self, token):
        self.token = token
        self.value = token.value

class Parser:
    def __init__(self, lexer):
        self.lexer = lexer
        self.current_token = self.lexer.get_next_token()

    def error(self):
        raise ParsingError("Помилка синтаксичного аналізу")

    def eat(self, token_type):
        # Порівнюємо поточний токен з очікуваним токеном
        if self.current_token.type == token_type:
            self.current_token = self.lexer.get_next_token()
        else:
            self.error()

    def factor(self):
        # Парсер для 'factor': ціле число або вираз у дужках
        token = self.current_token
        if token.type == TokenType.INTEGER:
            self.eat(TokenType.INTEGER)
            return Num(token)
        elif token.type == TokenType.LPAREN:
            self.eat(TokenType.LPAREN)
            node = self.expr()
            self.eat(TokenType.RPAREN)
            return node
        self.error()

    def term(self):
        # Парсер для 'term': множення та ділення (вищий пріоритет)
        node = self.factor()

        while self.current_token.type in (TokenType.MUL, TokenType.DIV):
            token = self.current_token
            if token.type == TokenType.MUL:
                self.eat(TokenType.MUL)
            elif token.type == TokenType.DIV:
                self.eat(TokenType.DIV)

            node = BinOp(left=node, op=token, right=self.factor())

        return node

    def parse(self):
        # Розбирає весь вхідний рядок і перевіряє, що після виразу нічого не лишилось
        node = self.expr()
        if self.current_token.type != TokenType.EOF:
            self.error()
        return node

    def expr(self):
        # Парсер для арифметичних виразів: додавання та віднімання (нижчий пріоритет)
        node = self.term()

        while self.current_token.type in (TokenType.PLUS, TokenType.MINUS):
            token = self.current_token
            if token.type == TokenType.PLUS:
                self.eat(TokenType.PLUS)
            elif token.type == TokenType.MINUS:
                self.eat(TokenType.MINUS)

            node = BinOp(left=node, op=token, right=self.term())

        return node

def print_ast(node, level=0):
    indent = "  " * level
    if isinstance(node, Num):
        print(f"{indent}Num({node.value})")
    elif isinstance(node, BinOp):
        print(f"{indent}BinOp:")
        print(f"{indent}  left: ")
        print_ast(node.left, level + 2)
        print(f"{indent}  op: {node.op.type}")
        print(f"{indent}  right: ")
        print_ast(node.right, level + 2)
    else:
        print(f"{indent}Unknown node type: {type(node)}")

class Interpreter:
    def __init__(self, parser):
        self.parser = parser

    def visit_BinOp(self, node):
        if node.op.type == TokenType.PLUS:
            return self.visit(node.left) + self.visit(node.right)
        elif node.op.type == TokenType.MINUS:
            return self.visit(node.left) - self.visit(node.right)
        elif node.op.type == TokenType.MUL:
            return self.visit(node.left) * self.visit(node.right)
        elif node.op.type == TokenType.DIV:
            right = self.visit(node.right)
            if right == 0:
                raise ZeroDivisionError("Помилка: ділення на нуль")
            return self.visit(node.left) / right

    def visit_Num(self, node):
        return node.value

    def interpret(self):
        tree = self.parser.parse()
        return self.visit(tree)

    def visit(self, node):
        method_name = "visit_" + type(node).__name__
        visitor = getattr(self, method_name, self.generic_visit)
        return visitor(node)

    def generic_visit(self, node):
        raise Exception(f"Немає методу visit_{type(node).__name__}")

def main():
    while True:
        try:
            text = input('Введіть вираз (або "exit" для виходу): ')
            if text.lower() == "exit":
                print("Вихід із програми.")
                break
            lexer = Lexer(text)
            parser = Parser(lexer)
            interpreter = Interpreter(parser)
            result = interpreter.interpret()
            print(result)
        except Exception as e:
            print(e)


if __name__ == "__main__":
    main()

# в консолі перевірка роботи програми
'''
    Введіть вираз (або "exit" для виходу): (2 + 3) * 4
    20
    Введіть вираз (або "exit" для виходу): 2 + 3 * 4
    14
    Введіть вираз (або "exit" для виходу): 10 / 4
    2.5
    Введіть вираз (або "exit" для виходу): 8 - 2 * (3 + 1)
    0
    Введіть вираз (або "exit" для виходу): ((1 + 2) * (3 + 4)) / 7
    3.0
    Введіть вираз (або "exit" для виходу): 2 * (3 + 4
    Помилка синтаксичного аналізу
    Введіть вираз (або "exit" для виходу): 5 / 0
    Помилка: ділення на нуль
    Введіть вираз (або "exit" для виходу): exit
    Вихід із програми.
'''