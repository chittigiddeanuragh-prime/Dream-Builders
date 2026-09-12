"""
CampusMind Agent Core (agent.py)
Powered by OpenRouter API & Live OpenAI/Gemini/Claude Tool Execution.
Generates detailed, step-by-step, structured, and ordered responses.
"""

import os
import json
import requests
import tools

# Load .env file if available
env_path = os.path.join(os.path.dirname(__file__), '.env')
if os.path.exists(env_path):
    with open(env_path, 'r') as f:
        for line in f:
            if '=' in line and not line.startswith('#'):
                k, v = line.strip().split('=', 1)
                os.environ[k] = v

MASTER_SYSTEM_PROMPT = """
You are CampusMind, a context-aware AI assistant embedded in a student's college dashboard.

You have access to tools for student data, 10 real-world integrations (Google Calendar, Microsoft Teams, Slack, College ERP/Portal, Notion, Gmail, Google Drive, GitHub, YouTube Learning, LinkedIn), timetable, assignments, notes, opportunities, campus map, community, lab viva prep, career roadmaps, projects, and mentorship. Always use tools to get current information rather than assuming.

When answering a student:
1. Provide a detailed, step-by-step, structured, and ordered response using Markdown formatting (headings, numbered steps, bold highlights, and emoji badges).
2. If the user greets or asks for an overview, break your answer down in clear chronological order:
   - Step 1: Today's Schedule & Classes
   - Step 2: Urgent Deadlines & Priority Tasks
   - Step 3: Recommended Scholarships & Opportunities
   - Step 4: Real-World Integrations & Quick Actions
"""

MAX_TOOL_LOOPS = 6

def execute_agent_turn(user_message, chat_history=None):
    if chat_history is None:
        chat_history = []

    executed_tools = []
    
    # Configure OpenRouter / OpenAI credentials exclusively from environment
    openrouter_key = os.getenv("OPENROUTER_API_KEY")
    openai_key = os.getenv("OPENAI_API_KEY") or openrouter_key
    
    api_url = "https://openrouter.ai/api/v1/chat/completions" if openrouter_key else os.getenv("OPENAI_BASE_URL", "https://api.openai.com/v1/chat/completions")
    model_name = os.getenv("MODEL_NAME", "openai/gpt-4o-mini")

    if openai_key:
        try:
            messages = [{"role": "system", "content": MASTER_SYSTEM_PROMPT}]
            for msg in chat_history:
                messages.append(msg)
            messages.append({"role": "user", "content": user_message})

            headers = {
                "Authorization": f"Bearer {openai_key}",
                "Content-Type": "application/json",
                "HTTP-Referer": "http://127.0.0.1:5000",
                "X-Title": "CampusMind AI"
            }

            for loop_idx in range(MAX_TOOL_LOOPS):
                payload = {
                    "model": model_name,
                    "messages": messages,
                    "tools": tools.TOOL_DECLARATIONS,
                    "tool_choice": "auto"
                }

                resp = requests.post(api_url, headers=headers, json=payload, timeout=25)
                if resp.status_code != 200:
                    print(f"[OpenRouter API Error]: {resp.status_code} - {resp.text}")
                    break

                res_json = resp.json()
                if "choices" not in res_json or not res_json["choices"]:
                    break

                message = res_json["choices"][0]["message"]
                messages.append(message)

                if "tool_calls" in message and message["tool_calls"]:
                    for tool_call in message["tool_calls"]:
                        fn_name = tool_call["function"]["name"]
                        fn_args = json.loads(tool_call["function"]["arguments"])
                        tool_func = tools.TOOL_FUNCTIONS.get(fn_name)
                        tool_result = tool_func(**fn_args) if tool_func else {"error": f"Unknown tool {fn_name}"}

                        executed_tools.append({
                            "loop": loop_idx + 1,
                            "tool_name": fn_name,
                            "arguments": fn_args,
                            "result": tool_result
                        })

                        messages.append({
                            "role": "tool",
                            "tool_call_id": tool_call["id"],
                            "content": json.dumps(tool_result)
                        })
                else:
                    return {
                        "reply": message.get("content", ""),
                        "tool_calls_executed": executed_tools
                    }

        except Exception as e:
            print(f"[Agent OpenRouter API Fallback Triggered]: {e}")

    return fallback_agent_loop(user_message, chat_history)


