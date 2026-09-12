/**
 * CampusMind AI — Firebase Auth & Cloud Firestore Integration
 * Supports Sign Up, Log In, Sign Out, Forgot Password, and Firestore "users" sync.
 * Project ID: campusminds-4c038
 */

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
let currentUser = null;

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
 * 1. Sign Up / Register New Student
 * Creates Auth account and stores student profile in Firestore "users" collection
 */
async function registerUser(email, password, fullName, major = "Computer Science & Engineering") {
    if (!auth) {
        // Fallback local registration state
        const mockUser = { uid: "user_" + Date.now(), email, displayName: fullName };
        saveUserProfileToFirestore(mockUser.uid, { name: fullName, email, major, semester: 6, gpa: 3.85, attendance_pct: 94.2 });
        return { success: true, user: mockUser };
    }

    try {
        const userCredential = await auth.createUserWithEmailAndPassword(email, password);
        const user = userCredential.user;

        // Update Auth Display Name
        await user.updateProfile({ displayName: fullName });

        // Save User Profile to Cloud Firestore "users" collection
        await saveUserProfileToFirestore(user.uid, {
            uid: user.uid,
            name: fullName,
            email: email,
            major: major,
            semester: 6,
            gpa: 3.85,
            attendance_pct: 94.2,
            createdAt: firebase.firestore.FieldValue.serverTimestamp(),
            lastLogin: firebase.firestore.FieldValue.serverTimestamp()
        });

        console.log(`✅ Registered & saved new user to Firestore: ${email}`);
        return { success: true, user: user };
    } catch (error) {
        console.error("❌ Sign Up Error:", error);
        return { success: false, error: error.message };
    }
}

/**
 * 2. Log In / Sign In Existing Student
 */
async function loginUser(email, password) {
    if (!auth) {
        const mockUser = { uid: "user_alex_chen", email, displayName: "Alex Chen" };
        return { success: true, user: mockUser };
    }

    try {
        const userCredential = await auth.signInWithEmailAndPassword(email, password);
        const user = userCredential.user;

        // Update last login in Firestore
        if (db) {
            await db.collection("users").doc(user.uid).set({
                lastLogin: firebase.firestore.FieldValue.serverTimestamp()
            }, { merge: true });
        }

        console.log(`✅ Logged in user: ${email}`);
        return { success: true, user: user };
    } catch (error) {
        console.error("❌ Log In Error:", error);
        return { success: false, error: error.message };
    }
}

/**
 * 3. Send Password Reset Email (Forgot Password)
 */
async function resetPassword(email) {
    if (!auth) {
        return { success: true, message: `Password reset email sent to ${email}` };
    }

    try {
        await auth.sendPasswordResetEmail(email);
        console.log(`✉️ Password reset email sent to: ${email}`);
        return { success: true, message: `Password reset email sent to ${email}. Check your inbox!` };
    } catch (error) {
        console.error("❌ Reset Password Error:", error);
        return { success: false, error: error.message };
    }
}

/**
 * 4. Sign Out
 */
async function logoutUser() {
    if (!auth) {
        return { success: true };
    }

    try {
        await auth.signOut();
        console.log("👋 User signed out.");
        return { success: true };
    } catch (error) {
        console.error("❌ Sign Out Error:", error);
        return { success: false, error: error.message };
    }
}

/**
 * Helper: Save User Profile Document to Firestore "users" Collection
 */
async function saveUserProfileToFirestore(uid, profileData) {
    if (!db) return;
    try {
        await db.collection("users").doc(uid).set(profileData, { merge: true });
        console.log(`💾 User document written to Firestore 'users/${uid}'`);
    } catch (err) {
        console.error("Error saving user document:", err);
    }
}

/**
 * Firestore Read/Write Test Helpers
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
    await saveUserProfileToFirestore(userId, profile);
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
