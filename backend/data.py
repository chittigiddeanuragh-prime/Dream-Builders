"""
CampusMind Expanded Data Store (data.py)
Includes full database persistence for registered users (USERS_DB).
"""

from datetime import datetime, timedelta

# User Database Store (Persists all registered users)
USERS_DB = [
    {
        "uid": "user_alex_chen",
        "name": "Alex Chen",
        "email": "alex.chen@campusminds.edu",
        "major": "Computer Science & Engineering",
        "semester": 6,
        "gpa": 3.85,
        "attendance_pct": 94.2,
        "createdAt": "2026-09-01 10:00:00"
    }
]

# Active Student Profile
STUDENT_PROFILE = USERS_DB[0]

def register_user_in_db(name, email, major, password):
    # Check if user already exists
    for u in USERS_DB:
        if u["email"].lower() == email.lower():
            u["name"] = name
            u["major"] = major
            u["lastLogin"] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            return u
    
    new_user = {
        "uid": f"user_{len(USERS_DB)+1}_{int(datetime.now().timestamp())}",
        "name": name or "Student",
        "email": email,
        "major": major or "Computer Science",
        "semester": 6,
        "gpa": 3.85,
        "attendance_pct": 94.2,
        "createdAt": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "lastLogin": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    }
    USERS_DB.append(new_user)
    global STUDENT_PROFILE
    STUDENT_PROFILE = new_user
    return new_user

def login_user_in_db(email, password):
    for u in USERS_DB:
        if u["email"].lower() == email.lower():
            u["lastLogin"] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            global STUDENT_PROFILE
            STUDENT_PROFILE = u
            return u
    
    # Auto-provision user if logging in first time
    name = email.split('@')[0].capitalize()
    return register_user_in_db(name, email, "Computer Science", password)

# 15 Campus Locations
CAMPUS_MAP = [
    {
        "id": "loc-1",
        "name": "B-102 DBMS Lecture Hall",
        "type": "Classroom",
        "block": "Academic Block B, 1st Floor",
        "hours": "8:00 AM - 6:00 PM",
        "directions": "Take main staircase next to lobby, turn right down Hallway B, door 102 on left.",
        "steps": [
            "Start at Main Campus Entrance / Central Lobby.",
            "Walk straight past security desk toward Academic Block B.",
            "Take central staircase or North elevator to Floor 1.",
            "Turn right down Hallway B; B-102 is third lecture hall on left."
        ]
    },
    {
        "id": "loc-2",
        "name": "Lab-3 Web Technologies Lab",
        "type": "Laboratory",
        "block": "CS Department Building, 3rd Floor",
        "hours": "9:00 AM - 7:00 PM",
        "directions": "Enter CS Department, take elevator to 3rd floor, door 304 opposite server room.",
        "steps": [
            "Enter CS Department Main Building.",
            "Take elevator to Floor 3.",
            "Turn left; door 304 is opposite the server room."
        ]
    }
]

# Course Notes
NOTES = [
    {
        "id": "note-1",
        "filename": "CS304_Unit3_ML_Regularization.pdf",
        "title": "CS304 - Machine Learning: L1 & L2 Regularization",
        "course_tag": "CS304",
        "uploaded_at": "2026-09-10",
        "content": "Unit 3: Regularization & Overfitting Prevention\n1. L1 Regularization (Lasso): Penalty = λ ∑ |w_i|\n2. L2 Regularization (Ridge): Penalty = λ ∑ (w_i)^2\n3. Cross-Validation: Tune λ parameter."
    }
]

