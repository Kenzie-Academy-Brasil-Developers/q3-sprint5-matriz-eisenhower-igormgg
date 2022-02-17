from flask import current_app, jsonify, request
from sqlalchemy.exc import IntegrityError
from werkzeug.exceptions import NotFound

from app.models.categories_model import Categories_Model
from app.models.eisenhowers_model import Eisenhowers_Model
from app.services.helpers import data_to_patch


def list_categories_tasks():
    all_categories = Categories_Model.query.all()

    categories_tasks = []

    for category in all_categories:
        output = {}

        output['id'] = category.id
        output['name'] = category.name
        output['description'] = category.description
        output['tasks'] = []

        for task in category.tasks:

            output_task = {}

            output_task['id'] = task.id
            output_task['name'] = task.name
            output_task['description'] = task.description
            output_task['duration'] = task.duration
            output_task['classification'] = Eisenhowers_Model.query.get(task.__dict__['eisenhowers_id']).type
            
            output['tasks'].append(output_task)

        categories_tasks.append(output)

    return jsonify(categories_tasks), 200

def create_category():
    try:
        data = request.get_json()
        data['name'] = data['name'].title()

        new_category = Categories_Model(**data)

        current_app.db.session.add(new_category)
        current_app.db.session.commit()

        return jsonify(new_category), 201
    
    except IntegrityError:
        return {'error': f'{data["name"]} already registered on database'}, 409
    
    except KeyError as ke:
        return {"error": f"{ke.args[0]} required"}, 400

def patch_category(id: int):
    
    try:
        data = request.get_json()
        if 'name' in data.keys():
            data['name'] = data['name'].title()

        category_query = Categories_Model.query.get_or_404(id)

        data_to_patch(category_query, data)

        current_app.db.session.add(category_query)
        current_app.db.session.commit()

        return jsonify(category_query), 200

    except NotFound:
        return {'error': 'Category not found on database!'}, 404

def delete_category(id: int):
    try:
        category_query = Categories_Model.query.get_or_404(id)

        current_app.db.session.delete(category_query)
        current_app.db.session.commit()

        return "", 204

    except NotFound:
        return {'error': 'Category not found on database!'}, 404