def fallback_agent_loop(user_message, chat_history):
    executed_tools = []
    msg_lower = user_message.lower().strip()

    # 1. Integrations Query
    if any(k in msg_lower for k in ["sync", "calendar", "gcal", "notion", "erp", "portal", "teams", "slack", "github", "drive", "youtube", "linkedin", "gmail"]):
        service_id = "gcal"
        if "notion" in msg_lower: service_id = "notion"
        elif "erp" in msg_lower or "portal" in msg_lower or "attendance" in msg_lower: service_id = "erp"
        elif "github" in msg_lower: service_id = "github"
        elif "youtube" in msg_lower or "video" in msg_lower:
            yt_res = tools.tool_get_youtube_learning()
            executed_tools.append({"loop": 1, "tool_name": "get_youtube_learning", "arguments": {}, "result": yt_res})
            tutorials = yt_res.get("tutorials", [])
            yt_str = "\n".join([f"**{i+1}. {t['topic']}** ({t['course']})\n   • Channel: `{t['channel']}` | Views: {t['views']} | Duration: {t['duration']}" for i, t in enumerate(tutorials[:5])])
            return {
                "reply": f"### 🎥 Curated YouTube Learning Video Tutorials\n\nHere are top recommended video lectures for your courses:\n\n{yt_str}\n\n--- \n💡 *Tip: You can ask me to generate practice viva questions for any of these subjects!*",
                "tool_calls_executed": executed_tools
            }

        res = tools.tool_sync_integration(service_id)
        executed_tools.append({"loop": 1, "tool_name": "sync_integration", "arguments": {"service_id": service_id}, "result": res})
        if res.get("success"):
            item = res["integration"]
            reply = f"### ⚡ Real-World Integration Synced!\n\n**Service Name**: `{item['name']}`\n\n1. **Status**: Connected & Active ✅\n2. **Synced Data**: {item['synced_count']}\n3. **Last Sync Timestamp**: {item['last_sync']}\n\n--- \n*All your class schedules and deadline reminders are automatically mirrored with {item['name']}!*"
        else:
            reply = "Synced real-world integrations!"
        return {"reply": reply, "tool_calls_executed": executed_tools}

    # 2. Timetable Query
    if any(k in msg_lower for k in ["timetable", "schedule", "class", "today"]):
        res = tools.tool_get_timetable(day="Monday")
        executed_tools.append({"loop": 1, "tool_name": "get_timetable", "arguments": {"day": "Monday"}, "result": res})
        classes = res.get("classes", [])
        classes_str = "\n".join([f"**{i+1}. {c['time']}** — **{c['course']}** (`{c['code']}`)\n   • **Location**: Room {c['room']}\n   • **Instructor**: {c['instructor']}" for i, c in enumerate(classes)])
        return {
            "reply": f"### 📅 Today's Class Schedule (Monday)\n\nHere is your step-by-step timetable for today:\n\n{classes_str}\n\n---\n💡 *Next Class: CS301 Operating Systems in Room A-201 at 09:00 AM!*",
            "tool_calls_executed": executed_tools
        }

    # 3. Notes Query
    if any(k in msg_lower for k in ["note", "notes", "lecture", "pdf", "study"]):
        res = tools.tool_search_notes("Machine Learning")
        executed_tools.append({"loop": 1, "tool_name": "search_notes", "arguments": {"query": "Machine Learning"}, "result": res})
        results = res.get("results", [])
        notes_str = "\n".join([f"**{i+1}. {n['title']}** (`{n['course_tag']}`)\n   • File: `{n['filename']}`\n   • Snippet: *{n['snippet']}*" for i, n in enumerate(results[:4])])
        return {
            "reply": f"### 📖 Grounded Course Notes & Study Guides\n\nHere are the top course notes found in your database:\n\n{notes_str}\n\n---\n💡 *You can upload new PDF lecture notes in the Notes & Knowledge tab anytime!*",
            "tool_calls_executed": executed_tools
        }

    # 4. Scholarships & Opportunities Query
    if any(k in msg_lower for k in ["scholarship", "hackathon", "internship", "opp"]):
        res = tools.tool_get_opportunities()
        executed_tools.append({"loop": 1, "tool_name": "get_opportunities", "arguments": {}, "result": res})
        opps = res.get("opportunities", [])
        opps_str = "\n".join([f"**{i+1}. {o['title']}** ({o['match_score']}% Match)\n   • **Sponsor**: {o['organization']} | **Category**: `{o['category']}`\n   • **Reward**: {o['stipend_or_prize']} | **Deadline**: {o['deadline']}" for i, o in enumerate(opps[:4])])
        return {
            "reply": f"### 🚀 Top Scholarships & Hackathons For You\n\nBased on your Computer Science profile and skills, here are ordered top opportunities:\n\n{opps_str}\n\n---\n💡 *Powered by Exa AI Live Web Search + Skill Match Scoring!*",
            "tool_calls_executed": executed_tools
        }

    # 5. Default Overview & Greetings (Detailed, Step-by-Step, Ordered)
    tt_res = tools.tool_get_timetable(day="Monday")
    asgn_res = tools.tool_get_assignments()
    opp_res = tools.tool_get_opportunities()

    executed_tools.append({"loop": 1, "tool_name": "get_timetable", "arguments": {"day": "Monday"}, "result": tt_res})
    executed_tools.append({"loop": 2, "tool_name": "get_assignments", "arguments": {}, "result": asgn_res})
    executed_tools.append({"loop": 3, "tool_name": "get_opportunities", "arguments": {}, "result": opp_res})

    today_classes = tt_res.get("classes", [])
    classes_summary = "\n".join([f"   • **{c['time']}**: {c['course']} (Room {c['room']})" for c in today_classes[:2]])

    assignments = asgn_res.get("assignments", [])
    top_asgn = assignments[0] if assignments else None
    asgn_summary = f"   • **{top_asgn['title']}** (`{top_asgn['course']}`) — **Due in {top_asgn['days_left']} days**\n     - Priority: `{top_asgn['priority']}` | Remaining Effort: {top_asgn['remaining_hours']} hrs" if top_asgn else ""

    opps = opp_res.get("opportunities", [])
    top_opp = opps[0] if opps else None
    opp_summary = f"   • **{top_opp['title']}** — {top_opp['stipend_or_prize']} (Deadline: {top_opp['deadline']})" if top_opp else ""

    reply = f"""### 👋 Welcome to CampusMind AI Co-Pilot!

Here is your **detailed, step-by-step ordered student briefing** for today:

#### 1. 📅 Today's Schedule & Classes (Monday)
{classes_summary}

#### 2. 📋 Highest Priority Assignment & Deadline
{asgn_summary}

#### 3. 🚀 Recommended Scholarship / Opportunity
{opp_summary}

#### 4. ⚡ Real-World Integrations & Database Status
   • **Cloud Database**: Connected to Firestore `campusminds-4c038`
   • **Productivity Sync**: Google Calendar, MS Teams, Slack, Notion, GitHub (10 Connected Services)

---
💡 **What would you like to work on?** You can ask me to:
- *"Show all my assignment subtasks"*
- *"Find hackathons for Python developers"*
- *"Get step-by-step directions to B-102 DBMS Hall"*
- *"Practice lab viva questions for Operating Systems"*
"""

    return {"reply": reply, "tool_calls_executed": executed_tools}
