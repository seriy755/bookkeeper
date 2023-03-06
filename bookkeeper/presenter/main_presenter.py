from bookkeeper.presenter.expense_presenter import ExpensePresenter
from bookkeeper.presenter.category_presenter import CategoryPresenter
from bookkeeper.presenter.budget_presenter import BudgetPresenter

class MainPresenter:
    
    def __init__(self, view, exp_repo, cat_repo, budg_repo):
        self.view = view
        self.exp_pres = ExpensePresenter(exp_repo)
        self.cat_pres = CategoryPresenter(cat_repo)
        self.budg_pres = BudgetPresenter(budg_repo)
        self.view.on_expense_add_button_clicked(
            self.handle_expense_add_button_clicked
        )
        self.view.on_category_edit_button_clicked(
            self.handle_category_edit_button_clicked
        )
        
    def get_data(self):
        data = {'exp_data': self.exp_pres.data(), 
                'cat_data': self.cat_pres.data(),
                'budg_data': self.budg_pres.data()}
        
        return data
    
    def _pk_to_cat(self, data):
        for exp in data['exp_data']:
            cat_pk = exp[2]
            cat = self.cat_pres.get_item(cat_pk)
            exp[2] = cat.name
        return data
        
    def update_data(self):
        data = self.get_data()
        data = self._pk_to_cat(data)
        
        if data['exp_data']:
            self.view.set_expense_grid(data['exp_data'])

        if data['cat_data']:
            self.view.set_category_dropdown(data['cat_data'])
            
        if data['budg_data']:
            self.view.set_budget_grid(data['budg_data'])
        else:
            self.budg_pres.init_data(self.exp_pres.repo)
            self.view.set_budget_grid(self.budg_pres.data())
    
    def show(self):
        self.view.show()
        self.update_data()
        
    def handle_expense_add_button_clicked(self):
        amount = int(self.view.get_amount())
        cat_pk = self.view.get_selected_cat()
        self.exp_pres.add_data(amount=amount, category=cat_pk)
        self.budg_pres.update_data(self.exp_pres.repo)
        self.update_data()
        
    def handle_category_edit_button_clicked(self):
        self.window = self.view.category_editor(self.cat_pres.data())
        self.window.on_category_add_button_clicked(
            self.handle_category_add_button_clicked
        )
        self.window.setWindowTitle("Редактирование категорий")
        self.window.resize(480, 640)
        self.window.show()
        
    def handle_category_add_button_clicked(self):
        name = self.window.get_new_category()
        parent = self.window.get_selected_parent()
        self.cat_pres.add_data(name=name, parent=parent)
        self.window.update_data(self.cat_pres.data())
        self.update_data()
        