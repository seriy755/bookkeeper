from bookkeeper.models.budget import Budget
from bookkeeper.presenter.abstract_presenter import AbstractPresenter


class BudgetPresenter(AbstractPresenter):
    
    def __init__(self, repo):
        self.repo = repo
        self._data = repo.get_all()
        if not self._data:
            b1 = Budget(0, 'день', None, 1000)
            b2 = Budget(0, 'неделя', None, 7000)
            b3 = Budget(0, 'месяц', None, 30000)
            self.repo.add(b1)
            self.repo.add(b2)
            self.repo.add(b3)
            self._data = repo.get_all()
        
    
    def _to_list(self):
        data = []
        for item in self._data:
            amount, restrict = item.amount, item.restrict
            data.append([amount, restrict])
        return data
    
    def data(self):
        return self._to_list()
        
    def update_data(self, exp_repo):
        amounts = Budget.get_amounts(exp_repo)
        for budget, amount in zip(self._data, amounts):
            budget.amount = amount
            self.repo.update(budget)
            
    def update_restricts(self, restricts):
        for budget, restrict in zip(self._data, restricts):
            budget.restrict = restrict
            self.repo.update(budget)
