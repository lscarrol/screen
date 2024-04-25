import React, { useEffect, useState } from 'react';
import { initializeApp } from 'firebase/app';
import { getFirestore, collection, query, onSnapshot } from 'firebase/firestore';
import styled from 'styled-components';
import { motion } from 'framer-motion';

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

const CategoriesListContainer = styled.div`
  background-color: #f0f0f0;
  min-height: 100vh;
  padding: 2rem 0;
`;

const CategoryCard = styled(motion.div)`
  background-color: white;
  border-radius: 1rem;
  box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
  padding: 1.5rem;
  transition: transform 0.3s ease;

  &:hover {
    transform: scale(1.05);
  }
`;

const ItemList = styled(motion.ul)`
  list-style-type: none;
  margin: 0;
  padding: 0;
`;

const ListItem = styled(motion.li)`
  border-bottom: 1px solid #e0e0e0;
  padding-bottom: 1rem;
  margin-bottom: 1rem;

  &:last-child {
    border-bottom: none;
    margin-bottom: 0;
    padding-bottom: 0;
  }
`;

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
    <CategoriesListContainer>
      <div className="container mx-auto px-4">
        <h1 className="text-4xl font-bold mb-8">Categories</h1>
        <div className="grid grid-cols-1 md:grid-cols-2 gap-8">
          {Object.entries(categories).map(([category, items]) => (
            <CategoryCard
              key={category}
              initial={{ opacity: 0, y: 20 }}
              animate={{ opacity: 1, y: 0 }}
              transition={{ duration: 0.5 }}
            >
              <h2 className="text-2xl font-bold mb-4">{category}</h2>
              <ItemList>
                {items.map((item) => (
                  <ListItem
                    key={item.name}
                    initial={{ opacity: 0, x: -20 }}
                    animate={{ opacity: 1, x: 0 }}
                    transition={{ duration: 0.3 }}
                  >
                    <div className="text-lg font-bold">{item.name}</div>
                    <p className="text-gray-600">Location: {item.location}</p>
                    <p className="text-gray-600">Description: {item.description}</p>
                  </ListItem>
                ))}
              </ItemList>
            </CategoryCard>
          ))}
        </div>
      </div>
    </CategoriesListContainer>
  );
};

export default CategoriesList;