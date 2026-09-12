"""
CampusMind Backend Automated Test Suite
Verifies Flask endpoints, Tool Execution, and Agent Loop functionality.
"""

import unittest
import json
from app import app

class CampusMindTestCase(unittest.TestCase):
    def setUp(self):
        self.app = app.test_client()
        self.app.testing = True

    def test_01_dashboard_endpoint(self):
        """Test GET /dashboard returns classes, top urgent assignments & subtask count"""
        response = self.app.get('/dashboard')
        self.assertEqual(response.status_code, 200)
        res_json = json.loads(response.data)
        self.assertIn("today_classes", res_json)
        self.assertIn("urgent_assignments", res_json)
        self.assertIn("pending_subtask_count", res_json)
        self.assertGreaterEqual(len(res_json["urgent_assignments"]), 1)
        print("OK - GET /dashboard passed")

    def test_02_assignments_list_and_patch(self):
        """Test GET /assignments and PATCH /assignments/:id for subtask updates"""
        response = self.app.get('/assignments')
        self.assertEqual(response.status_code, 200)
        res_json = json.loads(response.data)
        self.assertGreaterEqual(len(res_json["assignments"]), 1)

        # Test subtask completion PATCH
        patch_res = self.app.patch('/assignments/asgn-1', json={
            "task_id": "task-103",
            "status": "Completed"
        })
        self.assertEqual(patch_res.status_code, 200)
        patch_json = json.loads(patch_res.data)
        self.assertTrue(patch_json["success"])
        self.assertEqual(patch_json["task"]["status"], "Completed")
        print("OK - GET /assignments and PATCH subtask passed")

    def test_03_agent_chat_tool_calling(self):
        """Test POST /agent/chat runs tool execution loop (max 6 loops cap)"""
        response = self.app.post('/agent/chat', json={
            "message": "What is my schedule for today?",
            "history": []
        })
        self.assertEqual(response.status_code, 200)
        res_json = json.loads(response.data)
        self.assertIn("reply", res_json)
        self.assertIn("tool_calls_executed", res_json)
        self.assertGreaterEqual(len(res_json["tool_calls_executed"]), 1)
        self.assertEqual(res_json["tool_calls_executed"][0]["tool_name"], "get_timetable")
        print("OK - POST /agent/chat with get_timetable tool calling passed")

    def test_04_notes_upload(self):
        """Test POST /notes/upload extracts text and grounds notes"""
        response = self.app.post('/notes/upload', json={
            "filename": "OS_Semaphores_Unit2.txt",
            "title": "OS Unit 2 Notes",
            "course_tag": "CS301",
            "content": "Binary Semaphores control access to shared memory critical sections."
        })
        self.assertEqual(response.status_code, 200)
        res_json = json.loads(response.data)
        self.assertTrue(res_json["success"])
        self.assertEqual(res_json["note"]["course_tag"], "CS301")
        print("OK - POST /notes/upload text grounding passed")

    def test_05_opportunities_search(self):
        """Test GET /opportunities returns skill-matched opportunities with gaps"""
        response = self.app.get('/opportunities?type=Hackathons')
        self.assertEqual(response.status_code, 200)
        res_json = json.loads(response.data)
        self.assertIn("opportunities", res_json)
        self.assertGreaterEqual(len(res_json["opportunities"]), 1)
        first_opp = res_json["opportunities"][0]
        self.assertIn("match_score", first_opp)
        self.assertIn("missing_skills", first_opp)
        print("OK - GET /opportunities passed")

if __name__ == '__main__':
    unittest.main()
