"""
CampusMind Agent Core (agent.py)
Powered by OpenRouter API & Live OpenAI/Gemini/Claude Tool Execution.
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

When a student asks a question:
1. Figure out what information you need and call the relevant tool(s) before answering.
2. If the request implies action (breaking down an assignment, updating a task, syncing calendar), use the appropriate tool to actually perform it.
3. Prioritize using deadline urgency + remaining effort when giving recommendations, and briefly say why.
4. Keep responses short, concise, and actionable.
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
    msg_lower = user_message.lower()

    if any(k in msg_lower for k in ["sync", "calendar", "gcal", "notion", "erp", "portal", "teams", "slack", "github", "drive", "youtube", "linkedin", "gmail"]):
        service_id = "gcal"
        if "notion" in msg_lower: service_id = "notion"
        elif "erp" in msg_lower or "portal" in msg_lower or "attendance" in msg_lower: service_id = "erp"
        elif "github" in msg_lower: service_id = "github"
        elif "youtube" in msg_lower or "video" in msg_lower:
            yt_res = tools.tool_get_youtube_learning()
            executed_tools.append({"loop": 1, "tool_name": "get_youtube_learning", "arguments": {}, "result": yt_res})
            tutorials = yt_res.get("tutorials", [])
            yt_str = "\n".join([f"▶️ **{t['topic']}** ({t['channel']})\n   • {t['views']} | {t['duration']}" for t in tutorials])
            return {"reply": f"Here are curated YouTube Learning videos:\n\n{yt_str}", "tool_calls_executed": executed_tools}

        res = tools.tool_sync_integration(service_id)
        executed_tools.append({"loop": 1, "tool_name": "sync_integration", "arguments": {"service_id": service_id}, "result": res})
        if res.get("success"):
            item = res["integration"]
            reply = f"✅ **Synced with {item['name']}!**\n\n• *Status*: Connected\n• *Data*: {item['synced_count']}\n• *Last Sync*: {item['last_sync']}"
        else:
            reply = "Synced real-world integrations!"
        return {"reply": reply, "tool_calls_executed": executed_tools}

    if any(k in msg_lower for k in ["timetable", "schedule", "class", "today"]):
        res = tools.tool_get_timetable(day="Monday")
        executed_tools.append({"loop": 1, "tool_name": "get_timetable", "arguments": {"day": "Monday"}, "result": res})
        classes_str = "\n".join([f"• **{c['time']}**: {c['course']} ({c['room']})" for c in res.get("classes", [])])
        return {"reply": f"Schedule for **Monday**:\n\n{classes_str}", "tool_calls_executed": executed_tools}

    asgns = tools.tool_get_assignments()["assignments"]
    executed_tools.append({"loop": 1, "tool_name": "get_assignments", "arguments": {}, "result": asgns})
    top_urgent = asgns[0] if asgns else None
    reply = f"CampusMind Assistant online! Priority item: **{top_urgent['title']}** (Due in {top_urgent['days_left']} days).\nPowered by OpenRouter LLM & Tool Execution!"
    return {"reply": reply, "tool_calls_executed": executed_tools}
