"""
CampusMind Expanded Data Store (data.py)
Includes 15 detailed campus locations with step-by-step turn-by-turn navigation.
"""

from datetime import datetime, timedelta

# Student Profile
STUDENT_PROFILE = {
    "name": "Alex Chen",
    "avatar": "AC",
    "major": "Computer Science & Engineering",
    "semester": 6,
    "gpa": 3.85,
    "attendance_pct": 94.2,
    "skills": ["Python", "JavaScript", "React", "Data Structures", "Machine Learning", "Git", "SQL"],
    "interests": ["Web Development", "AI/ML Applications", "Robotics", "Open Source"]
}

# 15 Detailed Campus Locations with Step-by-Step Directions
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
            "Walk straight past the security desk toward Academic Block B.",
            "Take the central staircase or North elevator up to Floor 1.",
            "Turn right down Hallway B; B-102 is the third lecture hall on your left."
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
            "Enter the CS Department Main Building.",
            "Take the main elevator or East stairwell to Floor 3.",
            "Turn left upon exiting the elevator.",
            "Door 304 (Lab-3) is opposite the department server room."
        ]
    },
    {
        "id": "loc-3",
        "name": "Lab-4 Machine Learning & AI Lab",
        "type": "Laboratory",
        "block": "CS Department Building, 3rd Floor",
        "hours": "8:30 AM - 9:00 PM",
        "directions": "Directly opposite to Lab-3 on 3rd floor CS Building, door 308.",
        "steps": [
            "Proceed to 3rd Floor of CS Department Building.",
            "Walk down the central laboratory corridor.",
            "Lab-4 (AI/ML Lab) is located at door 308, right across from Lab-3."
        ]
    },
    {
        "id": "loc-4",
        "name": "Main Campus Auditorium",
        "type": "Auditorium",
        "block": "Central Campus Plaza",
        "hours": "8:00 AM - 10:00 PM",
        "directions": "Adjacent to Student Activity Center (SAC), double glass entrance doors.",
        "steps": [
            "Walk toward the Central Campus Fountain Plaza.",
            "Head South toward the Student Activity Center wing.",
            "The Main Auditorium double glass entrance is on the right side of the plaza."
        ]
    },
    {
        "id": "loc-5",
        "name": "Central Library & 24/7 Study Pods",
        "type": "Library",
        "block": "Central Library Building",
        "hours": "Open 24/7 (Silent Pods Floor 2)",
        "directions": "Enter main Library lobby, tap ID badge, take central escalator to Floor 2.",
        "steps": [
            "Walk to the Central Library glass building next to Academic Block A.",
            "Scan your Student ID at the turnstile entrance.",
            "Take the central escalator or elevator up to Floor 2.",
            "24/7 Silent Study Pods are located in the West Wing."
        ]
    },
    {
        "id": "loc-6",
        "name": "Lab-1 Operating Systems Lab",
        "type": "Laboratory",
        "block": "CS Department Building, 2nd Floor",
        "hours": "9:00 AM - 6:00 PM",
        "directions": "CS Building Floor 2, door 202 next to Linux Systems workstation bay.",
        "steps": [
            "Enter CS Department building lobby.",
            "Take staircase to Floor 2.",
            "Turn right past the Systems Faculty notice board.",
            "Lab-1 (Door 202) is located next to the Linux server lab."
        ]
    },
    {
        "id": "loc-7",
        "name": "B-204 Software Engineering Room",
        "type": "Classroom",
        "block": "Academic Block B, 2nd Floor",
        "hours": "8:00 AM - 6:00 PM",
        "directions": "Academic Block B 2nd floor, turn left past faculty cabins, room 204.",
        "steps": [
            "Enter Academic Block B.",
            "Take elevator to Floor 2.",
            "Turn left down the main corridor past faculty offices.",
            "Room B-204 is on the right side."
        ]
    },
    {
        "id": "loc-8",
        "name": "Student Activity Center (SAC)",
        "type": "Student Hub",
        "block": "South Campus Plaza",
        "hours": "7:00 AM - 11:00 PM",
        "directions": "South Campus Quadrangle, ground floor entrance opposite central lawn.",
        "steps": [
            "Head to South Campus Lawn.",
            "Enter through the SAC main archway.",
            "Clubs desk and event lounges are on the ground floor."
        ]
    },
    {
        "id": "loc-9",
        "name": "Dean & Academic Affairs Office",
        "type": "Administrative",
        "block": "Administrative Block A, Ground Floor",
        "hours": "9:00 AM - 5:00 PM",
        "directions": "Main Administrative Building, turn right at reception desk, Room A-05.",
        "steps": [
            "Enter Main Administrative Building A.",
            "Check in at the central reception desk.",
            "Walk down the right hallway to Room A-05."
        ]
    },
    {
        "id": "loc-10",
        "name": "Robotics & Drone Hardware Lab",
        "type": "Laboratory",
        "block": "Innovation Hub, Lab Block 2",
        "hours": "9:00 AM - 10:00 PM",
        "directions": "Innovation Complex 1st Floor, enter through glass workshop doors.",
        "steps": [
            "Walk to the Innovation Hub behind the Engineering Workshops.",
            "Take elevator to 1st Floor.",
            "Robotics Hardware Lab is behind the heavy prototyping workshop."
        ]
    },
    {
        "id": "loc-11",
        "name": "Central Cafeteria & Food Court",
        "type": "Cafeteria",
        "block": "Student Plaza, Ground Floor",
        "hours": "7:30 AM - 10:30 PM",
        "directions": "Central Student Quadrangle, outdoor shaded seating area.",
        "steps": [
            "Head to Central Student Quadrangle.",
            "Food stalls and main dining hall are on the ground level."
        ]
    },
    {
        "id": "loc-12",
        "name": "Indoor Sports Complex & Gym",
        "type": "Sports",
        "block": "Athletic Complex, West Campus",
        "hours": "6:00 AM - 9:30 PM",
        "directions": "West Campus athletic grounds, adjacent to basketball courts.",
        "steps": [
            "Head West past the outdoor tennis courts.",
            "Enter the main glass doors of the Indoor Sports Complex.",
            "Gymnasium is on the ground floor, badminton courts on floor 1."
        ]
    },
    {
        "id": "loc-13",
        "name": "Seminar Hall 1 (Tech Talks)",
        "type": "Auditorium",
        "block": "Central Auditorium Wing, 1st Floor",
        "hours": "8:30 AM - 8:00 PM",
        "directions": "Main Auditorium building, take side stairs to 1st floor balcony wing.",
        "steps": [
            "Enter Main Auditorium foyer.",
            "Take side staircase up to 1st Floor Balcony wing.",
            "Seminar Hall 1 is straight ahead."
        ]
    },
    {
        "id": "loc-14",
        "name": "Examination Hall C",
        "type": "Classroom",
        "block": "Academic Block A, 3rd Floor",
        "hours": "8:00 AM - 6:00 PM",
        "directions": "Block A 3rd Floor East Wing, large double doors.",
        "steps": [
            "Enter Academic Block A.",
            "Take main elevator up to Floor 3.",
            "Walk down East Wing corridor to double doors marked Exam Hall C."
        ]
    },
    {
        "id": "loc-15",
        "name": "Placement & Career Development Cell",
        "type": "Administrative",
        "block": "Administrative Block B, 2nd Floor",
        "hours": "9:00 AM - 6:00 PM",
        "directions": "Admin Block B 2nd floor, interview suites suite 201.",
        "steps": [
            "Enter Admin Block B.",
            "Take stairs or elevator to Floor 2.",
            "Placement Cell and interview cabins are in Suite 201."
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
        "content": "Unit 3: Regularization & Overfitting Prevention\n1. L1 Regularization (Lasso): Penalty = λ ∑ |w_i|\n2. L2 Regularization (Ridge): Penalty = λ ∑ (w_i)^2\n3. Cross-Validation: Tune λ parameter to balance bias-variance tradeoff."
    },
    {
        "id": "note-2",
        "filename": "CS301_OS_Semaphores_Notes.pdf",
        "title": "CS301 - Operating Systems: Semaphores & Synchronization",
        "course_tag": "CS301",
        "uploaded_at": "2026-09-08",
        "content": "Chapter 5: Process Synchronization & Deadlock Avoidance\n1. Critical Section Requirements: Mutual Exclusion, Progress, Bounded Waiting.\n2. Binary & Counting Semaphores (wait & signal atomic ops)."
    }
]

