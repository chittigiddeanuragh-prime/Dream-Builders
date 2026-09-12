/**
 * CampusMind AI — Firebase Cloud Firestore Configuration
 * Project Name: CampusMinds
 * Project ID: campusminds-4c038
 * Project Number: 89380595571
 */

// Firebase Web SDK Config
const firebaseConfig = {
    apiKey: "AIzaSyCampusMindsDemoApiKey123456789",
    authDomain: "campusminds-4c038.firebaseapp.com",
    projectId: "campusminds-4c038",
    storageBucket: "campusminds-4c038.appspot.com",
    messagingSenderId: "89380595571",
    appId: "1:89380595571:web:a1b2c3d4e5f67890"
};

// Initialize Firebase & Cloud Firestore
let db = null;
try {
    if (typeof firebase !== 'undefined') {
        if (!firebase.apps.length) {
            firebase.initializeApp(firebaseConfig);
        }
        db = firebase.firestore();
        console.log("🔥 Firebase Cloud Firestore Initialized for campusminds-4c038!");
    }
} catch (err) {
    console.warn("Firebase SDK initialization warning:", err);
}

/**
 * 1. Helper function to write a test user document in "users" collection
 */
async function writeTestUser(userId = "user_alex_chen", userData = null) {
    if (!db) {
        console.log("[Mock Firestore Write]: User test doc written for user_alex_chen");
        return { success: true, mock: true, userId: userId };
    }
    
    if (!userData) {
        userData = {
            name: "Alex Chen",
            email: "alex.chen@campusminds.edu",
            major: "Computer Science & Engineering",
            semester: 6,
            gpa: 3.85,
            attendance_pct: 94.2,
            createdAt: firebase.firestore.FieldValue.serverTimestamp()
        };
    }

    try {
        await db.collection("users").doc(userId).set(userData, { merge: true });
        console.log(`✅ Document successfully written to 'users/${userId}' in Firestore!`);
        return { success: true, userId: userId, data: userData };
    } catch (error) {
        console.error("❌ Error writing user document to Firestore:", error);
        return { success: false, error: error.message };
    }
}

/**
 * 2. Helper function to read a test user document from "users" collection
 */
async function readTestUser(userId = "user_alex_chen") {
    if (!db) {
        return {
            name: "Alex Chen",
            email: "alex.chen@campusminds.edu",
            major: "Computer Science & Engineering",
            semester: 6,
            gpa: 3.85
        };
    }

    try {
        const docSnap = await db.collection("users").doc(userId).get();
        if (docSnap.exists) {
            console.log(`📖 Document data from 'users/${userId}':`, docSnap.data());
            return docSnap.data();
        } else {
            console.log(`⚠️ No user document found for ID: ${userId}`);
            return null;
        }
    } catch (error) {
        console.error("❌ Error reading user document from Firestore:", error);
        return null;
    }
}

/**
 * 3. Helper function to sync assignment to "assignments" collection
 */
async function saveAssignmentToFirestore(asgn) {
    if (!db) return;
    try {
        await db.collection("assignments").doc(asgn.id).set(asgn, { merge: true });
        console.log(`✅ Assignment '${asgn.title}' synced to Firestore!`);
    } catch (err) {
        console.error("Error syncing assignment:", err);
    }
}

/**
 * 4. Helper function to sync note to "notes" collection
 */
async function saveNoteToFirestore(note) {
    if (!db) return;
    try {
        await db.collection("notes").doc(note.id).set(note, { merge: true });
        console.log(`✅ Note '${note.title}' synced to Firestore!`);
    } catch (err) {
        console.error("Error syncing note:", err);
    }
}
