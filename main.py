class Stack():

    def __init__(self, stack:str=''):
        self.stack = list(stack)

    def is_empty(self):
        return False if len(self.stack) > 0 else True

    def push(self, item:str):
        self.stack += item

    def pop(self):
        return self.stack.pop()

    def peek(self):
        return self.stack[-1]

    def size(self):
        return len(self.stack)


def is_balanced(expression: str) -> bool:
    # Создаем экземпляр стека
    stack = Stack()
    # Словарь для соответствия открывающих и закрывающих скобок
    matching_brackets = {')': '(', '}': '{', ']': '['}

    # Перебираем каждый символ в строке
    for char in expression:
        if char in "({[":  # Если символ - открывающая скобка
            stack.push(char)
        elif char in ")}]":  # Если символ - закрывающая скобка
            if stack.is_empty() or stack.peek() != matching_brackets[char]:
                return False  # Несоответствие или пустой стек
            stack.pop()  # Удаляем соответствующую открывающую скобку

    # В конце строки стек должен быть пустым
    return stack.is_empty()

# Примеры использования
def test_stack():
    expressions = [
    "(((([{}]))))",  # Сбалансировано
    "[([])((([[[]]])))]{()}",  # Сбалансировано
    "{{[()]}}",  # Сбалансировано
    "}{}",  # Несбалансировано
    "{{[(])]}}",  # Несбалансировано
    "[[{())}]",  # Несбалансировано
    ]

    for expr in expressions:
        print(f"{expr}: {'Сбалансировано' if is_balanced(expr) else 'Несбалансировано'}")

if __name__ == '__main__':

    test_stack()
