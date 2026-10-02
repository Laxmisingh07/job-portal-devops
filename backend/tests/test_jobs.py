def test_get_jobs(client):
    response = client.get("/api/jobs")

    assert response.status_code == 200


def test_get_single_job(client):
    response = client.get("/api/jobs/1")

    assert response.status_code in [200, 404]