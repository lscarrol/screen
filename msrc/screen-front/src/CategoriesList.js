import React, { useEffect, useState } from 'react';
import { initializeApp } from 'firebase/app';
import { getFirestore, collection, query, getDocs } from 'firebase/firestore';

const firebaseConfig = {

};

const app = initializeApp(firebaseConfig);
const db = getFirestore(app);

const CategoriesList = ({ username }) => {
  const [categories, setCategories] = useState([]);

  useEffect(() => {
    const fetchCategories = async () => {
      const categoriesRef = collection(db, 'screenshots', username, 'categories');
      const q = query(categoriesRef);

      console.log('Fetching categories for username:', username);
      console.log('Categories collection ref:', categoriesRef);
      console.log('Categories query:', q);

      const querySnapshot = await getDocs(q);
      const categoriesData = querySnapshot.docs.map((doc) => ({
        id: doc.id,
        ...doc.data(),
      }));

      console.log('Categories data:', categoriesData);
      setCategories(categoriesData);
    };

    fetchCategories();
  }, [username]);

  console.log('Rendering categories:', categories);

  return (
    <div className="bg-white shadow-md rounded px-8 pt-6 pb-8 mb-4">
      <h2 className="text-2xl font-bold mb-4">Categories</h2>
      {categories.map((category) => (
        <div key={category.id} className="mb-8">
          <h3 className="text-xl font-bold mb-2">{category.id}</h3>
          <ItemsList category={category.id} username={username} />
        </div>
      ))}
    </div>
  );
};

const ItemsList = ({ category, username }) => {
  const [items, setItems] = useState([]);

  useEffect(() => {
    const fetchItems = async () => {
      const itemsRef = collection(db, 'screenshots', username, 'categories', category, 'items');
      const q = query(itemsRef);

      console.log('Fetching items for category:', category);
      console.log('Items collection ref:', itemsRef);
      console.log('Items query:', q);

      const querySnapshot = await getDocs(q);
      const itemsData = querySnapshot.docs.map((doc) => ({
        id: doc.id,
        ...doc.data(),
      }));

      console.log('Items data:', itemsData);
      setItems(itemsData);
    };

    fetchItems();
  }, [category, username]);

  console.log('Rendering items for category:', category, items);

  return (
    <ul className="list-disc pl-6">
      {items.map((item) => (
        <li key={item.id} className="mb-2">
          <strong>{item.id}</strong>
          <p>Location: {item.location}</p>
          <p>Description: {item.description}</p>
        </li>
      ))}
    </ul>
  );
};

export default CategoriesList;