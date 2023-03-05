from bookkeeper.models.budget import Budget


class BudgetPresenter:
    
    def __init__(self, repo):
        self.repo = repo
        self._data = self.repo.get_all()
        self.restricts = [(None, 1000), 
                          (None, 7000), 
                          (None, 30000)]
    
    def _to_list(self):
        data = []
        for item in self._data:
            amount, restrict = item.amount, item.restrict
            data.append([amount, restrict])
        return data
    
    def init_data(self, exp_repo):
        for budg in Budget.create_from_list(self.restricts, 
                                            exp_repo):
            self.repo.add(budg)
        self._data = self.repo.get_all()
    
    def data(self):
        return self._to_list()
        
    def update_data(self, exp_repo):
        amounts = Budget.get_amounts(exp_repo)
        for budg, amount in zip(self._data, amounts):
            budg.amount = amount
            self.repo.update(budg)
        