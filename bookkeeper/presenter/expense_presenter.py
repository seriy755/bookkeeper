from bookkeeper.models.expense import Expense
from bookkeeper.presenter.abstract_presenter import AbstractPresenter


class ExpensePresenter(AbstractPresenter):
    
    def __init__(self, repo):
        self.repo = repo
        self._data = self.repo.get_all()
    
    def _to_list(self):
        data = []
        for item in self._data:
            amount, cat, date, comment = item.amount, item.category, \
                item.expense_date, item.comment
            data.append([date, amount, cat, comment])
        return data
    
    def data(self):
        return self._to_list()
        
    def add_data(self, **kwargs):
        exp = Expense(**kwargs)
        self.repo.add(exp)
        self._data = self.repo.get_all()  
