from flask import current_app, jsonify, request
from sqlalchemy.exc import IntegrityError
from werkzeug.exceptions import NotFound

from app.models.categories_model import Categories_Model
from app.models.eisenhowers_model import Eisenhowers_Model
from app.models.exceptions_model import Eisenhower_Error
from app.models.tasks_model import Tasks_Model
from app.services.helpers import data_categories_to_patch, data_to_patch, get_eisenhower_num


def create_task():

    try:
        data = request.get_json()
        data['name'] = data['name'].title()

        category_list = data.pop('categories')

        importance_num = data['importance']
        urgency_num = data['urgency']
        eisenhower_num = get_eisenhower_num(importance_num, urgency_num)

        if eisenhower_num == "error":
            raise Eisenhower_Error


        data['eisenhowers_id'] = eisenhower_num

        new_task = Tasks_Model(**data)

        for category in category_list:
            category = category.title()

            category_query = Categories_Model.query.filter_by(name=category).one_or_none()

            if not category_query:
                category_query = Categories_Model(**{"name": category})

                current_app.db.session.add(category_query)
                current_app.db.session.commit()
                
            new_task.categories.append(category_query)

        view_task = new_task.__dict__.copy()

        current_app.db.session.add(new_task)
        current_app.db.session.commit()
        
        eisenhower_query = Eisenhowers_Model.query.get(eisenhower_num)

        view_task['classification'] = eisenhower_query.type

        del view_task['_sa_instance_state']
        del view_task['importance']
        del view_task['urgency']
        del view_task['eisenhowers_id']

        view_task['categories'] = category_list

        return view_task, 201

    except Eisenhower_Error as ee:
        return ee.eisenhower_err_description(importance_num, urgency_num), ee.code
    
    except IntegrityError:
        return {'error': f'{data["name"]} already registered on database'}, 409
    
    except KeyError as ke:
        return {"error": f"{ke.args[0]} required"}, 400

def patch_task(id: int):
    try:
        data = request.get_json()

        tasks_query = Tasks_Model.query.get_or_404(id)

        if 'name' in data.keys():
            data['name'] = data['name'].title()
        
        if 'importance' in data.keys():
            importance_num = data['importance']
        else:
            importance_num = tasks_query.importance
        
        if 'urgency' in data.keys():
            urgency_num = data['urgency']
        else:
            urgency_num = tasks_query.urgency
        
        eisenhower_num = get_eisenhower_num(importance_num, urgency_num)

        eisenhower_query = Eisenhowers_Model.query.filter_by(id=eisenhower_num).one()

        data['eisenhowers_id'] = eisenhower_num

        if eisenhower_num == "error":
            raise Eisenhower_Error

        data_categories_to_patch(data)
        
        data_to_patch(tasks_query, data)

        view_task = tasks_query.__dict__.copy()

        view_task['classification'] = eisenhower_query.type

        view_task['categories'] = []

        for category in tasks_query.categories:
            view_task['categories'].append(category.name)


        del view_task['_sa_instance_state']
        del view_task['importance']
        del view_task['urgency']
        del view_task['eisenhowers_id']

        current_app.db.session.add(tasks_query)
        current_app.db.session.commit()

        return jsonify(view_task), 200

    except NotFound:
        return {'error': 'Category not found on database!'}, 404
    
    except Eisenhower_Error as ee:
        return ee.eisenhower_err_description(importance_num, urgency_num), ee.code
    
    except IntegrityError:
        return {'error': f'{data["name"]} already registered on database'}, 409

def delete_task(id: int):
    try:
        query = Tasks_Model.query.get_or_404(id)

        current_app.db.session.delete(query)
        current_app.db.session.commit()

        return "", 204

    except NotFound:
        return {'error': 'Task not found on database!'}, 404