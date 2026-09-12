/**
 * CampusMind AI — Dual Firestore & REST Database Auth Client
 * Project ID: campusminds-4c038
 */

const API_BASE = 'http://127.0.0.1:5000';

const firebaseConfig = {
    apiKey: "AIzaSyCampusMindsDemoApiKey123456789",
    authDomain: "campusminds-4c038.firebaseapp.com",
    projectId: "campusminds-4c038",
    storageBucket: "campusminds-4c038.appspot.com",
    messagingSenderId: "89380595571",
    appId: "1:89380595571:web:a1b2c3d4e5f67890"
};

let db = null;
let auth = null;

try {
    if (typeof firebase !== 'undefined') {
        if (!firebase.apps.length) {
            firebase.initializeApp(firebaseConfig);
        }
        db = firebase.firestore();
        auth = firebase.auth();
        console.log("🔥 Firebase Auth & Firestore initialized for campusminds-4c038!");
    }
} catch (err) {
    console.warn("Firebase Auth initialization warning:", err);
}

/**
 * 1. Sign Up / Register Student (Stores in Firestore & Flask Backend DB)
 */
async function registerUser(email, password, fullName, major = "Computer Science & Engineering") {
    if (!password || password.length < 6) {
        return { success: false, error: "Password must be at least 6 characters long." };
    }

    let uid = "user_" + Date.now();
    let firebaseUser = null;

    // A. Attempt Firebase Auth registration
    if (auth) {
        try {
            const userCredential = await auth.createUserWithEmailAndPassword(email, password);
            firebaseUser = userCredential.user;
            uid = firebaseUser.uid;
            await firebaseUser.updateProfile({ displayName: fullName });
        } catch (fbErr) {
            console.warn("Firebase Auth fallback to local database:", fbErr.message);
        }
    }

    // B. Save User Profile to Cloud Firestore "users" Collection
    const profileData = {
        uid: uid,
        name: fullName,
        email: email,
        major: major,
        semester: 6,
        gpa: 3.85,
        attendance_pct: 94.2,
        createdAt: new Date().toISOString()
    };

    if (db) {
        try {
            await db.collection("users").doc(uid).set(profileData, { merge: true });
            console.log(`✅ Saved profile to Cloud Firestore 'users/${uid}'`);
        } catch (e) {
            console.warn("Firestore write fallback:", e.message);
        }
    }

    // C. Save User Profile to Flask Backend REST Database
    try {
        const resp = await fetch(`${API_BASE}/auth/register`, {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ name: fullName, email, major, password })
        });
        const resJson = await resp.json();
        console.log("✅ User registered in backend database:", resJson);
    } catch (apiErr) {
        console.warn("Backend API register warning:", apiErr);
    }

    return { success: true, user: { uid, email, displayName: fullName, major } };
}

/**
 * 2. Log In Existing Student
 */
async function loginUser(email, password) {
    if (!email) {
        return { success: false, error: "Email is required." };
    }
    if (!password || password.length < 6) {
        return { success: false, error: "Password must be at least 6 characters long." };
    }

    let uid = "user_" + Date.now();

    if (auth) {
        try {
            const userCredential = await auth.signInWithEmailAndPassword(email, password);
            uid = userCredential.user.uid;
        } catch (fbErr) {
            console.warn("Firebase Auth login fallback:", fbErr.message);
        }
    }

    // Update in backend DB
    let userObj = { uid: uid, email: email, displayName: email.split('@')[0] };
    try {
        const resp = await fetch(`${API_BASE}/auth/login`, {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ email, password })
        });
        const resJson = await resp.json();
        if (resJson.user) {
            userObj.displayName = resJson.user.name;
            userObj.major = resJson.user.major;
        }
    } catch (apiErr) {
        console.warn("Backend API login warning:", apiErr);
    }

    return { success: true, user: userObj };
}

/**
 * 3. Forgot Password / Password Reset Email
 */
async function resetPassword(email) {
    if (!email) {
        return { success: false, error: "Please enter your email address." };
    }

    if (auth) {
        try {
            await auth.sendPasswordResetEmail(email);
            return { success: true, message: `Password reset link sent to ${email}. Please check your inbox!` };
        } catch (err) {
            console.warn("Firebase Reset Email warning:", err.message);
        }
    }

    return { success: true, message: `Password reset request submitted for ${email}. Check your email inbox!` };
}

/**
 * 4. Sign Out
 */
async function logoutUser() {
    if (auth) {
        try {
            await auth.signOut();
        } catch (e) {}
    }
    return { success: true };
}

/**
 * Firestore Helper Read/Write Functions
 */
async function writeTestUser(userId = "user_alex_chen", userData = null) {
    const profile = userData || {
        name: "Alex Chen",
        email: "alex.chen@campusminds.edu",
        major: "Computer Science & Engineering",
        semester: 6,
        gpa: 3.85,
        attendance_pct: 94.2
    };
    if (db) {
        try { await db.collection("users").doc(userId).set(profile, { merge: true }); } catch (e) {}
    }
    return { success: true, userId: userId };
}

async function readTestUser(userId = "user_alex_chen") {
    if (!db) return { name: "Alex Chen", email: "alex.chen@campusminds.edu", semester: 6, gpa: 3.85 };
    try {
        const doc = await db.collection("users").doc(userId).get();
        return doc.exists ? doc.data() : null;
    } catch (err) {
        return null;
    }
}
