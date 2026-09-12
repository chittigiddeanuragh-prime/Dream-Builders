"""
CampusMind Full Tools Suite (tools.py)
Includes Integrations Hub & Real-World Sync Tools + Exa AI Live Opportunities Search.
"""

import os
import json
from datetime import datetime
import data

# Load .env file if available
env_path = os.path.join(os.path.dirname(__file__), '.env')
if os.path.exists(env_path):
    with open(env_path, 'r') as f:
        for line in f:
            if '=' in line and not line.startswith('#'):
                k, v = line.strip().split('=', 1)
                os.environ[k] = v

try:
    from exa_py import Exa
except ImportError:
    Exa = None

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

def _exa_search_opportunities(category=None, query=None):
    api_key = os.environ.get("EXA_API_KEY")
    if not api_key or not Exa:
        return None

    student = getattr(data, "STUDENT_PROFILE", {})
    skills_str = " ".join(student.get("skills", []))
    major_str = student.get("major", "")
    category_term = category if category else "scholarship internship hackathon competition"
    q_term = query if query else ""
    query_str = f"{category_term} for {major_str} student {skills_str} {q_term}".strip()

    try:
        exa = Exa(api_key=api_key)
        res = exa.search(
            query_str,
            type="auto",
            num_results=8,
            contents={"highlights": True}
        )
        results = getattr(res, "results", [])
        if not results:
            return None

        mapped = []
        for idx, item in enumerate(results):
            title = getattr(item, "title", None) or "Global Opportunity"
            url = getattr(item, "url", "#")
            highlights = getattr(item, "highlights", [])
            desc = highlights[0] if highlights else title

            try:
                from urllib.parse import urlparse
                domain = urlparse(url).netloc.replace("www.", "")
            except Exception:
                domain = "Official Site"

            mapped.append({
                "id": getattr(item, "id", f"exa-{idx+1}"),
                "title": title,
                "category": category.capitalize() if category else "Opportunity",
                "organization": domain.capitalize() if domain else "Official Sponsor",
                "description": desc,
                "deadline": "See Official Portal",
                "stipend_or_prize": "Stipend / Prize Available",
                "required_skills": student.get("skills", ["Computer Science"])[:3],
                "url": url
            })
        return mapped
    except Exception as e:
        print(f"[Exa API Fallback Triggered]: {e}")
        return None

def tool_get_opportunities(category=None, query=None):
    exa_results = _exa_search_opportunities(category, query)
    if exa_results is not None and len(exa_results) > 0:
        raw_opps = exa_results
        source = "live"
    else:
        raw_opps = data.OPPORTUNITIES
        source = "seed"

    student = getattr(data, "STUDENT_PROFILE", {})
    student_skills = student.get("skills", [])
    results = []
    cat_lower = category.lower() if category else ""
    q_lower = query.lower() if query else ""

    for idx, opp in enumerate(raw_opps):
        opp_cat = opp.get("category", "").lower() or opp.get("type", "").lower()
        opp_title = opp.get("title", "").lower()
        opp_desc = opp.get("description", "").lower()

        # Apply category and text query filtering for both seed and live results
        if cat_lower and cat_lower not in opp_cat and cat_lower not in opp_title and cat_lower not in opp_desc:
            continue
        if q_lower and q_lower not in opp_title and q_lower not in opp_desc:
            continue

        req_skills = opp.get("required_skills", ["Computer Science"])
        matched_skills = [s for s in req_skills if any(s.lower() in st.lower() or st.lower() in s.lower() for st in student_skills)]
        missing_skills = [s for s in req_skills if s not in matched_skills]
        match_score = int((len(matched_skills) / len(req_skills)) * 100) if req_skills else 100

        results.append({
            "id": opp.get("id", f"opp-{idx+1}"),
            "title": opp.get("title", "Opportunity"),
            "category": opp.get("category", category.capitalize() if category else "Scholarships"),
            "organization": opp.get("organization", "Global Program"),
            "description": opp.get("description", ""),
            "deadline": opp.get("deadline", "Open Registration"),
            "stipend_or_prize": opp.get("stipend_or_prize", "Funding Available"),
            "required_skills": req_skills,
            "matched_skills": matched_skills,
            "missing_skills": missing_skills,
            "match_score": match_score,
            "url": opp.get("url", "#")
        })

    return {"opportunities": results, "count": len(results), "source": source}

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
