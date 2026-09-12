"""
CampusMind Full Tools Suite (tools.py)
Includes Integrations Hub & Real-World Sync Tools.
"""

import json
from datetime import datetime
import data

def tool_get_timetable(day=None):
    if day:
        day_clean = day.strip().capitalize()
        for d in data.TIMETABLE:
            if d["day"] == day_clean:
                return {"day": d["day"], "classes": d["classes"]}
        return {"error": f"No classes found for {day}"}
    return {"timetable": data.TIMETABLE}

def tool_get_assignments(status=None, course=None):
    assignments = data.get_all_assignments()
    filtered = []
    for a in assignments:
        if status and a["status"].lower() != status.lower():
            continue
        if course and course.lower() not in a["course"].lower() and course.lower() not in a["course_name"].lower():
            continue
        filtered.append(a)
    return {"assignments": filtered, "count": len(filtered)}

def tool_get_assignment_detail(assignment_id):
    asgn = data.get_assignment_by_id(assignment_id)
    if not asgn:
        return {"error": f"Assignment '{assignment_id}' not found."}
    return {"assignment": asgn}

def tool_create_assignment_plan(assignment_id, subtasks):
    if isinstance(subtasks, str):
        subtasks = [s.strip() for s in subtasks.split(",") if s.strip()]
    success, result = data.add_subtasks_to_assignment(assignment_id, subtasks)
    if not success:
        return {"error": result}
    asgn = data.get_assignment_by_id(assignment_id)
    return {
        "success": True,
        "message": f"Added {len(result)} subtasks to '{asgn['title']}'",
        "assignment_id": assignment_id,
        "created_subtasks": result,
        "updated_assignment": asgn
    }

def tool_update_task_status(task_id, status):
    valid_statuses = ["Completed", "In Progress", "Pending"]
    clean_status = status.title()
    if clean_status not in valid_statuses:
        clean_status = "Completed" if "complete" in status.lower() or "done" in status.lower() else "Pending"
    success, parent_asgn, updated_task = data.update_subtask_status(task_id, clean_status)
    if not success:
        return {"error": f"Subtask '{task_id}' not found."}
    return {
        "success": True,
        "task_id": task_id,
        "new_status": clean_status,
        "task_title": updated_task["title"],
        "parent_assignment": parent_asgn["title"]
    }

def tool_search_notes(query, course_tag=None):
    results = []
    q_lower = query.lower() if query else ""
    notes_list = getattr(data, "NOTES", [])
    for note in notes_list:
        if course_tag and course_tag.lower() not in note["course_tag"].lower():
            continue
        content = note["content"]
        if not q_lower or q_lower in content.lower() or q_lower in note["title"].lower():
            idx = content.lower().find(q_lower) if q_lower else 0
            start = max(0, idx - 50)
            end = min(len(content), idx + 250)
            snippet = content[start:end].replace('\n', ' ').strip()
            results.append({
                "note_id": note["id"],
                "filename": note["filename"],
                "title": note["title"],
                "course_tag": note["course_tag"],
                "snippet": f"...{snippet}..." if idx > 0 else snippet
            })
    return {"results": results, "match_count": len(results)}

def tool_generate_study_plan(course, exam_date, topics=None):
    if isinstance(topics, str):
        topics = [t.strip() for t in topics.split(",") if t.strip()]
    if not topics:
        topics = ["Core Concepts & Definitions", "Problem Solving & Examples", "Past Paper Questions"]
    plan_days = []
    for day_i in range(1, 6):
        topic_idx = (day_i - 1) % len(topics)
        plan_days.append({
            "day": f"Day {day_i}",
            "focus_topic": topics[topic_idx],
            "recommended_hours": 2
        })
    return {"course": course, "exam_date": exam_date, "study_plan": plan_days}

def tool_get_opportunities(category=None, query=None):
    student = data.STUDENT_PROFILE
    opps = data.OPPORTUNITIES
    results = []
    cat_lower = category.lower() if category else ""
    q_lower = query.lower() if query else ""
    for opp in opps:
        if cat_lower and cat_lower not in opp["category"].lower():
            continue
        if q_lower and q_lower not in opp["title"].lower() and q_lower in opp["description"].lower():
            continue
        req_skills = opp["required_skills"]
        student_skills = student["skills"]
        matched_skills = [s for s in req_skills if any(s.lower() in st.lower() or st.lower() in s.lower() for st in student_skills)]
        missing_skills = [s for s in req_skills if s not in matched_skills]
        match_score = int((len(matched_skills) / len(req_skills)) * 100) if req_skills else 100
        results.append({
            "id": opp["id"],
            "title": opp["title"],
            "category": opp["category"],
            "organization": opp["organization"],
            "description": opp["description"],
            "deadline": opp["deadline"],
            "stipend_or_prize": opp["stipend_or_prize"],
            "required_skills": req_skills,
            "matched_skills": matched_skills,
            "missing_skills": missing_skills,
            "match_score": match_score
        })
    return {"opportunities": results, "count": len(results)}

# Real-World Integration Tools

def tool_get_integrations():
    """Get status of 10 real-world integrations (GCal, Teams, Slack, ERP, Notion, Gmail, GDrive, GitHub, YouTube, LinkedIn)."""
    return {"integrations": data.INTEGRATIONS}

