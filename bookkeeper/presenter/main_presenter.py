"""
Модуль для описания общего представителя
"""
from datetime import datetime

from bookkeeper.presenter.expense_presenter import ExpensePresenter
from bookkeeper.presenter.category_presenter import CategoryPresenter
from bookkeeper.presenter.budget_presenter import BudgetPresenter

from bookkeeper.models.budget import Budget
from bookkeeper.models.expense import Expense
from bookkeeper.models.category import Category
from bookkeeper.repository.abstract_repository import AbstractRepository

from bookkeeper.view.main_window import MainWindow
from bookkeeper.view.modal_windows import error_message


class MainPresenter:
    "Класс общего представителя"
    def __init__(self, view: MainWindow,
                 exp_repo: AbstractRepository['Expense'],
                 cat_repo: AbstractRepository['Category'],
                 budget_repo: AbstractRepository['Budget']) -> None:
        self.view = view
        self.exp_pres = ExpensePresenter(exp_repo)
        self.cat_pres = CategoryPresenter(cat_repo)
        self.budget_pres = BudgetPresenter(budget_repo)

        self.view.on_expense_add_button_clicked(
            self.handle_expense_add_button_clicked
        )
        self.view.on_category_edit_button_clicked(
            self.handle_category_edit_button_clicked
        )
        self.view.on_expense_delete_button_clicked(
            self.handle_expense_delete_button_clicked
        )
        self.view.on_expense_save_changes_button_clicked(
            self.handle_expense_save_changes_button_clicked
        )

        self.view.category_editor.on_category_add_button_clicked(
            self.handle_category_add_button_clicked
        )
        self.view.category_editor.on_category_delete_button_clicked(
            self.handle_category_delete_button_clicked
        )
        self.view.category_editor.on_category_save_changes_button_clicked(
            self.handle_category_save_changes_button_clicked
        )

    def set_data(self) -> None:
        "Вывести на экран данные из базы данных"
        self.view.set_category_dropdown(self.cat_pres.data())

        exp_data = self.exp_pres.data()
        for exp in exp_data:
            cat = self.cat_pres.get(exp[2])
            if cat is not None:
                exp[2] = cat.name
        self.view.set_expense_grid(exp_data,
                                   self.exp_pres.get_all_pk())

        self.budget_pres.update_data(self.exp_pres.repo)
        self.view.set_budget_grid(self.budget_pres.data())

    def show(self) -> None:
        "Вывести окно приложения"
        self.view.show()
        self.set_data()

    def _check_amount(self, amount: str) -> bool:
        try:
            if float(amount) < 0:
                error_message("Сумма затрат не может быть отрицательной!\n"
                              "Пожалуйста, введите положительное число!")
                return False
        except ValueError:
            error_message("Неверно указана сумма затраты!\n"
                          "Пожалуйста, введите положительное число!")
            return False
        return True

    def handle_expense_add_button_clicked(self) -> None:
        """
        Добавить новую запись в таблицу расходов при
        нажатии на кнопку 'Добавить'. Добавить новые
        данные в базу данных
        """
        if not self._check_amount(self.view.get_amount()):
            return
        amount = float(self.view.get_amount())

        cat_pk = self.view.get_selected_cat()
        if cat_pk is None:
            error_message("Не выбрана категория расхода!\n"
                          "Пожалуйста, укажите категорию расхода")
            return

        self.exp_pres.add_data(amount=amount, category=cat_pk)

        self.set_data()

    def handle_expense_delete_button_clicked(self) -> None:
        """
        Удалить запись в таблице расходов при
        нажатии на кнопку 'Удалить'. Удалить запись
        в базе данных
        """
        ids = self.view.get_selected_expense()
        if ids is None:
            return

        deleted_exps: list['Expense'] = []
        for idx in ids:
            deleted_exps.append(self.exp_pres.get(idx))
        self.exp_pres.delete_data(deleted_exps)

        self.set_data()

    def handle_expense_save_changes_button_clicked(self) -> None:
        """
        Сохранить редактирование записей в таблицах при
        нажатии на кнопку 'Сохранить изменения'. Обновить записи
        в базе данных
        """
        restrict_data = self.view.get_all_restricts()
        self.budget_pres.update_restricts(restrict_data)

        exp_data = self.view.get_all_expenses()
        for exp in exp_data:
            pk = exp[0]
            comment = exp[4]
            date = exp[1]
            try:
                date = datetime.strptime(date, '%Y-%m-%d').strftime('%Y-%m-%d')
            except ValueError:
                error_message(f"Неправильный формат даты: {date}!\n"
                              "Пожалуйста, введите дату в виде: г-м-д!")
                continue

            if not self._check_amount(exp[2]):
                continue
            amount = float(exp[2])

            try:
                cat = self.cat_pres.get_all(where={'name': exp[3]})[0]
                self.exp_pres.update_data(
                    pk=pk, expense_date=date,
                    category=cat.pk, amount=amount, comment=comment)
            except IndexError:
                error_message(f"Неверное имя категории: {exp[3]}!\n"
                              "Пожалуйста, введите имя из списка категорий!")
                continue

        self.budget_pres.update_data(self.exp_pres.repo)

        self.set_data()

    def handle_category_edit_button_clicked(self) -> None:
        """
        Открыть редактиование списка категорий при
        нажатии на кнопку 'Редактировать'
        """
        data = self.cat_pres.data()
        self.view.show_category_editor_window(data)

    def handle_category_add_button_clicked(self) -> None:
        """
        Добавить новую запись в список категорий при
        нажатии на кнопку 'Добавить'. Добавить новые
        данные в базу данных
        """
        name = self.view.category_editor.get_new_category()
        if not (name and name.strip()):
            error_message('Неподдерживаемое имя категории: пустая строка!')
            return
        cat = self.cat_pres.get_all(where={'name': name})
        if cat:
            return

        parent = self.view.category_editor.get_selected_category()
        pid = None if parent is None else self.cat_pres.get_all(
                                            where={'name': parent})[0].pk

        self.cat_pres.add_data(name=name, parent=pid)
        self.view.category_editor.update_data(self.cat_pres.data())

        self.set_data()

    def handle_category_delete_button_clicked(self) -> None:
        """
        Удалить запись в списке категорий при
        нажатии на кнопку 'Удалить'. Удалить запись
        в базе данных
        """
        name = self.view.category_editor.get_selected_category()
        cat = self.cat_pres.get_all(where={'name': name})[0]

        deleted_exps = self.exp_pres.get_all(where={'category': cat.pk})
        self.exp_pres.delete_data(deleted_exps)

        self.cat_pres.delete_data(cat)
        self.view.category_editor.update_data(self.cat_pres.data())

        self.set_data()

    def handle_category_save_changes_button_clicked(self) -> None:
        """
        Сохранить редактирование записей в списке категорий при
        нажатии на кнопку 'Сохранить изменения'. Обновить записи
        в базе данных
        """
        cat_data = self.view.category_editor.get_all_categories()
        for cat in cat_data:
            if not (cat[1] and cat[1].strip()):
                error_message('Неподдерживаемое имя категории: пустая строка!')
                continue
            self.cat_pres.update_data(pk=cat[0], name=cat[1], parent=cat[2])

        self.view.category_editor.update_data(self.cat_pres.data())
        self.set_data()
