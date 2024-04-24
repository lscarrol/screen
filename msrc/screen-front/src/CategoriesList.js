import React, { useEffect, useState } from 'react';
import { initializeApp } from 'firebase/app';
import { getFirestore, collection, query, onSnapshot } from 'firebase/firestore';

const firebaseConfig = {
  apiKey: "",
  authDomain: "screenr-cd3f7.firebaseapp.com",
  databaseURL: "https://screenr-cd3f7-default-rtdb.firebaseio.com",
  projectId: "screenr-cd3f7",
  storageBucket: "screenr-cd3f7.appspot.com",
  messagingSenderId: "547680519195",
  appId: "1:547680519195:web:a2059eaf4709af8cb1e4be",
  measurementId: "G-ECKDZ2RQD4"
};

const app = initializeApp(firebaseConfig);
const db = getFirestore(app);

const CategoriesList = ({ username }) => {
  const [categories, setCategories] = useState({
    Book: [],
    Movie: [],
    Recipe: [],
    Restaurant: [],
  });

  useEffect(() => {
    const categoriesRef = collection(db, 'screenshots', username, 'categories');
    const unsubscribe = onSnapshot(categoriesRef, (snapshot) => {
      const newCategories = {
        Book: [],
        Movie: [],
        Recipe: [],
        Restaurant: [],
      };

      snapshot.forEach((categoryDoc) => {
        const categoryData = categoryDoc.data();
        const category = categoryData.category;

        if (newCategories.hasOwnProperty(category)) {
          newCategories[category].push({
            name: categoryDoc.id,
            location: categoryData.location,
            description: categoryData.description,
          });
        }
      });

      setCategories(newCategories);
    });

    // Unsubscribe from the listener when the component unmounts
    return () => unsubscribe();
  }, [username]);

  return (
    <div className="container mx-auto px-4 py-8">
      <h1 className="text-4xl font-bold mb-8">Categories</h1>
      <div className="grid grid-cols-1 md:grid-cols-2 gap-8">
        {Object.entries(categories).map(([category, items]) => (
          <div key={category} className="bg-white rounded-lg shadow-md p-6">
            <h2 className="text-2xl font-bold mb-4">{category}</h2>
            <ul className="space-y-4">
              {items.map((item) => (
                <li key={item.name} className="border-b pb-4">
                  <div className="text-lg font-bold">{item.name}</div>
                  <p className="text-gray-600">Location: {item.location}</p>
                  <p className="text-gray-600">Description: {item.description}</p>
                </li>
              ))}
            </ul>
          </div>
        ))}
      </div>
    </div>
  );
};

export default CategoriesList;