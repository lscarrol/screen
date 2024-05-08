import React, { useEffect, useState } from 'react';
import { initializeApp } from 'firebase/app';
import { getFirestore, collection, query, onSnapshot } from 'firebase/firestore';
import { Card, CardHeader, CardTitle, CardContent } from "@/components/ui/card";
import { motion } from 'framer-motion';

const firebaseConfig = {
  // Your Firebase configuration
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

    return () => unsubscribe();
  }, [username]);

  return (
    <div className="container mx-auto px-4">
      <h1 className="text-4xl font-bold mb-8">Categories</h1>
      <div className="grid grid-cols-1 md:grid-cols-2 gap-8">
        {Object.entries(categories).map(([category, items]) => (
          <motion.div
            key={category}
            initial={{ opacity: 0, y: 20 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ duration: 0.5 }}
          >
            <Card>
              <CardHeader>
                <CardTitle>{category}</CardTitle>
              </CardHeader>
              <CardContent>
                <motion.ul>
                  {items.map((item) => (
                    <motion.li
                      key={item.name}
                      initial={{ opacity: 0, x: -20 }}
                      animate={{ opacity: 1, x: 0 }}
                      transition={{ duration: 0.3 }}
                    >
                      <div className="text-lg font-bold">{item.name}</div>
                      <p className="text-gray-600">Location: {item.location}</p>
                      <p className="text-gray-600">Description: {item.description}</p>
                    </motion.li>
                  ))}
                </motion.ul>
              </CardContent>
            </Card>
          </motion.div>
        ))}
      </div>
    </div>
  );
};

export default CategoriesList;