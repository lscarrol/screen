import React, { useEffect, useState } from 'react';
import { initializeApp } from 'firebase/app';
import { getFirestore, collection, query, onSnapshot } from 'firebase/firestore';
import { Card, CardHeader, CardTitle, CardContent } from '@/components/ui/card';
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

interface Category {
  name: string;
  location: string;
  description: string;
}

interface CategoriesListProps {
  username: string;
}

const CategoriesList: React.FC<CategoriesListProps> = ({ username }) => {
  const [categories, setCategories] = useState<Record<string, Category[]>>({
    Book: [],
    Movie: [],
    Recipe: [],
    Restaurant: [],
  });

  useEffect(() => {
    const categoriesRef = collection(db, 'screenshots', username, 'categories');
    const unsubscribe = onSnapshot(categoriesRef, (snapshot) => {
      const newCategories: Record<string, Category[]> = {
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
    <div className="bg-white min-h-screen">
      <nav className="bg-white py-4 ">
        <div className="flex justify-between items-center px-4 mx-auto max-w-7xl">
          <div className="text-xl font-bold">screen</div>
          <div>{username}</div>
        </div>
      </nav>
      <div className="container mx-auto px-4 py-8">
        <div className="grid grid-cols-1 md:grid-cols-2 gap-8">
          {Object.entries(categories).map(([category, items]) => (
            <motion.div
              key={category}
              initial={{ opacity: 0, scale: 0.8 }}
              animate={{ opacity: 1, scale: 1 }}
              transition={{ duration: 0.6 }}
            >
              <Card className="rounded-lg shadow-lg">
                <CardHeader>
                  <CardTitle>{category}s</CardTitle>
                  <div className="w-3/4 h-px bg-gray-200 mt-2"></div>
                </CardHeader>
                <CardContent>
                  <motion.ul>
                    {items.map((item, index) => (
                      <motion.li
                        key={item.name}
                        className={`py-2 ${index !== items.length - 1 ? 'border-b border-gray-200' : ''}`}
                        initial={{ opacity: 0, x: -20 }}
                        animate={{ opacity: 1, x: 0 }}
                        transition={{ duration: 0.4 }}
                      >
                        <div className="font-medium">{item.name}</div>
                        {item.location !== 'N/A' && (
                          <p className="text-gray-600">Location: {item.location}</p>
                        )}
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
    </div>
  );
};

export default CategoriesList;