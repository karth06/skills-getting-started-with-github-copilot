import pytest


class TestSignupForActivity:
    """Tests for the POST /activities/{activity_name}/signup endpoint"""

    def test_signup_success(self, client, reset_activities):
        """
        ARRANGE: Prepare email and valid activity name
        ACT: Submit signup request with new participant
        ASSERT: Request succeeds and participant is added
        """
        # Arrange
        activity = "Chess Club"
        email = "newstudent@mergington.edu"
        
        # Act
        response = client.post(
            f"/activities/{activity}/signup",
            params={"email": email}
        )
        
        # Assert
        assert response.status_code == 200
        assert email in response.json().get("message", "")

    def test_signup_adds_participant_to_list(self, client, reset_activities):
        """
        ARRANGE: Get initial participant count
        ACT: Sign up a new participant
        ASSERT: Participant is added to the activity's participant list
        """
        # Arrange
        activity = "Chess Club"
        email = "newstudent@mergington.edu"
        initial_count = len(client.get("/activities").json()[activity]["participants"])
        
        # Act
        response = client.post(
            f"/activities/{activity}/signup",
            params={"email": email}
        )
        
        # Assert
        assert response.status_code == 200
        updated_count = len(client.get("/activities").json()[activity]["participants"])
        assert updated_count == initial_count + 1

    def test_signup_duplicate_email_fails(self, client, reset_activities):
        """
        ARRANGE: Use an email already registered for the activity
        ACT: Attempt to sign up same email again
        ASSERT: Request fails with 400 status and appropriate error message
        """
        # Arrange
        activity = "Chess Club"
        email = "michael@mergington.edu"  # Already registered
        
        # Act
        response = client.post(
            f"/activities/{activity}/signup",
            params={"email": email}
        )
        
        # Assert
        assert response.status_code == 400
        assert "already signed up" in response.json().get("detail", "").lower()

    def test_signup_invalid_activity_fails(self, client, reset_activities):
        """
        ARRANGE: Use a non-existent activity name
        ACT: Attempt to sign up for invalid activity
        ASSERT: Request fails with 404 status
        """
        # Arrange
        activity = "Nonexistent Club"
        email = "student@mergington.edu"
        
        # Act
        response = client.post(
            f"/activities/{activity}/signup",
            params={"email": email}
        )
        
        # Assert
        assert response.status_code == 404
        assert "not found" in response.json().get("detail", "").lower()

    def test_signup_returns_success_message(self, client, reset_activities):
        """
        ARRANGE: Prepare valid signup data
        ACT: Sign up participant
        ASSERT: Response contains success message with email and activity
        """
        # Arrange
        activity = "Programming Class"
        email = "alice@mergington.edu"
        
        # Act
        response = client.post(
            f"/activities/{activity}/signup",
            params={"email": email}
        )
        
        # Assert
        assert response.status_code == 200
        message = response.json()["message"]
        assert email in message
        assert activity in message