# 10 Real-World Integrations
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
        "description": "Financial assistance for meritorious undergraduate students with annual family income below 8 LPA.",
        "required_skills": ["Computer Science", "Academic Merit"],
        "deadline": "20 Oct 2026",
        "stipend_or_prize": "₹10,000 - ₹100,000",
        "url": "https://scholarships.gov.in"
    },
    {
        "id": "opp-2",
        "title": "State Merit Scholarship",
        "category": "Scholarships",
        "organization": "Ministry of Education",
        "description": "Awarded based on top 5% academic performance in university semester examinations.",
        "required_skills": ["Academic Excellence", "GPA > 3.8"],
        "deadline": "25 Oct 2026",
        "stipend_or_prize": "₹50,000 / Year",
        "url": "https://www.education.gov.in/scholarships"
    },
    {
        "id": "opp-3",
        "title": "AI & Web Tech Internship Program",
        "category": "Internships",
        "organization": "Google & Microsoft Student Careers",
        "description": "Summer software engineering internship working on scalable AI agent applications.",
        "required_skills": ["Python", "React", "Data Structures", "Git"],
        "deadline": "15 Nov 2026",
        "stipend_or_prize": "₹45,000 / Month Stipend",
        "url": "https://careers.google.com/students/"
    },
    {
        "id": "opp-4",
        "title": "AI Thinkers Global Hackathon",
        "category": "Hackathons",
        "organization": "Devpost & Unstop Tech",
        "description": "36-hour hackathon to build generative AI solutions for campus productivity and healthcare.",
        "required_skills": ["Python", "Machine Learning", "API Integration"],
        "deadline": "12 Sep 2026",
        "stipend_or_prize": "₹2,50,000 Prize Pool",
        "url": "https://unstop.com/hackathons"
    }
]

