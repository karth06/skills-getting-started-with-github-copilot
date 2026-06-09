import pytest


class TestGetActivities:
    """Tests for the GET /activities endpoint"""

    def test_get_activities_returns_all_activities(self, client, reset_activities):
        """
        ARRANGE: No setup needed, activities fixture provides test data
        ACT: Make GET request to /activities
        ASSERT: Response contains all activities with correct structure
        """
        # Act
        response = client.get("/activities")
        
        # Assert
        assert response.status_code == 200
        data = response.json()
        assert "Chess Club" in data
        assert "Programming Class" in data
        assert "Gym Class" in data

    def test_activities_have_required_fields(self, client, reset_activities):
        """
        ARRANGE: Activities are loaded via fixture
        ACT: Get activities and check structure
        ASSERT: Each activity has all required fields
        """
        # Act
        response = client.get("/activities")
        data = response.json()
        
        # Assert
        for activity_name, activity_data in data.items():
            assert "description" in activity_data
            assert "schedule" in activity_data
            assert "max_participants" in activity_data
            assert "participants" in activity_data
            assert isinstance(activity_data["participants"], list)

    def test_activities_show_correct_participant_count(self, client, reset_activities):
        """
        ARRANGE: Activities with known participant counts
        ACT: Fetch activities
        ASSERT: Participant counts match expectations
        """
        # Act
        response = client.get("/activities")
        data = response.json()
        
        # Assert
        assert len(data["Chess Club"]["participants"]) == 2
        assert len(data["Programming Class"]["participants"]) == 2
        assert len(data["Gym Class"]["participants"]) == 2
