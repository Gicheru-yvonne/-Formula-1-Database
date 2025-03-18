// Firebase configuration (Replace with your own credentials)
const firebaseConfig = {
    apiKey: "AIzaSyCtrT-uXPnvYYeE88C6sOPL3diA4LNzg1c",
    authDomain: "my-project-yvonne-9ff25.firebaseapp.com",
    projectId: "my-project-yvonne-9ff25",
    storageBucket: "my-project-yvonne-9ff25.firebasestorage.app",
    messagingSenderId: "569288049886",
    appId: "1:569288049886:web:77376ba2f7faf881116e4f"
};

firebase.initializeApp(firebaseConfig);
const auth = firebase.auth();

function login() {
    const email = document.getElementById("email").value;
    const password = document.getElementById("password").value;

    auth.signInWithEmailAndPassword(email, password)
    .then((userCredential) => {
        console.log("✅ Login Successful:", userCredential.user.email);
        document.cookie = `token=${userCredential.user.accessToken}; path=/; SameSite=Strict`;
        window.location.reload(); // ✅ Refresh the page after login
    })
    .catch((error) => {
        console.error("❌ Login Error:", error.message);
        alert("Login failed: " + error.message); // ✅ Show login error message
    });
}


function signup() {
    const email = document.getElementById("email").value;
    const password = document.getElementById("password").value;

    auth.createUserWithEmailAndPassword(email, password)
        .then(() => {
            alert("Signup successful! You can now log in.");
        })
        .catch((error) => {
            document.getElementById("error-message").innerText = error.message;
        });
}

function logout() {
    auth.signOut().then(() => {
        document.cookie = "token=; path=/; expires=Thu, 01 Jan 1970 00:00:00 UTC";
        window.location.reload();
    });
}

auth.onAuthStateChanged((user) => {
    if (user) {
        document.getElementById("user-email").innerText = user.email;
        document.getElementById("logout-btn").style.display = "block";
    } else {
        document.getElementById("user-email").innerText = "Guest";
        document.getElementById("logout-btn").style.display = "none";
    }
});

function addDriver() {
    const user = firebase.auth().currentUser;
    if (!user) {
        alert("You must be logged in to add a driver.");
        return;
    }

    user.getIdToken().then((token) => {
        const driverData = {
            driver_name: document.getElementById("driver_name").value.trim(),
            age: parseInt(document.getElementById("age").value) || 0,
            points_scored: parseInt(document.getElementById("points").value) || 0,
            world_titles: parseInt(document.getElementById("world-titles").value) || 0,
            pole_positions: parseInt(document.getElementById("pole-positions").value) || 0,
            fastest_laps: parseInt(document.getElementById("fastest-laps").value) || 0,
            team: document.getElementById("team").value.trim()
        };

        if (!driverData.driver_name || !driverData.team) {
            alert("Driver name and team are required.");
            return;
        }

        fetch('/add_driver', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                'Authorization': `Bearer ${token}`
            },
            body: JSON.stringify(driverData)
        })
        .then(response => response.json())
        .then(data => {
            console.log("🔍 Response from Server:", data);
            if (data.message) {
                alert("✅ Driver Added: " + data.message);
                document.querySelector("#add-driver-form form").reset(); // ✅ Corrected
            } else {
                throw new Error(data.error || "Error adding driver.");
            }
        })
        
        .catch(error => {
            alert("Error: " + error.message);
        });
    });
}

function addTeam() {
    const user = firebase.auth().currentUser;
    if (!user) {
        alert("You must be logged in to add a team.");
        return;
    }

    user.getIdToken().then((token) => {
        const teamData = {
            team_name: document.getElementById("team_name").value.trim(),
            year_founded: parseInt(document.getElementById("year_founded").value) || 0,
            constructor_titles: parseInt(document.getElementById("constructor_titles").value) || 0,
            pole_positions: parseInt(document.getElementById("pole_positions").value) || 0,
            race_wins: parseInt(document.getElementById("race_wins").value) || 0,
            previous_season_position: parseInt(document.getElementById("previous_season_position").value) || 0,
        };
        

        // ✅ Ensure all required fields are filled
        if (!teamData.team_name || teamData.year_founded === 0) {
            alert("Error: Team name and year founded are required.");
            return;
        }

        console.log("🔍 Sending Team Data:", JSON.stringify(teamData));

        fetch('/add_team', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                'Authorization': `Bearer ${token}`
            },
            body: JSON.stringify(teamData)
        })
        .then(response => response.json())
        .then(data => {
            console.log("🔍 Response from Server:", data);
            if (data.message) {
                alert("✅ Team Added: " + data.message);
                document.querySelector("#add-team-form form").reset();
            } else {
                throw new Error(data.error || "Error adding team.");
            }
        })
        .catch(error => {
            console.error("❌ Error:", error);
            alert("Error: " + error.message);
        });
    });
}




function queryDrivers() {
    const attribute = document.getElementById("query-attribute").value;
    const condition = document.getElementById("query-condition").value;
    const value = parseInt(document.getElementById("query-value").value);

    if (isNaN(value)) {
        alert("Please enter a valid number.");
        return;
    }

    const queryData = { attribute, condition, value };

    console.log("Sending Query: ", queryData);

    fetch('/query_drivers', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify(queryData)
    })
    .then(response => response.json())
    .then(data => {
        console.log("Query Results: ", data);
        
        const resultsList = document.getElementById("query-results");
        resultsList.innerHTML = "";

        if (data.drivers.length === 0) {
            resultsList.innerHTML = "<li>No drivers found.</li>";
        } else {
            data.drivers.forEach(driver => {
                const listItem = document.createElement("li");
                listItem.textContent = `${driver.driver_name} - ${attribute}: ${driver[attribute]}`;
                resultsList.appendChild(listItem);
            });
        }
    })
    .catch(error => {
        console.error("Error:", error);
        alert("Failed to retrieve drivers.");
    });
}
function queryTeams() {
    const attribute = document.getElementById("query-attribute").value;
    const condition = document.getElementById("query-condition").value;
    const value = parseInt(document.getElementById("query-value").value);

    if (isNaN(value)) {
        alert("Please enter a valid number.");
        return;
    }

    const queryData = { attribute, condition, value };

    console.log("Sending Query: ", queryData);

    fetch('/query_teams', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify(queryData)
    })
    .then(response => response.json())
    .then(data => {
        console.log("Query Results: ", data);
        
        const resultsList = document.getElementById("query-results");
        resultsList.innerHTML = "";

        if (data.teams.length === 0) {
            resultsList.innerHTML = "<li>No teams found.</li>";
        } else {
            data.teams.forEach(team => {
                const listItem = document.createElement("li");
                listItem.textContent = `${team.team_name} - ${attribute}: ${team[attribute]}`;
                resultsList.appendChild(listItem);
            });
        }
    })
    .catch(error => {
        console.error("Error:", error);
        alert("Failed to retrieve teams.");
    });
}


