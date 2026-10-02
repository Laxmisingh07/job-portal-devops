const API_URL = "http://localhost:5000/api";

function getToken() {
    return localStorage.getItem("token");
}

function getUser() {
    const user = localStorage.getItem("user");

    if (!user) {
        return null;
    }

    return JSON.parse(user);
}

function saveLogin(data) {
    localStorage.setItem("token", data.token);
    localStorage.setItem("user", JSON.stringify(data.user));
}

function logout() {
    localStorage.removeItem("token");
    localStorage.removeItem("user");

    window.location.href = "login.html";
}

async function apiRequest(
    endpoint,
    method = "GET",
    body = null,
    authenticated = false
) {
    const options = {
        method: method,
        headers: {
            "Content-Type": "application/json"
        }
    };

    if (authenticated) {
        options.headers["Authorization"] =
            "Bearer " + getToken();
    }

    if (body) {
        options.body = JSON.stringify(body);
    }

    const response = await fetch(
        API_URL + endpoint,
        options
    );

    const data = await response.json();

    if (!response.ok) {
        throw new Error(
            data.message || "Something went wrong"
        );
    }

    return data;
}