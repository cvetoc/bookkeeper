"""
Простой тестовый скрипт для терминала
"""

from bookkeeper.models.category import Category
from bookkeeper.models.expense import Expense
from bookkeeper.models.budget import Budget
from bookkeeper.repository.memory_repository import MemoryRepository
from bookkeeper.repository.sqlite_repository import SQLiteRepository
from bookkeeper.utils import read_tree
from PySide6.QtWidgets import QApplication
from bookkeeper.view.Window import Window

import sys

def memory_client():
    cat_repo = MemoryRepository[Category]()
    exp_repo = MemoryRepository[Expense]()

    cats = '''
    продукты
        мясо
            сырое мясо
            мясные продукты
        сладости
    книги
    одежда
    '''.splitlines()

    Category.create_from_tree(read_tree(cats), cat_repo)

    while True:
        try:
            cmd = input('$> ')
        except EOFError:
            break
        if not cmd:
            continue
        if cmd == 'категории':
            print(*cat_repo.get_all(), sep='\n')
        elif cmd == 'расходы':
            print(*exp_repo.get_all(), sep='\n')
        elif cmd[0].isdecimal():
            amount, name = cmd.split(maxsplit=1)
            try:
                cat = cat_repo.get_all({'name': name})[0]
            except IndexError:
                print(f'категория {name} не найдена')
                continue
            exp = Expense(int(amount), cat.pk)
            exp_repo.add(exp)
            print(exp)

def SQLite_client():

    DB_NAME = 'BD.db'

    app = QApplication(sys.argv)

    view = MainWindow()
    model = None

    category_repo = SQLiteRepository[Category](DB_NAME, Category)
    expense_repo = SQLiteRepository[Expense](DB_NAME, Expense)
    budget_repo = SQLiteRepository[Budget](DB_NAME, Budget)

    if len(category_repo.get_all()) == 0:
        cats = '''
        продукты
            мясо
                сырое мясо
                мясные продукты
            сладости
        книги
        одежда
        '''.splitlines()
        Category.create_from_tree(read_tree(cats), category_repo)

    window = ExpensePresenter(model, view, category_repo, expense_repo)
    window.show()
    app.exec()