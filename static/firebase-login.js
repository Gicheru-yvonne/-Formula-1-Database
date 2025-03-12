// Firebase configuration (Replace with your own credentials)
const firebaseConfig = {
    apiKey: "AIzaSyCtrT-uXPnvYYeE88C6sOPL3diA4LNzg1c",
    authDomain: "my-project-yvonne-9ff25.firebaseapp.com",
    projectId: "my-project-yvonne-9ff25",
    storageBucket: "my-project-yvonne-9ff25.firebasestorage.app",
    messagingSenderId: "569288049886",
    appId: "1:569288049886:web:77376ba2f7faf881116e4f"
};

// Initialize Firebase
firebase.initializeApp(firebaseConfig);
const auth = firebase.auth();

// Function to handle login
function login() {
    const email = document.getElementById("email").value;
    const password = document.getElementById("password").value;

    auth.signInWithEmailAndPassword(email, password)
    .then((userCredential) => {
        document.cookie = `token=${userCredential.user.accessToken}; path=/; SameSite=Strict`;
        window.location.reload();
    })
    .catch((error) => {
        document.getElementById("error-message").innerText = error.message;
    });
}

// Function to handle signup
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

// Function to handle logout
function logout() {
    auth.signOut().then(() => {
        document.cookie = "token=; path=/; expires=Thu, 01 Jan 1970 00:00:00 UTC";
        window.location.reload();
    });
}

// Update UI based on login state
auth.onAuthStateChanged((user) => {
    if (user) {
        document.getElementById("user-email").innerText = user.email;
        document.getElementById("logout-btn").style.display = "block";
    } else {
        document.getElementById("user-email").innerText = "Guest";
        document.getElementById("logout-btn").style.display = "none";
    }
});

// ✅ Function to Add a Driver to Firestore
function addDriver() {
    const driverData = {
        driver_name: document.getElementById("driver-name").value,
        age: parseInt(document.getElementById("age").value),
        points_scored: parseInt(document.getElementById("points").value),
        world_titles: parseInt(document.getElementById("world-titles").value),
        pole_positions: parseInt(document.getElementById("pole-positions").value),
        fastest_laps: parseInt(document.getElementById("fastest-laps").value),
        team: document.getElementById("team").value
    };

    // Check if any field is empty
    if (Object.values(driverData).some(value => value === "" || isNaN(value) && typeof value !== "string")) {
        alert("Please fill out all fields correctly.");
        return;
    }

    console.log("Sending Driver Data:", driverData);

    fetch('/add_driver', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify(driverData)
    })
    .then(response => response.json())
    .then(data => {
        if (data.message) {
            alert("✅ Driver Added: " + data.message);
            document.getElementById("add-driver-form").reset(); // Reset form
        } else {
            throw new Error("Error adding driver.");
        }
    })
    .catch(error => {
        console.error("❌ Error:", error);
        alert("Error: " + error.message);
    });
}

// ✅ Function to Add a Team to Firestore
function addTeam() {
    const teamData = {
        team_name: document.getElementById("team-name").value,
        year_founded: parseInt(document.getElementById("year-founded").value),
        constructor_titles: parseInt(document.getElementById("constructor-titles").value),
        pole_positions: parseInt(document.getElementById("pole-positions-team").value),
        race_wins: parseInt(document.getElementById("race-wins").value),
        previous_season_position: parseInt(document.getElementById("previous-position").value)
    };

    // Check if any field is empty
    if (Object.values(teamData).some(value => value === "" || isNaN(value) && typeof value !== "string")) {
        alert("Please fill out all fields correctly.");
        return;
    }

    console.log("Sending Team Data:", teamData);

    fetch('/add_team', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify(teamData)
    })
    .then(response => response.json())
    .then(data => {
        if (data.message) {
            alert("✅ Team Added: " + data.message);
            document.getElementById("add-team-form").reset(); // Reset form
        } else {
            throw new Error("Error adding team.");
        }
    })
    .catch(error => {
        console.error("❌ Error:", error);
        alert("Error: " + error.message);
    });
}