# 10 Integrations
INTEGRATIONS = [
    {
        "id": "gcal",
        "name": "Google Calendar",
        "category": "Productivity",
        "status": "Connected",
        "icon": "fa-calendar-days",
        "color": "text-blue-400 border-blue-500/40 bg-blue-950/40",
        "last_sync": "Just now",
        "synced_count": "15 Events (Timetable + Deadlines)",
        "action": "Open Google Calendar",
        "url": "https://calendar.google.com"
    },
    {
        "id": "teams",
        "name": "Microsoft Teams",
        "category": "Communication",
        "status": "Connected",
        "icon": "fa-people-group",
        "color": "text-indigo-400 border-indigo-500/40 bg-indigo-950/40",
        "last_sync": "10 mins ago",
        "synced_count": "3 Online Class Links Active",
        "action": "Open MS Teams",
        "url": "https://teams.microsoft.com"
    },
    {
        "id": "slack",
        "name": "Slack",
        "category": "Communication",
        "status": "Connected",
        "icon": "fa-hashtag",
        "color": "text-emerald-400 border-emerald-500/40 bg-emerald-950/40",
        "last_sync": "1 hour ago",
        "synced_count": "4 Club Channels (AI & Robotics)",
        "action": "Open Slack",
        "url": "https://slack.com"
    },
    {
        "id": "erp",
        "name": "College ERP/Portal",
        "category": "University",
        "status": "Connected",
        "icon": "fa-building-columns",
        "color": "text-cyan-400 border-cyan-500/40 bg-cyan-950/40",
        "last_sync": "Today 08:00 AM",
        "synced_count": "94.2% Attendance • GPA 3.85",
        "action": "Open ERP Portal",
        "url": "https://www.education.gov.in"
    },
    {
        "id": "notion",
        "name": "Notion",
        "category": "Notes",
        "status": "Connected",
        "icon": "fa-note-sticky",
        "color": "text-slate-200 border-slate-500/40 bg-slate-900/60",
        "last_sync": "2 hours ago",
        "synced_count": "6 Exam Plans & Summaries",
        "action": "Open Notion",
        "url": "https://www.notion.so"
    },
    {
        "id": "gmail",
        "name": "Gmail",
        "category": "Email",
        "status": "Connected",
        "icon": "fa-envelope",
        "color": "text-rose-400 border-rose-500/40 bg-rose-950/40",
        "last_sync": "15 mins ago",
        "synced_count": "12 Official Announcements",
        "action": "Open Gmail",
        "url": "https://mail.google.com"
    },
    {
        "id": "gdrive",
        "name": "Google Drive",
        "category": "Storage",
        "status": "Connected",
        "icon": "fa-hard-drive",
        "color": "text-amber-400 border-amber-500/40 bg-amber-950/40",
        "last_sync": "Today 11:00 AM",
        "synced_count": "8 Course PDFs & Datasets",
        "action": "Open Google Drive",
        "url": "https://drive.google.com"
    },
    {
        "id": "github",
        "name": "GitHub",
        "category": "Developer",
        "status": "Connected",
        "icon": "fa-code-branch",
        "color": "text-purple-400 border-purple-500/40 bg-purple-950/40",
        "last_sync": "30 mins ago",
        "synced_count": "5 Active Repositories",
        "action": "Open GitHub",
        "url": "https://github.com"
    },
    {
        "id": "youtube",
        "name": "YouTube Learning",
        "category": "Education",
        "status": "Connected",
        "icon": "fa-circle-play",
        "color": "text-red-400 border-red-500/40 bg-red-950/40",
        "last_sync": "Active",
        "synced_count": "Curated Video Playlists",
        "action": "Open YouTube",
        "url": "https://www.youtube.com/learning"
    },
    {
        "id": "linkedin",
        "name": "LinkedIn",
        "category": "Career",
        "status": "Connected",
        "icon": "fa-link",
        "color": "text-blue-500 border-blue-500/40 bg-blue-950/40",
        "last_sync": "Yesterday",
        "synced_count": "Profile Skills & Job Alerts",
        "action": "Open LinkedIn",
        "url": "https://www.linkedin.com"
    }
]