def tool_sync_integration(service_id):
    """Trigger real-world sync for Google Calendar, Notion, ERP, GitHub, Slack, etc."""
    success, item = data.sync_integration_service(service_id)
    if success:
        return {
            "success": True,
            "message": f"Successfully synced {item['name']}! {item['synced_count']}",
            "integration": item
        }
    return {"error": f"Integration service '{service_id}' not found."}

def tool_get_youtube_learning(topic=None):
    """Fetch curated video tutorials from YouTube Learning for course topics."""
    tutorials = data.YOUTUBE_TUTORIALS
    if topic:
        t_lower = topic.lower()
        matched = [t for t in tutorials if t_lower in t["topic"].lower() or t_lower in t["course"].lower()]
        if matched:
            return {"tutorials": matched}
    return {"tutorials": tutorials}

# Additional Module Tools
def tool_get_campus_map(location=None):
    return {"locations": data.CAMPUS_MAP}

def tool_get_community_events(category=None):
    return {"events": data.CAMPUS_EVENTS}

def tool_get_career_roadmap(role=None):
    return {"roadmaps": data.CAREER_ROADMAPS}

def tool_get_lab_exam_prep(course=None):
    return {"lab_preps": data.LAB_EXAMS}

def tool_get_projects(category=None):
    return {"projects": data.PROJECTS}

def tool_get_mentorship(topic=None):
    return {"mentors": data.MENTORS}

# Tool Dispatcher
TOOL_FUNCTIONS = {
    "get_timetable": tool_get_timetable,
    "get_assignments": tool_get_assignments,
    "get_assignment_detail": tool_get_assignment_detail,
    "create_assignment_plan": tool_create_assignment_plan,
    "update_task_status": tool_update_task_status,
    "search_notes": tool_search_notes,
    "generate_study_plan": tool_generate_study_plan,
    "get_opportunities": tool_get_opportunities,
    "get_integrations": tool_get_integrations,
    "sync_integration": tool_sync_integration,
    "get_youtube_learning": tool_get_youtube_learning,
    "get_campus_map": tool_get_campus_map,
    "get_community_events": tool_get_community_events,
    "get_career_roadmap": tool_get_career_roadmap,
    "get_lab_exam_prep": tool_get_lab_exam_prep,
    "get_projects": tool_get_projects,
    "get_mentorship": tool_get_mentorship
}

TOOL_DECLARATIONS = [
    {"type": "function", "function": {"name": "get_timetable", "description": "Fetch class schedule.", "parameters": {"type": "object", "properties": {"day": {"type": "string"}}}}},
    {"type": "function", "function": {"name": "get_assignments", "description": "Get upcoming assignments.", "parameters": {"type": "object", "properties": {"status": {"type": "string"}, "course": {"type": "string"}}}}},
    {"type": "function", "function": {"name": "create_assignment_plan", "description": "Break down assignment.", "parameters": {"type": "object", "properties": {"assignment_id": {"type": "string"}, "subtasks": {"type": "array", "items": {"type": "string"}}}, "required": ["assignment_id", "subtasks"]}}},
    {"type": "function", "function": {"name": "update_task_status", "description": "Update subtask.", "parameters": {"type": "object", "properties": {"task_id": {"type": "string"}, "status": {"type": "string"}}, "required": ["task_id", "status"]}}},
    {"type": "function", "function": {"name": "search_notes", "description": "Search course notes.", "parameters": {"type": "object", "properties": {"query": {"type": "string"}}, "required": ["query"]}}},
    {"type": "function", "function": {"name": "get_opportunities", "description": "Search scholarships/internships/hackathons.", "parameters": {"type": "object", "properties": {"category": {"type": "string"}}}}},
    {"type": "function", "function": {"name": "get_integrations", "description": "Get 10 real-world integrations status (GCal, Teams, Notion, ERP, GitHub).", "parameters": {"type": "object", "properties": {}}}},
    {"type": "function", "function": {"name": "sync_integration", "description": "Sync Google Calendar, Notion, College ERP, GitHub, Slack, etc.", "parameters": {"type": "object", "properties": {"service_id": {"type": "string"}}, "required": ["service_id"]}}},
    {"type": "function", "function": {"name": "get_youtube_learning", "description": "Fetch YouTube learning videos for courses.", "parameters": {"type": "object", "properties": {"topic": {"type": "string"}}}}},
    {"type": "function", "function": {"name": "get_campus_map", "description": "Find campus classrooms & labs.", "parameters": {"type": "object", "properties": {"location": {"type": "string"}}}}},
    {"type": "function", "function": {"name": "get_community_events", "description": "Get campus events & clubs.", "parameters": {"type": "object", "properties": {"category": {"type": "string"}}}}},
    {"type": "function", "function": {"name": "get_career_roadmap", "description": "Get career roadmaps.", "parameters": {"type": "object", "properties": {"role": {"type": "string"}}}}},
    {"type": "function", "function": {"name": "get_lab_exam_prep", "description": "Get lab viva questions.", "parameters": {"type": "object", "properties": {"course": {"type": "string"}}}}}
]
