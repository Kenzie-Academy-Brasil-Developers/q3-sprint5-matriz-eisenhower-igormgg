from flask import current_app
from app.models.categories_model import Categories_Model


def get_eisenhower_num(importance, urgency):
    if importance == 1 and urgency == 1:
        return 1
    
    if importance == 1 and urgency == 2:
        return 2

    if importance == 2 and urgency == 1:
        return 3

    if importance == 2 and urgency == 2:
        return 4
    
    else:
        return "error"

def data_to_patch(query, data):
    for key, value in data.items():
        setattr(query, key, value)
    
    return query

def data_categories_to_patch(data):

    if 'categories' in data.keys():
            category_list = data.pop('categories')
            data['categories'] = []

            for category in category_list:
                category = category.title()

                category_query = Categories_Model.query.filter_by(name=category).one_or_none()

                if not category_query:
                    category_query = Categories_Model(**{"name": category})

                    current_app.db.session.add(category_query)
                    current_app.db.session.commit()
            
                data['categories'].append(category_query)
    
    return data