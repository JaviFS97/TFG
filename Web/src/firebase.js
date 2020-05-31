// File: firebase.js

import firebase from 'firebase/app'

// Add the Firebase products that you want to use
require("firebase/auth");
require("firebase/firestore");
require("firebase/functions");
require("firebase/storage");

// Your web app's Firebase configuration
var firebaseConfig = {
    apiKey: "******************", // Private
    authDomain: "tfg-smartgaraje.firebaseapp.com",
    databaseURL: "https://tfg-smartgaraje.firebaseio.com",
    projectId: "tfg-smartgaraje",
    storageBucket: "tfg-smartgaraje.appspot.com",
    messagingSenderId: "364683945573",
    appId: "1:364683945573:web:872aaf59885aa87d5f088c",
    measurementId: "G-0J0GJ1Z8E4"
  };

// Initialize Firebase
firebase.initializeApp(firebaseConfig);

const auth = firebase.auth()
const db = firebase.firestore()
const storage = firebase.storage()
const functions = firebase.functions()

export{
    firebase,
    auth,
    db,
    storage,
    functions
}