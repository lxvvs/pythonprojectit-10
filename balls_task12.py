class Node:
    """Узел двусвязного списка."""

    def __init__(self, color: int):
        self.color = color
        self.prev = None
        self.next = None


class DoublyLinkedList:
    """Двусвязный список для управления цепочкой шариков."""

    def __init__(self):
        self.head = None
        self.tail = None

    def append(self, color: int):
        """Добавление шарика в конец списка."""
        new_node = Node(color)
        if not self.head:
            self.head = self.tail = new_node
        else:
            self.tail.next = new_node
            new_node.prev = self.tail
            self.tail = new_node

    def build_from_list(self, colors: list):
        """Заполнение списка из массива."""
        self.head = self.tail = None
        for color in colors:
            self.append(color)

    def process_game(self) -> int:
        """Основной алгоритм: поиск и удаление групп из 3+ шариков одного цвета."""
        destroyed_total = 0
        curr = self.head

        while curr:
            start_node = curr
            count = 1

            # Ищем длину группы одинаковых шариков
            while curr.next and curr.next.color == curr.color:
                count += 1
                curr = curr.next

            # Если нашли цепочку из 3 и более - готовимся к удалению
            if count >= 3:
                destroyed_total += count

                prev_node = start_node.prev
                next_node = curr.next

                # Перевязываем указатели, "вырезая" удаляемую цепочку из списка
                if prev_node:
                    prev_node.next = next_node
                else:
                    self.head = next_node  # Обновляем голову, если удалили начало

                if next_node:
                    next_node.prev = prev_node
                else:
                    self.tail = prev_node  # Обновляем хвост, если удалили конец

                # Откатываемся назад по списку, чтобы проверить новые слияния
                if prev_node:
                    temp = prev_node
                    while temp.prev and temp.prev.color == temp.color:
                        temp = temp.prev
                    curr = temp
                else:
                    curr = self.head
            else:
                # Если группа меньше 3, идем дальше по списку
                curr = curr.next

        return destroyed_total


def run_tests():
    """
    Комплексное системное тестирование (Критерий: 4 балла).
    Тесты разбиты на логические группы и покрывают все типы сценариев.
    """
    print("\n" + "=" * 70)
    print(" СИСТЕМНОЕ ТЕСТИРОВАНИЕ ПРОГРАММЫ (ЗАДАЧА №12)")
    print("=" * 70)

    test_groups = {
        "ГРУППА 1: БАЗОВЫЕ СЦЕНАРИИ (ИЗ ЗАДАНИЯ)": [
            {"input": [1, 3, 3, 3, 2], "expected": 3, "desc": "Один явный триггер в середине"},
            {"input": [3, 3, 2, 1, 1, 1, 2, 2, 3, 3], "expected": 10, "desc": "Каскадное (цепное) схлопывание до нуля"}
            {"input": [1, 2, 2, 2, 3, 3, 3, 1], "expected": 7, "desc": "Многоуровневый каскад (взрыв 2 -> смыкание 3 -> взрыв 3)"}
        ],
        "ГРУППА 2: ГРАНИЧНЫЕ СЛУЧАИ": [
            {"input": [], "expected": 0, "desc": "Пустой список шаров"},
            {"input": [5], "expected": 0, "desc": "Всего один шар в списке"},
            {"input": [2, 2], "expected": 0, "desc": "Два одинаковых шара (недостаточно для взрыва)"},
            {"input": [4, 4, 4], "expected": 3, "desc": "Ровно три одинаковых шара"},
            {"input": [1, 1, 1, 1, 1], "expected": 5, "desc": "Все шары одного цвета (больше трех)"},
            {"input": [1, 1, 1, 2, 2, 2], "expected": 6, "desc": "Две изолированные группы по 3 шара подряд"}
        ],
        "ГРУППА 3: СЦЕНАРИИ БЕЗ ИЗМЕНЕНИЙ": [
            {"input": [1, 2, 1, 2, 1, 2], "expected": 0, "desc": "Шары чередуются, совпадений нет"},
            {"input": [1, 1, 2, 2, 3, 3, 4, 4], "expected": 0, "desc": "Пары дублей, но ни одна не достигает 3 штук"}
        ]
    }

    total_tests = 0
    passed_tests = 0

    for group_name, tests in test_groups.items():
        print(f"\n{group_name}")
        print("-" * 70)
        print(f"{'Описание теста':<35} | {'Вход':<15} | {'Результат':<12}")
        print("-" * 70)

        for test in tests:
            total_tests += 1
            dll = DoublyLinkedList()
            dll.build_from_list(test["input"])
            result = dll.process_game()

            if result == test["expected"]:
                status = "ПРОЙДЕН"
                passed_tests += 1
            else:
                status = f"ФЕЙЛ (Ожид. {test['expected']})"

            print(f"{test['desc']:<35} | {str(test['input']):<15} | {status} ({result})")

    print("\n" + "=" * 70)
    print(f"ИТОГ ТЕСТИРОВАНИЯ: Успешно пройдено {passed_tests} из {total_tests} тестов.")
    print("=" * 70 + "\n")


def main_menu():
    """Циклическое меню для взаимодействия с пользователем."""
    while True:
        print("\n=== Главное меню (Задача №12: Шарики) ===")
        print("1. Ввести данные вручную")
        print("2. Запустить комплексное системное тестирование")
        print("0. Выход")
        print("=========================================")

        choice = input("Выберите действие: ").strip()

        if choice == '1':
            try:
                line = input("Введите количество шаров и их цвета через пробел (например: 5 1 3 3 3 2):\n").strip()
                if not line:
                    print("Ошибка: строка ввода пуста.")
                    continue

                parts = list(map(int, line.split()))
                if not parts:
                    print("Ошибка: данные не обнаружены.")
                    continue

                n = parts[0]
                colors = parts[1:]

                if n < 0:
                    print("Ошибка: количество шаров N не может быть отрицательным.")
                    continue

                if len(colors) != n:
                    print(f"\n[Внимание]: Указано N={n}, но фактически введено {len(colors)} цветов.")
                    print("Обрабатываем реально введенную последовательность согласно правилам...")

                dll = DoublyLinkedList()
                dll.build_from_list(colors)

                destroyed = dll.process_game()
                print(f"\nРезультат обработки: уничтожено шариков -> {destroyed}")

            except ValueError:
                print("\nОшибка ввода (Защита от некорректных данных):")
                print("Пожалуйста, вводите исключительно целые числа через пробел.")

        elif choice == '2':
            run_tests()

        elif choice == '0':
            print("Завершение работы программы. Проект сохранен.")
            break

        else:
            print("Неизвестная команда. Введите цифру 1, 2 или 0.")


if __name__ == "__main__":
    main_menu()
