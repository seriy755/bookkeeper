from bookkeeper.presenter.expense_presenter import ExpensePresenter
from bookkeeper.presenter.category_presenter import CategoryPresenter
from bookkeeper.presenter.budget_presenter import BudgetPresenter


class MainPresenter:
    
    def __init__(self, view, exp_repo, cat_repo, budget_repo):
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
        
    def _pk_to_cat(self, data):
        for exp in data['exp_data']:
            cat_pk = exp[2]
            cat = self.cat_pres.get_item(cat_pk)
            exp[2] = cat.name
        return data
        
    def get_data(self):
        data = {'exp_data': self.exp_pres.data(), 
                'cat_data': self.cat_pres.data(),
                'budget_data': self.budget_pres.data()}
        
        return data
        
    def update_data(self):
        self.budget_pres.update_data(self.exp_pres.repo)
        data = self.get_data()
        data = self._pk_to_cat(data)
        
        exp_ids = self.exp_pres.get_all_pk()
        self.view.set_expense_grid(data['exp_data'],
                                       exp_ids)

        self.view.set_category_dropdown(data['cat_data'])
        self.view.category_editor.update_data(data['cat_data'])
            
        self.view.set_budget_grid(data['budget_data'])
    
    def show(self):
        self.view.show()
        self.update_data()
        
    def handle_expense_add_button_clicked(self):
        amount = int(self.view.get_amount())
        cat_pk = self.view.get_selected_cat()
        self.exp_pres.add_data(amount=amount, category=cat_pk)
        self.update_data()
        
    def handle_category_edit_button_clicked(self):
        data = self.cat_pres.data()
        self.view.set_category_editor_window(data)
        
    def handle_category_add_button_clicked(self):
        name = self.view.category_editor.get_new_category()
        parent = self.view.category_editor.get_selected_parent()
        cat = self.cat_pres.get_item_all(where={'name': name})
        if not cat:
            self.cat_pres.add_data(name=name, parent=parent)
            self.view.category_editor.update_data(self.cat_pres.data())
            self.update_data()
        
    def handle_category_delete_button_clicked(self):
        name = self.view.category_editor.get_selected_category()
        cat = self.cat_pres.get_item_all(where={'name': name})[0]
        deleted_exps = self.exp_pres.get_item_all(where={'category': cat.pk})
        self.exp_pres.delete_data(deleted_exps)
        self.cat_pres.delete_data(cat)
        self.view.category_editor.update_data(self.cat_pres.data())
        self.update_data()
        
    def handle_expense_delete_button_clicked(self) -> None:
        idx = self.view.get_selected_expense()
        if idx != 0:
            exp = self.exp_pres.get_item(idx)
            self.exp_pres.delete_data([exp])
            self.update_data()
    
    def handle_expense_save_changes_button_clicked(self) -> None:
        exp_data = self.view.get_all_expenses()
        restrict_data = self.view.get_all_restricts()
        self.budget_pres.update_restricts(restrict_data)
        
        for exp in exp_data:
            pk, date = exp[0], exp[1]
            amount, comment = int(exp[2]), exp[4]
            cat = self.cat_pres.get_item_all(where={'name': exp[3]})[0]
            self.exp_pres.update_data(pk=pk, expense_date=date, 
                category=cat.pk, amount=amount, comment=comment)
            
        self.budget_pres.update_data(self.exp_pres.repo)
        self.view.set_budget_grid(self.budget_pres.data())
        
    def handle_category_save_changes_button_clicked(self) -> None:
        cat_data = self.view.category_editor.get_all_categories()
        
        for cat in cat_data:
            self.cat_pres.update_data(pk=cat[0], name=cat[1], 
                                      parent=cat[2])
        self.update_data()