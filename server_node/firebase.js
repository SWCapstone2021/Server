var admin  = require('firebase-admin');
import serviceAccount from './credential.json';
import firebase from "firebase/app";
import "firebase/auth";
import "firebase/database";


 const firebaseConfig = {
    apiKey: "AIzaSyATuPUaK9vNK_Z4R3p1LM2ZcP672UWgbKM",
    authDomain: "findyou-22c20.firebaseapp.com",
    projectId: "findyou-22c20",
    storageBucket: "findyou-22c20.appspot.com",
    messagingSenderId: "856124733777",
    databaseURL: "https://findyou-22c20-default-rtdb.firebaseio.com",
    appId: "1:856124733777:web:e6e31ec0823c5e53ecbb70",
    measurementId: "G-N2PCS34H2H"
  };

firebase.initializeApp(firebaseConfig);
const database = firebase.database();
const auth = firebase.auth(); 
admin.initializeApp({
    credential: admin.credential.cert(serviceAccount),
    databaseURL: "https://findyou-22c20-default-rtdb.firebaseio.com/",
    databaseAuthVariableOverride: null
  }, "DB");
/*  const firebase_admin = admin.initializeApp({
    credential: admin.credential.cert(serviceAccount),
    databaseURL: "https://findyou-22c20-default-rtdb.firebaseio.com",
    databaseAuthVariableOverride: null
  }); */
//}

export { admin, database }; 

