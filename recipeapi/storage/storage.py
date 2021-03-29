from sqlalchemy.sql import exists
from sqlalchemy import MetaData, and_
from .database import get_database


class Storage:
    """
    A layer of abstraction between the higher level API code in routes.py and the lower level interface to the target database.
    Changes to the database or storage system used and low level optimisations are decoupled from the high level API logic.
    """
    def __init__(self):
        self.session, self.engine = get_database()
        meta = MetaData()
        meta.reflect(bind=self.engine)
        self.recipes = meta.tables['recipes']
        self.ingredients = meta.tables['ingredients']
        self.bridge_recipes_ingredients = meta.tables['bridge_recipes_ingredients']

    @staticmethod
    def _res_to_json(results):
        return [dict(r) for r in results]
    
    @staticmethod
    def _get_alch_filter(target_table, attr_filters):
        filter_ = [target_table.columns[attr_name] == attr_value for attr_name, attr_value in attr_filters.items()]
        return and_(*filter_)

    def item_exists(self, collection:str, attr_filters:dict):
        target_table = getattr(self, collection)
        filter_ = self._get_alch_filter(target_table, attr_filters)
        return self.session.query(exists().where(filter_)).scalar()
    
    def get_items(self, collection, attr_filters={}, by_related=None):
        target_table = getattr(self, collection)
        if by_related is None:
            filter_ = self._get_alch_filter(target_table, attr_filters)
            items = self.session.query(target_table).where(filter_).all()
        else:
            if by_related=='ingredients' and collection=='recipes':
                items = self.session.query(target_table).join(self.bridge_recipes_ingredients).\
                        filter(self.bridge_recipes_ingredients.columns.ingredient_id==attr_filters['id']).\
                        all()
            else:
                raise NotImplementedError('The specified resource extraction is not implemented.')
        return self._res_to_json(items)

    def get_item(self, collection, attr_filters={}):   
        return self.get_items(collection, attr_filters=attr_filters)[0]

    def update_item(self, collection, id_, data):
        target_table = getattr(self, collection)
        if collection!='recipes':
            raise NotImplementedError('Storage.update_item has only been implemented for the recipes collection.')
        self.session.execute(target_table.update().where(target_table.columns['id']==id_).\
                             values(**data))
        # TODO Create/delete entries in bridge_recipes_ingredients table based on
        # possibly updated ingredients to maintain relationships. Commit once done
        self.session.commit()
    
    def delete_item(self, collection, id_):
        target_table = getattr(self, collection)
        if collection!='recipes':
            raise NotImplementedError('Storage.delete_item has only been implemented for the recipes collection.')
        self.session.query().where(target_table.columns['id']==id_).\
                    delete()
        self.session.commit()
    
    def add_item(self, collection, name, data):
        target_table = getattr(self, collection)
        print('Inserting',data)
        self.session.execute(target_table.insert(), data)
        # TODO Create entries in bridge_recipes_ingredients based on ingredients in recipe
        # if the collection is 'recipes'
        self.session.commit()

    