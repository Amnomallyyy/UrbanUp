import json
from flask import Blueprint, render_template, request, jsonify, url_for
from flask_login import login_required, current_user
from models import Project
from Final import db

Proj = Blueprint('Proj', __name__)


# Route to save map data
@Proj.route('/save_project', methods=['POST'])
@login_required
def save_project():
    data = request.get_json()
    project_name = data.get('name', 'Untitled City')
    map_state = data.get('map_state')

    # Ensure these column names match exactly what is in your models.py
    new_project = Project(
        fileName=project_name,
        jsonMapData=map_state,
        aiAdvice="",
        user_id=current_user.id
    )

    db.session.add(new_project)
    db.session.commit()

    return jsonify({
        "status": "success",
        "redirect_url": url_for('Proj.saved_files_directory')
    }), 200


# Route to display the saved files dashboard
@Proj.route('/savedfiles')
@login_required
def saved_files_directory():
    # Fetch projects specifically for the logged-in user
    user_projects = Project.query.filter_by(user_id=current_user.id).order_by(Project.id.desc()).all()
    return render_template('savedfiles.html', user=current_user, projects=user_projects)


# Route to delete a project
@Proj.route('/delete_project/<int:project_id>', methods=['POST'])
@login_required
def delete_project(project_id):
    project_to_delete = Project.query.get(project_id)

    if not project_to_delete:
        return jsonify({"status": "error", "message": "Project not found"}), 404

    # Check if project belongs to the user
    if project_to_delete.user_id != current_user.id:
        return jsonify({"status": "error", "message": "Unauthorized"}), 403

    try:
        db.session.delete(project_to_delete)
        db.session.commit()
        return jsonify({"status": "success", "message": "Project deleted"}), 200
    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 500


@Proj.route('/update_project/<int:project_id>', methods=['PUT'])
@login_required
def update_project(project_id):
    project = Project.query.get_or_404(project_id)

    # Security: Ensure only the owner can update
    if project.user_id != current_user.id:
        return jsonify({"status": "error", "message": "Unauthorized"}), 403

    data = request.get_json()
    project.fileName = data.get('name', project.fileName)
    project.jsonMapData = data.get('map_state')

    db.session.commit()

    return jsonify({
        "status": "success",
        "redirect_url": url_for('Proj.saved_files_directory')
    }), 200

@Proj.route('/api/project/<int:project_id>')
@login_required
def get_project_data(project_id):
    project = Project.query.get_or_404(project_id)
    
    return jsonify({
        "map_state": project.jsonMapData,
        "fileName": project.fileName 
    })