"""
EduMitra AI Flask Backend Server (app.py)
Integrates Firestore DB, OpenRouter AI, Exa Search, and 10 Real-World Services.
"""

import os
from flask import Flask, request, jsonify, render_template, send_from_directory
from flask_cors import CORS

import data
import tools
import agent

app = Flask(__name__, static_folder="../frontend", template_folder="../frontend")
CORS(app)

# Serve Frontend SPA
@app.route('/')
def serve_index():
    return send_from_directory('../frontend', 'index.html')

@app.route('/<path:path>')
def serve_static(path):
    if os.path.exists(os.path.join('../frontend', path)):
        return send_from_directory('../frontend', path)
    return send_from_directory('../frontend', 'index.html')

# Health Check API
@app.route('/api/health', methods=['GET'])
def health_check():
    return jsonify({
        "status": "healthy",
        "service": "EduMitra AI Platform",
        "tagline": "Your AI Friend. Your Future.",
        "sub_tagline": "Plan Smarter | Learn Better | Do More | Together",
        "version": "2.0.0",
        "firestore_status": "connected",
        "modules_active": 13
    })

# User Auth API
@app.route('/auth/register', methods=['POST'])
def register_user():
    req_data = request.json or {}
    email = req_data.get('email')
    name = req_data.get('name', 'Student')
    major = req_data.get('major', 'Computer Science')
    password = req_data.get('password')

    if not email:
        return jsonify({"error": "Email is required"}), 400

    user = data.register_user_in_db(name, email, major, password)
    return jsonify({
        "success": True,
        "message": f"User '{user['name']}' registered successfully!",
        "user": user
    })

@app.route('/auth/login', methods=['POST'])
def login_user():
    req_data = request.json or {}
    email = req_data.get('email')
    password = req_data.get('password')

    if not email:
        return jsonify({"error": "Email is required"}), 400

    user = data.login_user_in_db(email, password)
    return jsonify({
        "success": True,
        "message": f"User '{user['name']}' logged in!",
        "user": user
    })

@app.route('/user/profile', methods=['GET'])
def get_user_profile():
    return jsonify({"user": data.STUDENT_PROFILE})

# Timetable
@app.route('/timetable', methods=['GET'])
def get_timetable_endpoint():
    day = request.args.get('day', 'Monday')
    return jsonify(tools.tool_get_timetable(day))

# Dashboard Summary
@app.route('/dashboard', methods=['GET'])
def get_dashboard_summary():
    student = data.STUDENT_PROFILE
    timetable = tools.tool_get_timetable("Monday")
    assignments = tools.tool_get_assignments()
    notes = tools.tool_search_notes("Machine Learning")
    opps = tools.tool_get_opportunities()

    return jsonify({
        "student": student,
        "today_day": "Monday",
        "today_classes": timetable.get("classes", []),
        "urgent_assignments": assignments.get("assignments", [])[:3],
        "pending_subtask_count": sum(len([t for t in a.get("subtasks", []) if t.get("status") != "Completed"]) for a in assignments.get("assignments", [])),
        "recent_notes": notes.get("results", [])[:3],
        "opportunities": opps.get("opportunities", [])[:3]
    })

# Assignments
@app.route('/assignments', methods=['GET'])
def list_assignments():
    return jsonify({"assignments": data.get_all_assignments(), "count": len(data.get_all_assignments())})

@app.route('/assignments', methods=['POST'])
def add_assignment_endpoint():
    req_data = request.json or {}
    new_asgn = data.add_new_assignment(
        req_data.get('title', 'New Assignment'),
        req_data.get('course', 'CS301'),
        req_data.get('due_date', '28 Sep 2026'),
        req_data.get('priority', 'High'),
        req_data.get('description', '')
    )
    return jsonify({"success": True, "assignment": new_asgn})

@app.route('/assignments/<asgn_id>', methods=['PATCH'])
def update_assignment(asgn_id):
    req_data = request.json or {}
    task_id = req_data.get('task_id')
    new_status = req_data.get('status')
    if task_id and new_status:
        success, parent_asgn, updated_task = data.update_subtask_status(task_id, new_status)
        if success: return jsonify({"success": True, "assignment": parent_asgn, "task": updated_task})
        return jsonify({"error": f"Task {task_id} not found"}), 404
    asgn = data.get_assignment_by_id(asgn_id)
    if not asgn: return jsonify({"error": f"Assignment {asgn_id} not found"}), 404
    if "status" in req_data: asgn["status"] = req_data["status"]
    if "priority" in req_data: asgn["priority"] = req_data["priority"]
    return jsonify({"success": True, "assignment": asgn})

# AI Agent Chat
@app.route('/agent/chat', methods=['POST'])
def agent_chat():
    req_data = request.json or {}
    user_message = req_data.get('message', '')
    history = req_data.get('history', [])
    if not user_message.strip(): return jsonify({"error": "Empty message"}), 400
    return jsonify(agent.execute_agent_turn(user_message, history))

# Notes
@app.route('/notes/upload', methods=['POST'])
def upload_notes():
    req_data = request.json or {}
    filename = req_data.get('filename', 'Manual_Note.txt')
    course_tag = req_data.get('course_tag', 'General')
    title = req_data.get('title', filename)
    text_content = req_data.get('content', '')
    new_note = data.add_new_note(title, course_tag, text_content, filename)
    return jsonify({"success": True, "note": new_note})

@app.route('/notes', methods=['GET'])
def list_notes():
    return jsonify({"notes": data.NOTES, "count": len(data.NOTES)})

# Opportunities & Integrations
@app.route('/opportunities', methods=['GET'])
def get_opportunities_endpoint():
    return jsonify(tools.tool_get_opportunities(request.args.get('type') or request.args.get('category'), request.args.get('q')))

@app.route('/integrations', methods=['GET'])
def get_integrations_endpoint():
    return jsonify({"integrations": data.INTEGRATIONS, "count": len(data.INTEGRATIONS)})

@app.route('/integrations/sync', methods=['POST'])
def sync_integration_endpoint():
    req_data = request.json or {}
    service_id = req_data.get('service_id', 'gcal')
    return jsonify(tools.tool_sync_integration(service_id))

@app.route('/youtube/learning', methods=['GET'])
def get_youtube_learning_endpoint():
    return jsonify(tools.tool_get_youtube_learning(request.args.get('topic')))

@app.route('/campus/map', methods=['GET'])
def get_campus_map_endpoint(): return jsonify(tools.tool_get_campus_map(request.args.get('location')))

@app.route('/community/events', methods=['GET'])
def get_community_events_endpoint(): return jsonify(tools.tool_get_community_events(request.args.get('category')))

@app.route('/career/roadmap', methods=['GET'])
def get_career_roadmap_endpoint(): return jsonify(tools.tool_get_career_roadmap(request.args.get('role')))

@app.route('/lab/prep', methods=['GET'])
def get_lab_prep_endpoint(): return jsonify(tools.tool_get_lab_exam_prep(request.args.get('course')))

@app.route('/projects', methods=['GET'])
def get_projects_endpoint(): return jsonify(tools.tool_get_projects(request.args.get('category')))

@app.route('/mentorship', methods=['GET'])
def get_mentorship_endpoint(): return jsonify(tools.tool_get_mentorship(request.args.get('topic')))

if __name__ == '__main__':
    port = int(os.getenv("PORT", 5000))
    print(f"EduMitra AI Full Platform & Database Server running on http://127.0.0.1:{port}")
    app.run(host='0.0.0.0', port=port, debug=False)
