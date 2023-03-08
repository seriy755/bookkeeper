from bookkeeper.models.category import Category
from bookkeeper.presenter.abstract_presenter import AbstractPresenter


class CategoryPresenter(AbstractPresenter):
    
    def __init__(self, repo):
        self.repo = repo
        self._data = self.repo.get_all()
    
    def _to_list(self):
        data = []
        for item in self._data:
            pk, name, parent = item.pk, item.name, item.parent
            data.append([pk, name, parent])
        return data
    
    def data(self):
        return self._to_list()
        
    def add_data(self, **kwargs):
        cat = Category(**kwargs)
        self.repo.add(cat)
        self._data = self.repo.get_all()
    
    def delete_data(self, cat):
        for child in cat.get_subcategories(self.repo):
            child.parent = cat.parent
            self.repo.update(child)
        self.repo.delete(cat.pk)
        self._data = self.repo.get_all()
        
    def update_data(self, **kwargs):
        cat = Category(**kwargs)
        self.repo.update(cat)
        self._data = self.repo.get_all()
        
    def get_item(self, pk):
        return self.repo.get(pk)
    
    def get_item_all(self, where=None):
        return self.repo.get_all(where)
