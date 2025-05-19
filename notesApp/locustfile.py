from locust import HttpUser, TaskSet, task, between
import random

class UserBehavior(TaskSet):
    def on_start(self):
        """Login and store JWT access token"""
        response = self.client.post("/api/user/login/", json={
            "email": "johndoe@example.com",
            "password": "TestPass123!"
        })

        print("Login Status:", response.status_code)
        if response.status_code != 200:
            print("Login failed! Response:", response.text)
            self.interrupt()

        try:
            token = response.json()["access"]
            self.client.headers = {"Authorization": f"Bearer {token}"}
        except Exception as e:
            print("Error getting token:", e)
            self.interrupt()

        self.note_ids = []

    @task(1)
    def create_note(self):
        """POST /api/user/notes/"""
        title = f"Note {random.randint(1000, 9999)}"
        content = "This is a load test note."

        response = self.client.post("/api/user/notes/", json={
            "title": title,
            "content": content
        })

        if response.status_code == 201:
            note_id = response.json().get("id")
            if note_id:
                self.note_ids.append(note_id)

    @task(2)
    def list_notes(self):
        """GET /api/user/notes/"""
        self.client.get("/api/user/notes/")

    @task(1)
    def update_note(self):
        """PUT /api/user/notes/<id>/"""
        if not self.note_ids:
            return

        note_id = random.choice(self.note_ids)
        self.client.put(f"/api/user/notes/{note_id}/", json={
            "title": "Updated title",
            "content": "Updated content from load test"
        })

    @task(1)
    def delete_note(self):
        """DELETE /api/user/notes/<id>/"""
        if not self.note_ids:
            return

        note_id = self.note_ids.pop()
        self.client.delete(f"/api/user/notes/{note_id}/")


class WebsiteUser(HttpUser):
    tasks = [UserBehavior]
    wait_time = between(1, 2)