# Opportunities
OPPORTUNITIES = [
    {
        "id": "opp-1",
        "title": "Central Sector Scholarship",
        "category": "Scholarships",
        "organization": "National Scholarship Portal",
        "description": "Financial assistance for meritorious undergraduate students.",
        "required_skills": ["Computer Science", "Academic Merit"],
        "deadline": "20 Oct 2026",
        "stipend_or_prize": "₹10,000 - ₹100,000",
        "url": "https://scholarships.gov.in"
    }
]

# YouTube Tutorials
YOUTUBE_TUTORIALS = [
    {
        "id": "yt-1",
        "course": "CS304 - Machine Learning",
        "topic": "L1 (Lasso) vs L2 (Ridge) Regularization",
        "channel": "StatQuest",
        "duration": "14:20",
        "views": "1.2M views",
        "url": "https://www.youtube.com/watch?v=Q81RR3yKnbc"
    }
]

# Timetable
TIMETABLE = [
    {
        "day": "Monday",
        "classes": [
            {"time": "10:00 AM", "course": "DBMS Class", "room": "B-102", "instructor": "Dr. Ramesh Gupta", "code": "CS302"},
            {"time": "12:00 PM", "course": "Project Meeting", "room": "Lab-3", "instructor": "Prof. Grace Hopper", "code": "CS308"}
        ]
    }
]

# Assignments Store
now = datetime.now()
ASSIGNMENTS = [
    {
        "id": "asgn-1",
        "title": "DBMS Assignment",
        "course": "CS302",
        "course_name": "Database Management Systems",
        "due_date": (now + timedelta(days=2)).strftime("%d %b %Y"),
        "days_left": 2,
        "priority": "High",
        "status": "In Progress",
        "remaining_hours": 4,
        "description": "Design ER Diagram and normalization.",
        "subtasks": []
    }
]

CAMPUS_EVENTS = []
LAB_EXAMS = []
CAREER_ROADMAPS = []
PROJECTS = []
MENTORS = []

def get_all_assignments(): return ASSIGNMENTS
def get_assignment_by_id(asgn_id): return next((a for a in ASSIGNMENTS if a["id"] == asgn_id), None)
def add_new_assignment(title, course, due_date, priority, description):
    new_asgn = {"id": f"asgn-{len(ASSIGNMENTS)+1}", "title": title, "course": course, "course_name": course, "due_date": due_date, "days_left": 7, "priority": priority or "Medium", "status": "Not Started", "remaining_hours": 6, "description": description or title, "subtasks": []}
    ASSIGNMENTS.append(new_asgn)
    return new_asgn

def add_new_note(title, course_tag, content, filename=None):
    new_note = {"id": f"note-{len(NOTES)+1}", "filename": filename or f"{course_tag}_Note.txt", "title": title or f"{course_tag} Note", "course_tag": course_tag or "General", "uploaded_at": datetime.now().strftime("%Y-%m-%d"), "content": content}
    NOTES.append(new_note)
    return new_note

def update_subtask_status(task_id, new_status):
    for a in ASSIGNMENTS:
        for t in a.get("subtasks", []):
            if t["id"] == task_id:
                t["status"] = new_status
                return True, a, t
    return False, None, None

def add_subtasks_to_assignment(asgn_id, subtask_titles):
    asgn = get_assignment_by_id(asgn_id)
    if not asgn: return False, "Assignment not found"
    new_subtasks = [{"id": f"task-{asgn_id.replace('asgn-', '')}{101+i}", "title": title, "status": "Pending", "estimated_hours": 1.5} for i, title in enumerate(subtask_titles)]
    asgn["subtasks"].extend(new_subtasks)
    return True, new_subtasks

def sync_integration_service(service_id):
    for item in INTEGRATIONS:
        if item["id"] == service_id or service_id.lower() in item["name"].lower():
            item["status"] = "Connected"
            item["last_sync"] = datetime.now().strftime("%H:%M:%S")
            return True, item
    return False, None
