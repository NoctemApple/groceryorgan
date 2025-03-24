// src/App.js
import React, { useState, useEffect } from 'react';
import './App.css';

function App() {
  // State for storing grocery list data
  const [groceryList, setGroceryList] = useState([]);

  // Fetch the grocery list from the Django API when the component mounts
  useEffect(() => {
    // In development, you can set a proxy in package.json to avoid CORS issues:
    // "proxy": "http://localhost:8000"
    fetch('/api/grocery-list/')
      .then(response => {
        if (!response.ok) {
          throw new Error('Network response was not OK');
        }
        return response.json();
      })
      .then(data => {
        setGroceryList(data);
      })
      .catch(error => {
        console.error('Error fetching grocery list:', error);
      });
  }, []);

  return (
    <div className="App">
      <header className="App-header">
        <h1>Your Grocery List</h1>
      </header>
      <main>
        <ul>
          {groceryList.map((item, index) => (
            <li key={index}>
              {item.name} – Group {item.category + 1}
            </li>
          ))}
        </ul>
      </main>
    </div>
  );
}

export default App;