# YouTube Tutorials
YOUTUBE_TUTORIALS = [
    {
        "id": "yt-1",
        "course": "CS304 - Machine Learning",
        "topic": "L1 (Lasso) vs L2 (Ridge) Regularization Explained",
        "channel": "StatQuest with Josh Starmer",
        "duration": "14:20",
        "views": "1.2M views",
        "url": "https://www.youtube.com/watch?v=Q81RR3yKnbc"
    },
    {
        "id": "yt-2",
        "course": "CS301 - Operating Systems",
        "topic": "Process Synchronization, Semaphores & Mutexes",
        "channel": "Neso Academy",
        "duration": "18:45",
        "views": "850K views",
        "url": "https://www.youtube.com/watch?v=ukM_zzrIeXs"
    }
]

# Timetable
TIMETABLE = [
    {
        "day": "Monday",
        "classes": [
            {"time": "10:00 AM", "course": "DBMS Class", "room": "B-102", "instructor": "Dr. Ramesh Gupta", "code": "CS302"},
            {"time": "12:00 PM", "course": "Project Meeting", "room": "Lab-3", "instructor": "Prof. Grace Hopper", "code": "CS308"},
            {"time": "03:00 PM", "course": "Hackathon Prep", "room": "Online", "instructor": "AI Thinkers Club", "code": "CLUB"}
        ]
    },
    {
        "day": "Tuesday",
        "classes": [
            {"time": "09:00 AM", "course": "Operating Systems", "room": "Hall B", "instructor": "Dr. Sarah Jenkins", "code": "CS301"},
            {"time": "11:00 AM", "course": "Machine Learning", "room": "Lab 4", "instructor": "Prof. Alan Turing", "code": "CS304"}
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
        "description": "Design ER Diagram and normalization up to BCNF for hospital management system.",
        "subtasks": [
            {"id": "task-101", "title": "Identify Entities & Relationships", "status": "Completed", "estimated_hours": 1.0},
            {"id": "task-102", "title": "Draw ER Diagram in StarUML/Figma", "status": "Completed", "estimated_hours": 1.5},
            {"id": "task-103", "title": "Convert ER diagram to Relational Schema", "status": "Pending", "estimated_hours": 1.5}
        ]
    }
]

# Campus Events
CAMPUS_EVENTS = [
    {
        "id": "evt-1",
        "title": "AI Thinkers Hackathon",
        "date": "12 Sep 2026",
        "location": "IIIT Hyderabad / Auditorium 1",
        "category": "Events",
        "organizer": "AI Club",
        "description": "Build innovative generative AI prototypes in 36 hours. Free food and mentors provided.",
        "action": "Register",
        "url": "https://unstop.com/hackathons"
    }
]

# Lab Exams
LAB_EXAMS = [
    {
        "course": "CS301 - Operating Systems",
        "viva_questions": ["What is binary semaphore?", "Explain Peterson algorithm."],
        "past_paper_topics": ["FCFS Numerical", "Bankers Algorithm"]
    }
]

# Career Roadmaps
CAREER_ROADMAPS = [
    {
        "role": "AI / ML Engineer",
        "description": "Master machine learning algorithms, deep learning models, and LLM agent orchestration.",
        "steps": ["Phase 1: Python Mastery", "Phase 2: ML & Scikit-Learn", "Phase 3: Deep Learning", "Phase 4: LLMs & Agents"]
    }
]

# Projects
PROJECTS = [
    {
        "title": "CampusMind AI Student Co-Pilot",
        "category": "AI / Web",
        "tags": ["React", "Flask", "Python", "LLM Agent"],
        "description": "Context-aware student dashboard assistant with tool execution loops and PDF grounding.",
        "looking_for": "UI/UX Designer & Backend Developer"
    }
]

# Mentors
MENTORS = [
    {
        "name": "Dr. Sarah Jenkins",
        "role": "Associate Professor (OS & Systems)",
        "expertise": ["Operating Systems", "Distributed Systems"],
        "available_slots": "Wednesdays 3:00 PM - 5:00 PM"
    }
]

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
