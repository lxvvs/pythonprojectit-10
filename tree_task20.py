class Node:
    def __init__(self, t, v, l=None, r=None):
        self.type = t   # 'op', 'val', 'var'
        self.val = v    # знак, число или переменная
        self.left = l
        self.right = r

class ExpressionTree:
    def __init__(self):
        self.root = None

    def build(self, expr):
        # 1. Перевод инфиксной строки в ОПЗ
        expr = expr.replace(" ", "")
        prec = {'+': 1, '-': 1, '*': 2, '/': 2, 'u-': 3}
        postfix, ops = [], []
        i = 0
        while i < len(expr):
            if expr[i].isdigit():
                num = ""
                while i < len(expr) and (expr[i].isdigit() or expr[i] == '.'):
                    num += expr[i]; i += 1
                postfix.append(Node('val', float(num) if '.' in num else int(num)))
                continue
            elif expr[i].isalpha():
                postfix.append(Node('var', expr[i])); i += 1
                continue
            elif expr[i] == '(': ops.append(expr[i])
            elif expr[i] == ')':
                while ops and ops[-1] != '(': postfix.append(ops.pop())
                ops.pop()
            elif expr[i] in '+-*/':
                op = 'u-' if expr[i] == '-' and (i == 0 or expr[i-1] in '+-*/(') else expr[i]
                while ops and ops[-1] != '(' and prec.get(ops[-1], 0) >= prec[op]:
                    postfix.append(ops.pop())
                ops.append(op)
            i += 1
        while ops: postfix.append(ops.pop())

        # 2. Построение дерева связей в памяти
        stack = []
        for item in postfix:
            if isinstance(item, Node): stack.append(item)
            elif item == 'u-': stack.append(Node('op', 'u-', None, stack.pop()))
            else:
                r, l = stack.pop(), stack.pop()
                stack.append(Node('op', item, l, r))
        self.root = stack[0]

    def display(self, node=None, level=0):
        # Визуальный вывод структуры дерева боком
        if level == 0 and self.root: node = self.root
        if node:
            self.display(node.right, level + 1)
            print('    ' * level + f"[{node.val}]")
            self.display(node.left, level + 1)

    def _eval(self, node, vars_dict):
        if not node: return 0.0
        if node.type == 'val': return float(node.val)
        if node.type == 'var': return float(vars_dict[node.val])
        if node.val == 'u-': return -self._eval(node.right, vars_dict)
        l, r = self._eval(node.left, vars_dict), self._eval(node.right, vars_dict)
        return {'+': l+r, '-': l-r, '*': l*r, '/': l/r}[node.val]

    def evaluate(self, vars_dict):
        return self._eval(self.root, vars_dict)

    def _same(self, n1, n2):
        if not n1 and not n2: return True
        if not n1 or not n2 or n1.type != n2.type or n1.val != n2.val: return False
        return self._same(n1.left, n2.left) and self._same(n1.right, n2.right)

    def _clone(self, n):
        return Node(n.type, n.val, self._clone(n.left), self._clone(n.right)) if n else None

    def _simplify(self, n):
        if not n: return None, False
        n.left, ch_l = self._simplify(n.left)
        n.right, ch_r = self._simplify(n.right)
        ch = ch_l or ch_r
        if n.type == 'op' and n.val in ('+', '-'):
            l, r = n.left, n.right
            if l and r and l.type == 'op' and l.val == '*' and r.type == 'op' and r.val == '*':
                if self._same(l.right, r.right):
                    return Node('op', '*', Node('op', n.val, self._clone(l.left), self._clone(r.left)), self._clone(l.right)), True
                if self._same(l.left, r.left):
                    return Node('op', '*', self._clone(l.left), Node('op', n.val, self._clone(l.right), self._clone(r.right))), True
        return n, ch

    def simplify(self):
        while True:
            self.root, ch = self._simplify(self.root)
            if not ch: break

    def _get_vars(self, n, s):
        if n:
            if n.type == 'var': s.add(n.val)
            self._get_vars(n.left, s)
            self._get_vars(n.right, s)

    def get_variables(self):
        s = set()
        self._get_vars(self.root, s)
        return sorted(list(s))

    def _to_str(self, n):
        if not n: return ""
        if n.type in ('val', 'var'): return str(n.val)
        if n.val == 'u-': return f"-({self._to_str(n.right)})" if n.right.type == 'op' else f"-{self._to_str(n.right)}"
        l_str, r_str = self._to_str(n.left), self._to_str(n.right)
        p = {'+': 1, '-': 1, '*': 2, '/': 2}
        if n.left.type == 'op' and p.get(n.left.val, 3) < p[n.val]: l_str = f"({l_str})"
        if n.right.type == 'op' and (p.get(n.right.val, 3) < p[n.val] or (p.get(n.right.val, 3) == p[n.val] and n.val in ('-', '/'))): r_str = f"({r_str})"
        return f"{l_str} {n.val} {r_str}"

    def __str__(self):
        return self._to_str(self.root)


def main_menu():
    tree = None
    while True:
        print("\n=== Меню (Задача 20) ===")
        print("1. Ввести формулу")
        print("2. Упростить формулу")
        print("3. Вычислить значение")
        print("0. Выход")
        choice = input("Пункт: ").strip()

        if choice == '1':
            expr = input("Выражение: ").strip()
            if expr:
                try:
                    tree = ExpressionTree()
                    tree.build(expr)
                    print("\nСтруктура построенного дерева:")
                    tree.display()
                    print(f"Строковый вид: {tree}")
                except Exception as e:
                    print(f"Ошибка: {e}")
            if not expr:
                print("Ошибка: Выражение не может быть пустым.")
                continue

            # Проверка на недопустимые символы
            allowed = set("0123456789.+-*/()abcdefghijklmnopqrstuvwxyz")
            if not set(expr.replace(" ", "")).issubset(allowed):
                print("Ошибка: Формула содержит недопустимые символы.")
                continue
        elif choice == '2':
            if tree:
                tree.simplify()
                print("\nДерево после упрощения:")
                tree.display()
                print(f"Строковый вид: {tree}")
            else:
                print("Сначала введите формулу")
        elif choice == '3':
            if tree:
                v_list = tree.get_variables()
                v_dict = {}
                try:
                    for v in v_list:
                        v_dict[v] = float(input(f"Значение {v}: ").strip())
                    print(f"Результат вычисления: {tree.evaluate(v_dict)}")
                except Exception as e:
                    print(f"Ошибка подсчета: {e}")
            else:
                print("Сначала введите формулу")
        elif choice == '0':
            break


if __name__ == "__main__":
    main_menu()
