from bookkeeper.presenter.expense_presenter import ExpensePresenter
from bookkeeper.presenter.category_presenter import CategoryPresenter
from bookkeeper.presenter.budget_presenter import BudgetPresenter

class MainPresenter:
    
    def __init__(self, view, exp_repo, cat_repo):
        self.view = view
        self.exp_pres = ExpensePresenter(exp_repo)
        self.cat_pres = CategoryPresenter(cat_repo)
        self.view.on_expense_add_button_clicked(
            self.handle_expense_add_button_clicked
        )
        
    def get_data(self):
        data = {'exp_data': self.exp_pres.data(), 
                'cat_data': self.cat_pres.data()
               }
        
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
    
    def show(self):
        self.view.show()
        self.update_data()
        
    def handle_expense_add_button_clicked(self):
        amount = int(self.view.get_amount())
        cat_pk = self.view.get_selected_cat()
        self.exp_pres.add_data(amount=amount, category=cat_pk)
        self.update_data()
        