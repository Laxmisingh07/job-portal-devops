def test_get_applications_without_token(client):
    response = client.get("/api/applications")

    assert response.status_code in [401, 422]


def test_create_application_without_token(client):
    response = client.post(
        "/api/applications",
        json={
            "job_id": 1,
            "cover_letter": "I am interested in this job."
        }
    )

    assert response.status_code in [401, 422]