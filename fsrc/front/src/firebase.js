import { initializeApp } from 'firebase/app';
import { getAuth } from 'firebase/auth';

const firebaseConfig = {
  apiKey: "AIzaSyCR6FXA2crXmeXyTBAyqzk68iBd-rwPQZ0",
  authDomain: "screenr-cd3f7.firebaseapp.com",
  databaseURL: "https://screenr-cd3f7-default-rtdb.firebaseio.com",
  projectId: "screenr-cd3f7",
  storageBucket: "screenr-cd3f7.appspot.com",
  messagingSenderId: "547680519195",
  appId: "1:547680519195:web:a2059eaf4709af8cb1e4be",
  measurementId: "G-ECKDZ2RQD4"
};

const app = initializeApp(firebaseConfig);
const auth = getAuth(app);

export { auth };