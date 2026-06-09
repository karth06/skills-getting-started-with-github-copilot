import pytest


class TestUnregisterFromActivity:
    """Tests for the DELETE /activities/{activity_name}/unregister endpoint"""

    def test_unregister_success(self, client, reset_activities):
        """
        ARRANGE: Use email already registered for activity
        ACT: Submit unregister request
        ASSERT: Request succeeds and participant is removed
        """
        # Arrange
        activity = "Chess Club"
        email = "michael@mergington.edu"
        
        # Act
        response = client.delete(
            f"/activities/{activity}/unregister",
            params={"email": email}
        )
        
        # Assert
        assert response.status_code == 200
        assert email in response.json().get("message", "")

    def test_unregister_removes_participant(self, client, reset_activities):
        """
        ARRANGE: Get initial participant count
        ACT: Unregister a participant
        ASSERT: Participant count decreases by one and email is gone
        """
        # Arrange
        activity = "Chess Club"
        email = "michael@mergington.edu"
        initial_count = len(client.get("/activities").json()[activity]["participants"])
        
        # Act
        response = client.delete(
            f"/activities/{activity}/unregister",
            params={"email": email}
        )
        
        # Assert
        assert response.status_code == 200
        updated_count = len(client.get("/activities").json()[activity]["participants"])
        assert updated_count == initial_count - 1
        assert email not in client.get("/activities").json()[activity]["participants"]

    def test_unregister_not_registered_fails(self, client, reset_activities):
        """
        ARRANGE: Use email not registered for the activity
        ACT: Attempt to unregister non-registered email
        ASSERT: Request fails with 400 status and appropriate error message
        """
        # Arrange
        activity = "Chess Club"
        email = "notregistered@mergington.edu"
        
        # Act
        response = client.delete(
            f"/activities/{activity}/unregister",
            params={"email": email}
        )
        
        # Assert
        assert response.status_code == 400
        assert "not registered" in response.json().get("detail", "").lower()

    def test_unregister_invalid_activity_fails(self, client, reset_activities):
        """
        ARRANGE: Use a non-existent activity name
        ACT: Attempt to unregister from invalid activity
        ASSERT: Request fails with 404 status
        """
        # Arrange
        activity = "Nonexistent Club"
        email = "student@mergington.edu"
        
        # Act
        response = client.delete(
            f"/activities/{activity}/unregister",
            params={"email": email}
        )
        
        # Assert
        assert response.status_code == 404
        assert "not found" in response.json().get("detail", "").lower()

    def test_unregister_returns_success_message(self, client, reset_activities):
        """
        ARRANGE: Prepare valid unregister data
        ACT: Unregister participant
        ASSERT: Response contains success message with email and activity
        """
        # Arrange
        activity = "Gym Class"
        email = "john@mergington.edu"
        
        # Act
        response = client.delete(
            f"/activities/{activity}/unregister",
            params={"email": email}
        )
        
        # Assert
        assert response.status_code == 200
        message = response.json()["message"]
        assert email in message
        assert activity in message
