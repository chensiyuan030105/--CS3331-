class Category:
    def __init__(self, category_name):
        self.category_name = category_name
        self.item_types = []

    def add_item_type(self, item_type):
        self.item_types.append(item_type)

    def __str__(self):
        return f"Category({self.category_name})"
