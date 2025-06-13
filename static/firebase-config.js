// Firebase public config — safe to expose
// This file contains only client-side Firebase config values
// DO NOT include any private keys or service account credentials here

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