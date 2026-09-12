"""
CampusMind Expanded Data Store (data.py)
Includes full database persistence for registered users, official brand logos, and visual images for all modules.
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
        "skills": ["Python", "JavaScript", "React", "Data Structures", "Machine Learning", "Git", "SQL"],
        "createdAt": "2026-09-01 10:00:00"
    }
]

# Active Student Profile
STUDENT_PROFILE = USERS_DB[0]

def register_user_in_db(name, email, major, password):
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
        "skills": ["Python", "JavaScript", "React", "Data Structures", "Machine Learning", "Git", "SQL"],
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
    name = email.split('@')[0].capitalize()
    return register_user_in_db(name, email, "Computer Science", password)

# 1. 15 Campus Locations with Visual Preview Images
CAMPUS_MAP = [
    {
        "id": "loc-1",
        "name": "B-102 DBMS Lecture Hall",
        "type": "Classroom",
        "block": "Academic Block B, 1st Floor",
        "hours": "8:00 AM - 6:00 PM",
        "image_url": "https://images.unsplash.com/photo-1562774053-701939374585?auto=format&fit=crop&w=600&q=80",
        "directions": "Take main staircase next to lobby, turn right down Hallway B, door 102 on left.",
        "steps": ["Start at Main Campus Lobby.", "Walk straight toward Academic Block B.", "Take staircase to 1st Floor.", "Turn right to B-102."]
    },
    {
        "id": "loc-2",
        "name": "Lab-3 Web Technologies Lab",
        "type": "Laboratory",
        "block": "CS Department Building, 3rd Floor",
        "hours": "9:00 AM - 7:00 PM",
        "image_url": "https://images.unsplash.com/photo-1517694712202-14dd9538aa97?auto=format&fit=crop&w=600&q=80",
        "directions": "Enter CS Building, take elevator to 3rd floor, door 304 opposite server room.",
        "steps": ["Enter CS Department Building.", "Take elevator to 3rd Floor.", "Door 304 is opposite the server room."]
    },
    {
        "id": "loc-3",
        "name": "Central Library & Digital Study Lounge",
        "type": "Library",
        "block": "Central Academic Building, Ground & 1st Floor",
        "hours": "8:00 AM - 10:00 PM",
        "image_url": "https://images.unsplash.com/photo-1521587760476-6c12a4b040da?auto=format&fit=crop&w=600&q=80",
        "directions": "Walk straight from South Gate, enter main glass doors of Central Academic Building.",
        "steps": ["Enter Central Academic Building.", "Show ID at reception desk.", "Proceed to Quiet Study Zone."]
    },
    {
        "id": "loc-4",
        "name": "Main Auditorium A",
        "type": "Auditorium",
        "block": "Student Center Building, Ground Floor",
        "hours": "9:00 AM - 9:00 PM",
        "image_url": "https://images.unsplash.com/photo-1475721027785-f74eccf877e2?auto=format&fit=crop&w=600&q=80",
        "directions": "Located beside the main quadrangle amphitheater.",
        "steps": ["Walk to Central Quadrangle.", "Enter main double doors under the clock tower."]
    },
    {
        "id": "loc-5",
        "name": "College Canteen & Food Court",
        "type": "Dining",
        "block": "Student Activity Complex, Ground Floor",
        "hours": "7:30 AM - 9:00 PM",
        "image_url": "https://images.unsplash.com/photo-1555396273-367ea4eb4db5?auto=format&fit=crop&w=600&q=80",
        "directions": "Next to the Sports Complex and Student Activity Center.",
        "steps": ["Walk towards West Gate.", "Follow signs to Student Activity Complex."]
    },
    {
        "id": "loc-6",
        "name": "Sports Complex & Gymnasium",
        "type": "Sports",
        "block": "West Campus Athletics Ground",
        "hours": "6:00 AM - 9:00 PM",
        "image_url": "https://images.unsplash.com/photo-1534438327276-14e5300c3a48?auto=format&fit=crop&w=600&q=80",
        "directions": "Behind the College Canteen across the football turf.",
        "steps": ["Head West from Main Library.", "Cross the athletic track."]
    },
    {
        "id": "loc-7",
        "name": "Robotics & IoT Research Lab",
        "type": "Laboratory",
        "block": "ECE & CS Joint Wing, 2nd Floor",
        "hours": "9:00 AM - 8:00 PM",
        "image_url": "https://images.unsplash.com/photo-1485827404703-89b55fcc595e?auto=format&fit=crop&w=600&q=80",
        "directions": "Take East staircase in ECE Wing to Room 215.",
        "steps": ["Enter ECE Wing.", "Go up to 2nd Floor.", "Room 215 on right."]
    },
    {
        "id": "loc-8",
        "name": "Faculty Cabin Block C",
        "type": "Faculty Offices",
        "block": "Academic Block C, 2nd Floor",
        "hours": "9:00 AM - 5:00 PM",
        "image_url": "https://images.unsplash.com/photo-1497366216548-37526070297c?auto=format&fit=crop&w=600&q=80",
        "directions": "Elevator B to 2nd floor, turn left past HOD Office.",
        "steps": ["Take Elevator B in Block C.", "Turn left past HOD Office."]
    },
    {
        "id": "loc-9",
        "name": "Placement & Training Cell",
        "type": "Career Services",
        "block": "Administrative Wing, 1st Floor",
        "hours": "9:00 AM - 6:00 PM",
        "image_url": "https://images.unsplash.com/photo-1522071820081-009f0129c71c?auto=format&fit=crop&w=600&q=80",
        "directions": "Above Central Admissions Desk in Admin Wing.",
        "steps": ["Enter Admin Wing.", "Staircase to 1st Floor.", "Room 110."]
    },
    {
        "id": "loc-10",
        "name": "Student Activity Center (SAC)",
        "type": "Clubs",
        "block": "SAC Building, Ground Floor",
        "hours": "8:00 AM - 10:00 PM",
        "image_url": "https://images.unsplash.com/photo-1511632765486-a01980e01a18?auto=format&fit=crop&w=600&q=80",
        "directions": "Adjacent to Gymnasium and Music Club rooms.",
        "steps": ["Walk to SAC Quad.", "Main glass entrance."]
    },
    {
        "id": "loc-11",
        "name": "AI & Data Science Center",
        "type": "Research",
        "block": "Innovation Tower, 4th Floor",
        "hours": "24/7 Access",
        "image_url": "https://images.unsplash.com/photo-1507679799987-c73779587ccf?auto=format&fit=crop&w=600&q=80",
        "directions": "Take Innovation Elevator to 4th Floor.",
        "steps": ["Swipe Student Card at Innovation Tower Lobby.", "Take High-Speed Elevator to 4th Floor."]
    },
    {
        "id": "loc-12",
        "name": "Seminar Hall 2",
        "type": "Seminar",
        "block": "Academic Block A, Ground Floor",
        "hours": "9:00 AM - 6:00 PM",
        "image_url": "https://images.unsplash.com/photo-1505373877841-8d25f7d46678?auto=format&fit=crop&w=600&q=80",
        "directions": "Directly behind Central Fountain.",
        "steps": ["Walk past Central Fountain.", "Door A-05."]
    },
    {
        "id": "loc-13",
        "name": "Health & First Aid Center",
        "type": "Medical",
        "block": "Residential Hostel Zone",
        "hours": "24/7 Service",
        "image_url": "https://images.unsplash.com/photo-1519494026892-80bbd2d6fd0d?auto=format&fit=crop&w=600&q=80",
        "directions": "Near Boys Hostel 1 main entrance.",
        "steps": ["Follow Medical Signs near Hostel Circle."]
    },
    {
        "id": "loc-14",
        "name": "Incubation & Startup Hub",
        "type": "Entrepreneurship",
        "block": "Innovation Tower, 2nd Floor",
        "hours": "8:00 AM - 11:00 PM",
        "image_url": "https://images.unsplash.com/photo-1531403009284-440f080d1e12?auto=format&fit=crop&w=600&q=80",
        "directions": "Innovation Tower, Floor 2.",
        "steps": ["Enter Innovation Tower.", "Stairs to 2nd Floor."]
    },
    {
        "id": "loc-15",
        "name": "Administrative & Dean Offices",
        "type": "Admin",
        "block": "Main Admin Building, 2nd Floor",
        "hours": "9:00 AM - 5:00 PM",
        "image_url": "https://images.unsplash.com/photo-1486406146926-c627a92ad1ab?auto=format&fit=crop&w=600&q=80",
        "directions": "Main entrance building facing North Gate.",
        "steps": ["Enter Main Admin Building.", "Staircase to Dean Office."]
    }
]

# 2. 10 Course Notes
NOTES = [
    {
        "id": "note-1",
        "filename": "CS304_Unit3_ML_Regularization.pdf",
        "title": "CS304 - Machine Learning: L1 & L2 Regularization",
        "course_tag": "CS304",
        "uploaded_at": "2026-09-10",
        "content": "Unit 3: Regularization & Overfitting Prevention\n1. L1 Regularization (Lasso): Penalty = λ ∑ |w_i|\n2. L2 Regularization (Ridge): Penalty = λ ∑ (w_i)^2\n3. Cross-Validation: Tune λ parameter."
    },
    {
        "id": "note-2",
        "filename": "CS302_Unit2_DBMS_Indexing.pdf",
        "title": "CS302 - DBMS: B+ Tree Indexing & ACID Rules",
        "course_tag": "CS302",
        "uploaded_at": "2026-09-09",
        "content": "Unit 2: Indexing & Transactions\n1. B+ Trees maintain sorted data for O(log N) lookup.\n2. ACID Properties: Atomicity, Consistency, Isolation, Durability.\n3. WAL (Write-Ahead Logging)."
    },
    {
        "id": "note-3",
        "filename": "CS301_Unit4_OS_Semaphores.pdf",
        "title": "CS301 - Operating Systems: Semaphores & Deadlocks",
        "course_tag": "CS301",
        "uploaded_at": "2026-09-08",
        "content": "Unit 4: Synchronization\n1. Binary vs Counting Semaphores.\n2. Producer-Consumer Problem & Mutual Exclusion.\n3. Banker's Algorithm for Deadlock Avoidance."
    },
    {
        "id": "note-4",
        "filename": "CS305_Unit1_React_State_Hooks.pdf",
        "title": "CS305 - Web Development: React State & Context",
        "course_tag": "CS305",
        "uploaded_at": "2026-09-07",
        "content": "Unit 1: Modern Frontend Architecture\n1. useState & useEffect Lifecycle.\n2. Context API for global state without prop drilling.\n3. Virtual DOM Reconciliation."
    },
    {
        "id": "note-5",
        "filename": "CS306_Unit3_Networks_TCP_Handshake.pdf",
        "title": "CS306 - Computer Networks: TCP Handshake & IP Subnetting",
        "course_tag": "CS306",
        "uploaded_at": "2026-09-06",
        "content": "Unit 3: Transport Layer Protocols\n1. TCP 3-Way Handshake: SYN -> SYN-ACK -> ACK.\n2. Flow Control & Sliding Window Protocol.\n3. CIDR Subnet Masking."
    },
    {
        "id": "note-6",
        "filename": "CS307_Unit2_Software_Engineering_Agile.pdf",
        "title": "CS307 - Software Engineering: Agile Scrum & Sprint Planning",
        "course_tag": "CS307",
        "uploaded_at": "2026-09-05",
        "content": "Unit 2: Agile Methodologies\n1. Scrum Roles: Product Owner, Scrum Master, Dev Team.\n2. Sprint Burndown Charts & Daily Standups.\n3. CI/CD Automated Testing."
    },
    {
        "id": "note-7",
        "filename": "CS308_Unit5_DeepLearning_Transformers.pdf",
        "title": "CS308 - Deep Learning: Attention Mechanisms & Transformers",
        "course_tag": "CS308",
        "uploaded_at": "2026-09-04",
        "content": "Unit 5: Generative Models & Attention\n1. Self-Attention Formula: Attention(Q,K,V) = softmax(QK^T / sqrt(d_k))V.\n2. Multi-Head Attention.\n3. Positional Encoding."
    },
    {
        "id": "note-8",
        "filename": "CS309_Unit3_Cybersecurity_RSA_PKI.pdf",
        "title": "CS309 - Cybersecurity: RSA Asymmetric Cryptography & SSL",
        "course_tag": "CS309",
        "uploaded_at": "2026-09-03",
        "content": "Unit 3: Cryptographic Protocols\n1. RSA Algorithm: Modulo math with prime factors p and q.\n2. Public Key Infrastructure (PKI) & TLS 1.3 Handshake.\n3. SHA-256 Hashing."
    },
    {
        "id": "note-9",
        "filename": "CS310_Unit2_Cloud_Docker_Kubernetes.pdf",
        "title": "CS310 - Cloud Computing: Docker Containers & Kubernetes",
        "course_tag": "CS310",
        "uploaded_at": "2026-09-02",
        "content": "Unit 2: Containerization & Orchestration\n1. Dockerfile Layering & Image Caching.\n2. Kubernetes Pods, Deployments & Services.\n3. Auto-scaling Policies."
    },
    {
        "id": "note-10",
        "filename": "CS311_Unit1_Flutter_State_Management.pdf",
        "title": "CS311 - Mobile Development: Flutter Declarative Layouts",
        "course_tag": "CS311",
        "uploaded_at": "2026-09-01",
        "content": "Unit 1: Cross-Platform Mobile Apps\n1. Stateless vs Stateful Widgets.\n2. Riverpod & Provider State Management.\n3. Async Data Fetching with FutureBuilder."
    }
]

# 3. 10 Integrations with Official High-Res Brand Logos
INTEGRATIONS = [
    {
        "id": "gcal",
        "name": "Google Calendar",
        "category": "Productivity",
        "status": "Connected",
        "logo_url": "https://upload.wikimedia.org/wikipedia/commons/a/a5/Google_Calendar_icon_%282020%29.svg",
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
        "logo_url": "https://upload.wikimedia.org/wikipedia/commons/c/c9/Microsoft_Office_Teams_%282018%E2%80%93present%29.svg",
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
        "logo_url": "https://upload.wikimedia.org/wikipedia/commons/d/d5/Slack_icon_2019.svg",
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
        "logo_url": "https://img.icons8.com/color/96/university.png",
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
        "logo_url": "https://upload.wikimedia.org/wikipedia/commons/e/e9/Notion-logo.svg",
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
        "logo_url": "https://upload.wikimedia.org/wikipedia/commons/7/7e/Gmail_icon_%282020%29.svg",
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
        "logo_url": "https://upload.wikimedia.org/wikipedia/commons/1/12/Google_Drive_icon_%282020%29.svg",
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
        "logo_url": "https://upload.wikimedia.org/wikipedia/commons/9/91/Octicons-mark-github.svg",
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
        "logo_url": "https://upload.wikimedia.org/wikipedia/commons/0/09/YouTube_full-color_icon_%282017%29.svg",
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
        "logo_url": "https://upload.wikimedia.org/wikipedia/commons/ca/ca/LinkedIn_logo_initials.png",
        "color": "text-blue-500 border-blue-500/40 bg-blue-950/40",
        "last_sync": "Yesterday",
        "synced_count": "Profile Skills & Job Alerts",
        "action": "Open LinkedIn",
        "url": "https://www.linkedin.com"
    }
]

# 4. 10 Opportunities (Scholarships, Hackathons, Internships) with Brand Logos
OPPORTUNITIES = [
    {
        "id": "opp-1",
        "title": "Central Sector Scholarship for College Students",
        "category": "Scholarships",
        "type": "Scholarships",
        "organization": "National Scholarship Portal",
        "logo_url": "https://img.icons8.com/color/96/guarantee.png",
        "description": "Financial aid grant for top performing undergraduate students in engineering.",
        "required_skills": ["Computer Science", "Academic Merit"],
        "deadline": "20 Oct 2026",
        "stipend_or_prize": "₹20,000 / Year Grant",
        "url": "https://scholarships.gov.in"
    },
    {
        "id": "opp-2",
        "title": "Google Women Techmakers Scholars Program",
        "category": "Scholarships",
        "type": "Scholarships",
        "organization": "Google India",
        "logo_url": "https://upload.wikimedia.org/wikipedia/commons/2/2f/Google_2015_logo.svg",
        "description": "Scholarship and mentorship retreat for female computer science students.",
        "required_skills": ["Python", "Leadership", "Data Structures"],
        "deadline": "30 Oct 2026",
        "stipend_or_prize": "$1,000 USD Grant",
        "url": "https://buildyourfuture.withgoogle.com/scholarships"
    },
    {
        "id": "opp-3",
        "title": "AI Thinkers Global Hackathon 2026",
        "category": "Hackathons",
        "type": "Hackathons",
        "organization": "Devpost & Unstop",
        "logo_url": "https://img.icons8.com/color/96/artificial-intelligence.png",
        "description": "36-hour hackathon to build generative AI solutions for campus productivity.",
        "required_skills": ["Python", "Machine Learning", "API Integration"],
        "deadline": "12 Sep 2026",
        "stipend_or_prize": "₹2,50,000 Prize Pool",
        "url": "https://unstop.com/hackathons"
    },
    {
        "id": "opp-4",
        "title": "Microsoft Imagine Cup World Championship",
        "category": "Hackathons",
        "type": "Hackathons",
        "organization": "Microsoft",
        "logo_url": "https://upload.wikimedia.org/wikipedia/commons/4/44/Microsoft_logo.svg",
        "description": "Global student developer competition leveraging Azure and OpenAI technologies.",
        "required_skills": ["Azure", "C#", "React", "AI"],
        "deadline": "15 Nov 2026",
        "stipend_or_prize": "$100,000 USD Grand Prize",
        "url": "https://imaginecup.microsoft.com"
    },
    {
        "id": "opp-5",
        "title": "Amazon ML Summer School Internship 2026",
        "category": "Internships",
        "type": "Internships",
        "organization": "Amazon Science",
        "logo_url": "https://upload.wikimedia.org/wikipedia/commons/a/a9/Amazon_logo.svg",
        "description": "Exclusive training and internship offer for undergraduate CS students in ML.",
        "required_skills": ["Python", "Machine Learning", "Linear Algebra"],
        "deadline": "05 Oct 2026",
        "stipend_or_prize": "₹80,000 / Month Stipend",
        "url": "https://amazon.jobs"
    },
    {
        "id": "opp-6",
        "title": "Smart India Hackathon (SIH) National Final",
        "category": "Hackathons",
        "type": "Hackathons",
        "organization": "Ministry of Education India",
        "logo_url": "https://img.icons8.com/color/96/india.png",
        "description": "Nationwide competition solving real-world government department challenges.",
        "required_skills": ["Full Stack", "IoT", "Problem Solving"],
        "deadline": "10 Oct 2026",
        "stipend_or_prize": "₹1,00,000 Per Problem Statement",
        "url": "https://sih.gov.in"
    },
    {
        "id": "opp-7",
        "title": "Meta Open Source Fellowship 2026",
        "category": "Fellowships",
        "type": "Fellowships",
        "organization": "Meta Engineering",
        "logo_url": "https://upload.wikimedia.org/wikipedia/commons/7/7b/Meta_Platforms_Inc._logo.svg",
        "description": "3-month paid open-source internship working on React, PyTorch, and Llama models.",
        "required_skills": ["React", "PyTorch", "C++"],
        "deadline": "01 Nov 2026",
        "stipend_or_prize": "$3,000 USD / Month",
        "url": "https://metacareers.com"
    },
    {
        "id": "opp-8",
        "title": "GitHub Octernships Global Program",
        "category": "Internships",
        "type": "Internships",
        "organization": "GitHub Campus",
        "logo_url": "https://upload.wikimedia.org/wikipedia/commons/9/91/Octicons-mark-github.svg",
        "description": "Remote paid internships for student open-source contributors.",
        "required_skills": ["Git", "JavaScript", "Python"],
        "deadline": "25 Sep 2026",
        "stipend_or_prize": "$1,500 USD / Month",
        "url": "https://github.com/education"
    },
    {
        "id": "opp-9",
        "title": "Intel AI Innovation Research Grant",
        "category": "Scholarships",
        "type": "Scholarships",
        "organization": "Intel Labs",
        "logo_url": "https://upload.wikimedia.org/wikipedia/commons/7/7d/Intel_logo_%282020%29.svg",
        "description": "Grant for student projects focusing on edge AI acceleration and OpenVINO.",
        "required_skills": ["Computer Vision", "C++", "OpenVINO"],
        "deadline": "18 Oct 2026",
        "stipend_or_prize": "₹1,50,000 Project Grant",
        "url": "https://intel.com/research"
    },
    {
        "id": "opp-10",
        "title": "Pragati Scholarship for Female Engineers",
        "category": "Scholarships",
        "type": "Scholarships",
        "organization": "AICTE India",
        "logo_url": "https://img.icons8.com/color/96/graduation-cap.png",
        "description": "Government scholarship promoting women in technical higher education.",
        "required_skills": ["Engineering", "Academic Excellence"],
        "deadline": "31 Oct 2026",
        "stipend_or_prize": "₹50,000 / Year",
        "url": "https://aicte-india.org"
    }
]

# 5. 10 Curated YouTube Tutorials
YOUTUBE_TUTORIALS = [
    {"id": "yt-1", "course": "CS304 - Machine Learning", "topic": "L1 (Lasso) vs L2 (Ridge) Regularization", "channel": "StatQuest", "duration": "14:20", "views": "1.2M views", "url": "https://www.youtube.com/watch?v=Q81RR3yKnbc"},
    {"id": "yt-2", "course": "CS302 - Database Systems", "topic": "B+ Trees & Database Indexing Explained", "channel": "Gate Smashers", "duration": "18:45", "views": "850K views", "url": "https://www.youtube.com/watch?v=aZjYr87r1b8"},
    {"id": "yt-3", "course": "CS301 - Operating Systems", "topic": "Process Synchronization & Semaphores", "channel": "Neso Academy", "duration": "22:10", "views": "1.5M views", "url": "https://www.youtube.com/watch?v=ukM_qw4dGE0"},
    {"id": "yt-4", "course": "CS305 - Web Technologies", "topic": "React 18 Hooks & Context API Crash Course", "channel": "Traversy Media", "duration": "45:00", "views": "2.1M views", "url": "https://www.youtube.com/watch?v=w7ejDZ8SWv8"},
    {"id": "yt-5", "course": "CS306 - Computer Networks", "topic": "TCP 3-Way Handshake & Packet Capture", "channel": "NetworkChuck", "duration": "16:30", "views": "980K views", "url": "https://www.youtube.com/watch?v=rYodcvhh7b8"},
    {"id": "yt-6", "course": "CS307 - Software Engineering", "topic": "Agile Scrum & Sprint Planning in 10 Minutes", "channel": "Fireship", "duration": "10:15", "views": "1.1M views", "url": "https://www.youtube.com/watch?v=2Vt7Ik8Ublw"},
    {"id": "yt-7", "course": "CS308 - Deep Learning", "topic": "PyTorch Neural Network Step-by-Step", "channel": "freeCodeCamp", "duration": "2:30:00", "views": "3.4M views", "url": "https://www.youtube.com/watch?v=V_xro1bcAuA"},
    {"id": "yt-8", "course": "CS309 - Cybersecurity", "topic": "RSA Encryption & Public Key Cryptography", "channel": "Computerphile", "duration": "12:50", "views": "1.8M views", "url": "https://www.youtube.com/watch?v=GSIDSfKVGDY"},
    {"id": "yt-9", "course": "CS310 - Cloud Computing", "topic": "Docker Containers & Kubernetes Crash Course", "channel": "TechWorld with Nana", "duration": "1:15:00", "views": "4.2M views", "url": "https://www.youtube.com/watch?v=3c-iBn73dDE"},
    {"id": "yt-10", "course": "CS311 - Mobile Development", "topic": "Flutter State Management with Riverpod", "channel": "Reso Coder", "duration": "28:40", "views": "450K views", "url": "https://www.youtube.com/watch?v=Zp75gUdLyR0"}
]

# 6. Weekly Class Timetable
TIMETABLE = [
    {
        "day": "Monday",
        "classes": [
            {"time": "09:00 AM", "course": "CS301 - Operating Systems", "room": "A-201", "instructor": "Dr. Sarah Jenkins", "code": "CS301"},
            {"time": "10:30 AM", "course": "CS302 - DBMS Class", "room": "B-102", "instructor": "Prof. Ramesh Gupta", "code": "CS302"},
            {"time": "01:30 PM", "course": "CS304 - Machine Learning", "room": "C-305", "instructor": "Dr. Alan Turing", "code": "CS304"},
            {"time": "03:30 PM", "course": "CS305 - Web Technologies Lab", "room": "Lab-3", "instructor": "Prof. Grace Hopper", "code": "CS305"}
        ]
    },
    {
        "day": "Tuesday",
        "classes": [
            {"time": "09:30 AM", "course": "CS306 - Computer Networks", "room": "B-104", "instructor": "Dr. Anita Borg", "code": "CS306"},
            {"time": "11:30 AM", "course": "CS307 - Software Engineering", "room": "A-108", "instructor": "Prof. Ken Thompson", "code": "CS307"},
            {"time": "02:00 PM", "course": "CS308 - Deep Learning Lab", "room": "Lab-4", "instructor": "Dr. Alan Turing", "code": "CS308"}
        ]
    }
]

# 7. 10 Assignments & Tasks
now = datetime.now()
ASSIGNMENTS = [
    {
        "id": "asgn-1",
        "title": "DBMS Relational Schema & ER Diagram Assignment",
        "course": "CS302",
        "course_name": "Database Management Systems",
        "due_date": (now + timedelta(days=2)).strftime("%d %b %Y"),
        "days_left": 2,
        "priority": "High",
        "status": "In Progress",
        "remaining_hours": 4,
        "description": "Design ER Diagram and normalization for College Portal.",
        "subtasks": [
            {"id": "task-101", "title": "Identify Entities & Relationships", "status": "Completed", "estimated_hours": 1.0},
            {"id": "task-102", "title": "Draw ER Diagram in StarUML/Figma", "status": "Completed", "estimated_hours": 1.5},
            {"id": "task-103", "title": "Convert ER diagram to Relational Schema", "status": "Pending", "estimated_hours": 1.5}
        ]
    },
    {
        "id": "asgn-2",
        "title": "Operating Systems Producer-Consumer Semaphore Lab",
        "course": "CS301",
        "course_name": "Operating Systems",
        "due_date": (now + timedelta(days=3)).strftime("%d %b %Y"),
        "days_left": 3,
        "priority": "High",
        "status": "In Progress",
        "remaining_hours": 3,
        "description": "Implement POSIX mutexes and semaphores in C.",
        "subtasks": [
            {"id": "task-201", "title": "Write C code for Pthreads Synchronization", "status": "Completed", "estimated_hours": 1.5},
            {"id": "task-202", "title": "Test Deadlock Conditions", "status": "Pending", "estimated_hours": 1.5}
        ]
    },
    {
        "id": "asgn-3",
        "title": "Machine Learning Regularization & Model Tuning",
        "course": "CS304",
        "course_name": "Machine Learning",
        "due_date": (now + timedelta(days=5)).strftime("%d %b %Y"),
        "days_left": 5,
        "priority": "Medium",
        "status": "Pending",
        "remaining_hours": 6,
        "description": "Build Scikit-Learn pipeline comparing Ridge vs Lasso regression.",
        "subtasks": [
            {"id": "task-301", "title": "Preprocess dataset with StandardScaler", "status": "Pending", "estimated_hours": 2.0},
            {"id": "task-302", "title": "Plot Cross-Validation Error Curve", "status": "Pending", "estimated_hours": 4.0}
        ]
    },
    {
        "id": "asgn-4",
        "title": "Full-Stack Web App Frontend & API Integration",
        "course": "CS305",
        "course_name": "Web Technologies",
        "due_date": (now + timedelta(days=6)).strftime("%d %b %Y"),
        "days_left": 6,
        "priority": "Medium",
        "status": "Pending",
        "remaining_hours": 5,
        "description": "Build responsive React dashboard consuming REST API.",
        "subtasks": [
            {"id": "task-401", "title": "Design Tailwind CSS Components", "status": "Pending", "estimated_hours": 2.5},
            {"id": "task-402", "title": "Connect Fetch API Endpoints", "status": "Pending", "estimated_hours": 2.5}
        ]
    },
    {
        "id": "asgn-5",
        "title": "Computer Networks Socket Programming Project",
        "course": "CS306",
        "course_name": "Computer Networks",
        "due_date": (now + timedelta(days=8)).strftime("%d %b %Y"),
        "days_left": 8,
        "priority": "Medium",
        "status": "Pending",
        "remaining_hours": 5,
        "description": "Create TCP Multi-client Chat Server in Python.",
        "subtasks": [{"id": "task-501", "title": "Implement Socket Bind & Listen", "status": "Pending", "estimated_hours": 5.0}]
    },
    {
        "id": "asgn-6",
        "title": "Software Architecture SRS Document & UML Diagrams",
        "course": "CS307",
        "course_name": "Software Engineering",
        "due_date": (now + timedelta(days=9)).strftime("%d %b %Y"),
        "days_left": 9,
        "priority": "Low",
        "status": "Pending",
        "remaining_hours": 4,
        "description": "Write IEEE 830 SRS Specification document.",
        "subtasks": [{"id": "task-601", "title": "Draft Use Case Specifications", "status": "Pending", "estimated_hours": 4.0}]
    },
    {
        "id": "asgn-7",
        "title": "Deep Learning Image Classification PyTorch Model",
        "course": "CS308",
        "course_name": "Deep Learning",
        "due_date": (now + timedelta(days=11)).strftime("%d %b %Y"),
        "days_left": 11,
        "priority": "High",
        "status": "Pending",
        "remaining_hours": 8,
        "description": "Train ResNet CNN model on CIFAR-10 dataset.",
        "subtasks": [{"id": "task-701", "title": "Setup PyTorch DataLoader & Augmentation", "status": "Pending", "estimated_hours": 8.0}]
    },
    {
        "id": "asgn-8",
        "title": "Cybersecurity RSA Encryption & Key Exchange Audit",
        "course": "CS309",
        "course_name": "Cybersecurity",
        "due_date": (now + timedelta(days=12)).strftime("%d %b %Y"),
        "days_left": 12,
        "priority": "Medium",
        "status": "Pending",
        "remaining_hours": 5,
        "description": "Implement RSA key generation and digital signature verification.",
        "subtasks": [{"id": "task-801", "title": "Verify Hash Signature Integrity", "status": "Pending", "estimated_hours": 5.0}]
    },
    {
        "id": "asgn-9",
        "title": "Cloud Computing Microservices Docker Deployment",
        "course": "CS310",
        "course_name": "Cloud Computing",
        "due_date": (now + timedelta(days=14)).strftime("%d %b %Y"),
        "days_left": 14,
        "priority": "Medium",
        "status": "Pending",
        "remaining_hours": 6,
        "description": "Write docker-compose file for Flask & Postgres.",
        "subtasks": [{"id": "task-901", "title": "Configure Nginx Reverse Proxy Container", "status": "Pending", "estimated_hours": 6.0}]
    },
    {
        "id": "asgn-10",
        "title": "Flutter Mobile App UI Prototype & Navigation",
        "course": "CS311",
        "course_name": "Mobile App Development",
        "due_date": (now + timedelta(days=15)).strftime("%d %b %Y"),
        "days_left": 15,
        "priority": "Low",
        "status": "Pending",
        "remaining_hours": 4,
        "description": "Build multi-screen Flutter mobile user interface.",
        "subtasks": [{"id": "task-1001", "title": "Setup GoRouter Navigation Stack", "status": "Pending", "estimated_hours": 4.0}]
    }
]

# 8. 10 Campus Events & Club Meetups with Visual Banner Images
CAMPUS_EVENTS = [
    {"id": "evt-1", "title": "AI Thinkers Global Hackathon 2026", "location": "Main Auditorium A", "category": "Hackathons", "date": "12 Sep 2026", "time": "09:00 AM", "banner_url": "https://images.unsplash.com/photo-1504384308090-c894fdcc538d?auto=format&fit=crop&w=600&q=80"},
    {"id": "evt-2", "title": "Annual Tech Symposium (TechFest 2026)", "location": "Central Quadrangle", "category": "Symposium", "date": "18 Sep 2026", "time": "10:00 AM", "banner_url": "https://images.unsplash.com/photo-1540575467063-178a50c2df87?auto=format&fit=crop&w=600&q=80"},
    {"id": "evt-3", "title": "Google Developer Student Club Orientation", "location": "Seminar Hall 2", "category": "Club Orientation", "date": "20 Sep 2026", "time": "02:00 PM", "banner_url": "https://images.unsplash.com/photo-1531482615713-2afd69097998?auto=format&fit=crop&w=600&q=80"},
    {"id": "evt-4", "title": "Competitive Programming Code-a-Thon", "location": "Lab-3 Web Lab", "category": "Coding", "date": "22 Sep 2026", "time": "04:00 PM", "banner_url": "https://images.unsplash.com/photo-1517694712202-14dd9538aa97?auto=format&fit=crop&w=600&q=80"},
    {"id": "evt-5", "title": "Cybersecurity CTF Flag Hunt Competition", "location": "Lab-4 Network Lab", "category": "Security", "date": "25 Sep 2026", "time": "11:00 AM", "banner_url": "https://images.unsplash.com/photo-1526374965328-7f61d4dc18c5?auto=format&fit=crop&w=600&q=80"},
    {"id": "evt-6", "title": "Open Source Software & Git Workshop", "location": "B-102 Lecture Hall", "category": "Workshop", "date": "28 Sep 2026", "time": "03:00 PM", "banner_url": "https://images.unsplash.com/photo-1522071820081-009f0129c71c?auto=format&fit=crop&w=600&q=80"},
    {"id": "evt-7", "title": "Robotics Club Live Autonomous Drone Exhibition", "location": "Sports Ground", "category": "Robotics", "date": "02 Oct 2026", "time": "04:30 PM", "banner_url": "https://images.unsplash.com/photo-1485827404703-89b55fcc595e?auto=format&fit=crop&w=600&q=80"},
    {"id": "evt-8", "title": "Entrepreneurship & Startup Pitch Day", "location": "Incubation Hub", "category": "Startups", "date": "05 Oct 2026", "time": "10:30 AM", "banner_url": "https://images.unsplash.com/photo-1556761175-5973dc0f32e7?auto=format&fit=crop&w=600&q=80"},
    {"id": "evt-9", "title": "Data Science & GenAI Industry Seminar", "location": "Main Auditorium A", "category": "Seminar", "date": "08 Oct 2026", "time": "02:00 PM", "banner_url": "https://images.unsplash.com/photo-1451187580459-43490279c0fa?auto=format&fit=crop&w=600&q=80"},
    {"id": "evt-10", "title": "Alumni Placement & Career Networking Night", "location": "Student Activity Center", "category": "Networking", "date": "12 Oct 2026", "time": "06:00 PM", "banner_url": "https://images.unsplash.com/photo-1511578314322-379afb476865?auto=format&fit=crop&w=600&q=80"}
]

# 9. 10 Lab Exams Viva Solvers
LAB_EXAMS = [
    {"id": "lab-1", "course": "CS301 - Operating Systems Lab", "viva_questions": ["What is binary semaphore vs counting semaphore?", "Explain Banker's algorithm for deadlock avoidance.", "What is paging vs segmentation?"]},
    {"id": "lab-2", "course": "CS302 - Database Systems Lab", "viva_questions": ["Define 3rd Normal Form (3NF) and BCNF.", "What is the difference between Clustered and Non-Clustered index?", "Explain ACID properties in SQL transactions."]},
    {"id": "lab-3", "course": "CS304 - Machine Learning Lab", "viva_questions": ["What is precision, recall, and F1-Score?", "Explain how Random Forest handles overfitting.", "What is gradient descent and learning rate decay?"]},
    {"id": "lab-4", "course": "CS305 - Web Technologies Lab", "viva_questions": ["What is Virtual DOM in React?", "Difference between LocalStorage and SessionStorage.", "Explain CORS and pre-flight HTTP requests."]},
    {"id": "lab-5", "course": "CS306 - Computer Networks Lab", "viva_questions": ["Explain TCP 3-Way Handshake step-by-step.", "Difference between IPv4 and IPv6 headers.", "What is ARP and DNS lookup flow?"]},
    {"id": "lab-6", "course": "CS307 - Software Engineering Lab", "viva_questions": ["Explain Agile Scrum ceremonies.", "What is Unit Testing vs Integration Testing?", "Define SOLID principles in object-oriented design."]},
    {"id": "lab-7", "course": "CS308 - Deep Learning Lab", "viva_questions": ["What is vanishing gradient in RNNs?", "Explain Self-Attention in Transformer models.", "What is Softmax activation function?"]},
    {"id": "lab-8", "course": "CS309 - Cybersecurity Lab", "viva_questions": ["How does RSA asymmetric encryption work?", "Difference between Symmetric and Asymmetric ciphers.", "What is SQL Injection and how to prevent it?"]},
    {"id": "lab-9", "course": "CS310 - Cloud Computing Lab", "viva_questions": ["Difference between Docker Image and Container.", "Explain Kubernetes Pod architecture.", "What is Serverless computing (AWS Lambda)?"]},
    {"id": "lab-10", "course": "CS311 - Mobile Development Lab", "viva_questions": ["Difference between Stateful and Stateless Widget in Flutter.", "Explain Riverpod state provider lifecycle.", "How to optimize ListView rendering performance?"]}
]

# 10. 10 AI Career Roadmaps
CAREER_ROADMAPS = [
    {"id": "road-1", "role": "AI / Machine Learning Engineer", "description": "Master Python, Scikit-Learn, PyTorch, Transformers, and MLOps deployment.", "milestones": ["1. Python & Linear Algebra", "2. ML Algorithms & Scikit-Learn", "3. Deep Learning & PyTorch", "4. Model Deployment & FastAPI"]},
    {"id": "road-2", "role": "Full-Stack Web Developer", "description": "Master React, Node.js, Express, Tailwind CSS, PostgreSQL, and AWS.", "milestones": ["1. HTML, CSS & JavaScript ES6+", "2. React & State Management", "3. Node.js REST APIs", "4. Database Normalization & Deployment"]},
    {"id": "road-3", "role": "Data Scientist & Analytics Engineer", "description": "Master SQL, Pandas, Feature Engineering, Tableau, and Predictive Modeling.", "milestones": ["1. Advanced SQL & Data Cleaning", "2. Statistical Analysis with Python", "3. Machine Learning Modeling", "4. BI Dashboards & Storytelling"]},
    {"id": "road-4", "role": "Cloud & DevOps Solutions Architect", "description": "Master Linux, Docker, Kubernetes, Terraform, CI/CD, and AWS/GCP Cloud.", "milestones": ["1. Linux Administration & Shell Scripting", "2. Docker Containerization", "3. Kubernetes Orchestration", "4. Infrastructure as Code (Terraform)"]},
    {"id": "road-5", "role": "Cybersecurity & Ethical Hacking Specialist", "description": "Master Cryptography, Wireshark Packet Analysis, Pen Testing, and Network Security.", "milestones": ["1. Network Protocols & Linux Security", "2. Web Vulnerability Auditing (OWASP)", "3. Penetration Testing (Metasploit)", "4. Incident Response & SIEM"]},
    {"id": "road-6", "role": "Mobile App Developer (Flutter / iOS / Android)", "description": "Master Dart/Flutter, Swift, Kotlin, Firebase, and App Store Publishing.", "milestones": ["1. Dart Fundamentals & Flutter UI", "2. REST API & Firebase Integration", "3. State Management (Riverpod)", "4. Play Store / App Store Release"]},
    {"id": "road-7", "role": "Backend Systems & Database Engineer", "description": "Master Java/Go, Microservices, Redis Caching, Kafka, and PostgreSQL.", "milestones": ["1. High-Performance Java / Go", "2. Microservice Architecture", "3. Distributed Caching with Redis", "4. Message Queues with Kafka"]},
    {"id": "road-8", "role": "Autonomous Robotics & Embedded Engineer", "description": "Master C++, ROS2, Computer Vision, Sensor Fusion, and Microcontrollers.", "milestones": ["1. Modern C++17/20", "2. ROS2 Robot Operating System", "3. OpenCV Computer Vision", "4. Sensor Fusion & SLAM"]},
    {"id": "road-9", "role": "Blockchain & Smart Contract Developer", "description": "Master Solidity, Ethereum EVM, Web3.js, Rust, and Decentralized Finance.", "milestones": ["1. Solidity Smart Contracts", "2. Web3.js / Ethers.js Frontend Integration", "3. Smart Contract Auditing", "4. Layer-2 Scaling Solutions"]},
    {"id": "road-10", "role": "UI/UX & Product Experience Designer", "description": "Master Figma Design Systems, User Research, Wireframing, and Prototyping.", "milestones": ["1. User Research & Personas", "2. Wireframing & Information Architecture", "3. Interactive Figma Components", "4. Usability Testing & Hand-off"]}
]

# 11. 10 Student Projects with Banner Images
PROJECTS = [
    {"id": "proj-1", "title": "CampusMind AI Student Co-Pilot", "category": "AI / Web", "tech": "Flask, React, Firebase, Exa AI", "banner_url": "https://images.unsplash.com/photo-1526374965328-7f61d4dc18c5?auto=format&fit=crop&w=600&q=80", "description": "All-in-one AI assistant for student schedules, notes, and scholarships.", "needed_roles": ["Frontend Dev", "Backend Dev"]},
    {"id": "proj-2", "title": "Smart Indoor Campus Navigation App", "category": "Mobile / AR", "tech": "Flutter, ARCore, Bluetooth Beacons", "banner_url": "https://images.unsplash.com/photo-1562774053-701939374585?auto=format&fit=crop&w=600&q=80", "description": "AR indoor navigation app guiding students to classrooms and labs.", "needed_roles": ["Flutter Dev", "AR Designer"]},
    {"id": "proj-3", "title": "Automated Exam Question Generator", "category": "GenAI", "tech": "Python, Gemini API, PyPDF2", "banner_url": "https://images.unsplash.com/photo-1516321318423-f06f85e504b3?auto=format&fit=crop&w=600&q=80", "description": "Generates viva quizzes and practice exams from uploaded lecture notes.", "needed_roles": ["ML Engineer", "UI Designer"]},
    {"id": "proj-4", "title": "Peer-to-Peer Notes & Book Exchange", "category": "Web App", "tech": "Node.js, MongoDB, React", "banner_url": "https://images.unsplash.com/photo-1524995997946-a1c2e315a42f?auto=format&fit=crop&w=600&q=80", "description": "Student marketplace for sharing class notes, textbooks, and lab gear.", "needed_roles": ["Full Stack Dev"]},
    {"id": "proj-5", "title": "AI Resume Matcher & Mock Interviewer", "category": "Career AI", "tech": "Python, OpenAI/Gemini, WebRTC", "banner_url": "https://images.unsplash.com/photo-1573496359142-b8d87734a5a2?auto=format&fit=crop&w=600&q=80", "description": "Conducts AI voice mock interviews and scores resume skill gaps.", "needed_roles": ["AI/ML Specialist", "WebRTC Engineer"]},
    {"id": "proj-6", "title": "IoT Smart Library Seat & Attendance System", "category": "IoT / Cloud", "tech": "ESP32, MQTT, Firebase, React", "banner_url": "https://images.unsplash.com/photo-1521587760476-6c12a4b040da?auto=format&fit=crop&w=600&q=80", "description": "Real-time occupancy tracking for quiet study zones and library seats.", "needed_roles": ["Hardware Engineer", "Cloud Dev"]},
    {"id": "proj-7", "title": "College Canteen Pre-Ordering & Queue App", "category": "Mobile", "tech": "React Native, Node.js, Stripe", "banner_url": "https://images.unsplash.com/photo-1555396273-367ea4eb4db5?auto=format&fit=crop&w=600&q=80", "description": "Pre-order meals to skip lunchtime canteen queues on campus.", "needed_roles": ["Mobile Dev", "Backend Dev"]},
    {"id": "proj-8", "title": "Blockchain Degree Verification Portal", "category": "Web3", "tech": "Solidity, Ethereum, IPFS, React", "banner_url": "https://images.unsplash.com/photo-1639762681485-074b7f938ba0?auto=format&fit=crop&w=600&q=80", "description": "Tamper-proof academic transcript and degree certificate verification.", "needed_roles": ["Smart Contract Dev"]},
    {"id": "proj-9", "title": "Code Error Diagnostic VSCode Extension", "category": "Developer Tools", "tech": "TypeScript, VSCode API, LLM API", "banner_url": "https://images.unsplash.com/photo-1555066931-4365d14bab8c?auto=format&fit=crop&w=600&q=80", "description": "Real-time AI syntax error fixer inside VSCode editor.", "needed_roles": ["TypeScript Dev"]},
    {"id": "proj-10", "title": "Virtual Campus 3D Metaverse Tour", "category": "3D / Gaming", "tech": "Three.js, WebGL, React", "banner_url": "https://images.unsplash.com/photo-1618005182384-a83a8bd57fbe?auto=format&fit=crop&w=600&q=80", "description": "Interactive 3D virtual tour of the college campus for prospective students.", "needed_roles": ["3D Artist", "Three.js Developer"]}
]

# 12. 10 Faculty & Alumni Mentors with Professional Avatars
MENTORS = [
    {"id": "men-1", "name": "Dr. Sarah Jenkins", "role": "Associate Professor (Operating Systems)", "avatar_url": "https://images.unsplash.com/photo-1573496359142-b8d87734a5a2?auto=format&fit=crop&w=300&q=80", "expertise": "OS Kernels, C/C++, Synchronization", "availability": "Mon & Wed 2:00 PM"},
    {"id": "men-2", "name": "Prof. Ramesh Gupta", "role": "Head of Department (DBMS)", "avatar_url": "https://images.unsplash.com/photo-1560250097-0b93528c311a?auto=format&fit=crop&w=300&q=80", "expertise": "SQL Tuning, B+ Trees, Database Architecture", "availability": "Tue & Thu 10:00 AM"},
    {"id": "men-3", "name": "Dr. Alan Turing", "role": "AI Research Chair", "avatar_url": "https://images.unsplash.com/photo-1534528741775-53994a69daeb?auto=format&fit=crop&w=300&q=80", "expertise": "Machine Learning, PyTorch, Neural Networks", "availability": "Friday 3:00 PM"},
    {"id": "men-4", "name": "Prof. Grace Hopper", "role": "Professor (Software Engineering)", "avatar_url": "https://images.unsplash.com/photo-1580489944761-15a19d654956?auto=format&fit=crop&w=300&q=80", "expertise": "Agile Scrum, System Design, CI/CD", "availability": "Wednesday 11:00 AM"},
    {"id": "men-5", "name": "Dr. Linus Torvalds", "role": "Distinguished Visiting Faculty", "avatar_url": "https://images.unsplash.com/photo-1507003211169-0a1dd7228f2d?auto=format&fit=crop&w=300&q=80", "expertise": "Linux Architecture, Git, Open Source", "availability": "Monday 4:00 PM"},
    {"id": "men-6", "name": "Mentor Priya Sharma", "role": "Senior SDE @ Google (Alumni 2022)", "avatar_url": "https://images.unsplash.com/photo-1573497019940-1c28c88b4f3e?auto=format&fit=crop&w=300&q=80", "expertise": "DSA, Tech Interviews, Cloud Infrastructure", "availability": "Saturday 11:00 AM"},
    {"id": "men-7", "name": "Mentor Rahul Verma", "role": "Staff Software Engineer @ Microsoft", "avatar_url": "https://images.unsplash.com/photo-1500648767791-00dcc994a43e?auto=format&fit=crop&w=300&q=80", "expertise": "Full Stack React/Node, System Architecture", "availability": "Sunday 2:00 PM"},
    {"id": "men-8", "name": "Dr. Anita Borg", "role": "Professor (Networks & Security)", "avatar_url": "https://images.unsplash.com/photo-1573496799652-408c2ac9fe98?auto=format&fit=crop&w=300&q=80", "expertise": "Cryptography, Penetration Testing, SSL", "availability": "Thursday 1:00 PM"},
    {"id": "men-9", "name": "Mentor David Patel", "role": "AI Researcher @ OpenAI Alumni", "avatar_url": "https://images.unsplash.com/photo-1472099645785-5658abf4ff4e?auto=format&fit=crop&w=300&q=80", "expertise": "Large Language Models, GenAI, MLOps", "availability": "Saturday 4:00 PM"},
    {"id": "men-10", "name": "Prof. Ken Thompson", "role": "Professor (Algorithms)", "avatar_url": "https://images.unsplash.com/photo-1519085360753-af0119f7cbe7?auto=format&fit=crop&w=300&q=80", "expertise": "Data Structures, Go Language, Unix", "availability": "Tuesday 3:00 PM"}
]

# Data Access Helper Functions
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
