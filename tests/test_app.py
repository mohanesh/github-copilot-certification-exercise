import pytest


class TestRootEndpoint:
    """Tests for GET / endpoint"""

    def test_root_redirects_to_static_index(self, client):
        # Arrange
        expected_redirect_url = "/static/index.html"

        # Act
        response = client.get("/", follow_redirects=False)

        # Assert
        assert response.status_code in (307, 308)
        assert response.headers["location"] == expected_redirect_url


class TestGetActivities:
    """Tests for GET /activities endpoint"""

    def test_get_activities_returns_all_activities(self, client):
        # Arrange
        expected_activity_count = 9
        expected_activities = [
            "Chess Club", "Programming Class", "Gym Class", "Basketball Team",
            "Tennis Club", "Art Studio", "Music Band", "Debate Team", "Science Club"
        ]

        # Act
        response = client.get("/activities")
        data = response.json()

        # Assert
        assert response.status_code == 200
        assert len(data) == expected_activity_count
        assert all(activity in data for activity in expected_activities)

    def test_get_activities_has_correct_structure(self, client):
        # Arrange
        required_fields = ["description", "schedule", "max_participants", "participants"]

        # Act
        response = client.get("/activities")
        data = response.json()

        # Assert
        assert response.status_code == 200
        for activity_name, activity_details in data.items():
            for field in required_fields:
                assert field in activity_details, f"Missing field '{field}' in {activity_name}"

    def test_get_activities_participants_is_list(self, client):
        # Arrange - no specific arrangement needed

        # Act
        response = client.get("/activities")
        data = response.json()

        # Assert
        assert response.status_code == 200
        for activity_details in data.values():
            assert isinstance(activity_details["participants"], list)


class TestSignupEndpoint:
    """Tests for POST /activities/{activity_name}/signup endpoint"""

    def test_signup_successfully_adds_participant(self, client, clean_activities):
        # Arrange
        activity_name = "Chess Club"
        email = "newstudent@mergington.edu"
        initial_count = len(clean_activities[activity_name]["participants"])

        # Act
        response = client.post(
            f"/activities/{activity_name}/signup",
            params={"email": email}
        )

        # Assert
        assert response.status_code == 200
        assert response.json()["message"] == f"Signed up {email} for {activity_name}"
        assert len(clean_activities[activity_name]["participants"]) == initial_count + 1
        assert email in clean_activities[activity_name]["participants"]

    def test_signup_returns_404_for_nonexistent_activity(self, client):
        # Arrange
        nonexistent_activity = "Nonexistent Activity"
        email = "student@mergington.edu"

        # Act
        response = client.post(
            f"/activities/{nonexistent_activity}/signup",
            params={"email": email}
        )

        # Assert
        assert response.status_code == 404
        assert response.json()["detail"] == "Activity not found"

    def test_signup_returns_400_for_duplicate_signup(self, client):
        # Arrange
        activity_name = "Chess Club"
        email = "michael@mergington.edu"  # Already signed up

        # Act
        response = client.post(
            f"/activities/{activity_name}/signup",
            params={"email": email}
        )

        # Assert
        assert response.status_code == 400
        assert response.json()["detail"] == "Student already signed up for this activity"

    def test_signup_works_with_url_encoded_activity_name(self, client, clean_activities):
        # Arrange
        activity_name = "Programming Class"
        encoded_activity_name = "Programming%20Class"
        email = "newstudent@mergington.edu"

        # Act
        response = client.post(
            f"/activities/{encoded_activity_name}/signup",
            params={"email": email}
        )

        # Assert
        assert response.status_code == 200
        assert email in clean_activities[activity_name]["participants"]


class TestUnregisterEndpoint:
    """Tests for DELETE /activities/{activity_name}/unregister endpoint"""

    def test_unregister_successfully_removes_participant(self, client, clean_activities):
        # Arrange
        activity_name = "Chess Club"
        email = "michael@mergington.edu"  # Already signed up
        initial_count = len(clean_activities[activity_name]["participants"])

        # Act
        response = client.delete(
            f"/activities/{activity_name}/unregister",
            params={"email": email}
        )

        # Assert
        assert response.status_code == 200
        assert response.json()["message"] == f"Unregistered {email} from {activity_name}"
        assert len(clean_activities[activity_name]["participants"]) == initial_count - 1
        assert email not in clean_activities[activity_name]["participants"]

    def test_unregister_returns_404_for_nonexistent_activity(self, client):
        # Arrange
        nonexistent_activity = "Nonexistent Activity"
        email = "student@mergington.edu"

        # Act
        response = client.delete(
            f"/activities/{nonexistent_activity}/unregister",
            params={"email": email}
        )

        # Assert
        assert response.status_code == 404
        assert response.json()["detail"] == "Activity not found"

    def test_unregister_returns_400_for_not_enrolled_student(self, client):
        # Arrange
        activity_name = "Chess Club"
        email = "notenrolled@mergington.edu"  # Not signed up

        # Act
        response = client.delete(
            f"/activities/{activity_name}/unregister",
            params={"email": email}
        )

        # Assert
        assert response.status_code == 400
        assert response.json()["detail"] == "Student not signed up for this activity"

    def test_unregister_works_with_url_encoded_activity_name(self, client, clean_activities):
        # Arrange
        activity_name = "Programming Class"
        encoded_activity_name = "Programming%20Class"
        email = "emma@mergington.edu"  # Already signed up

        # Act
        response = client.delete(
            f"/activities/{encoded_activity_name}/unregister",
            params={"email": email}
        )

        # Assert
        assert response.status_code == 200
        assert email not in clean_activities[activity_name]["participants"]
