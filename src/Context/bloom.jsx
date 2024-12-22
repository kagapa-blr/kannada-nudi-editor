import React, { createContext, useContext, useEffect, useState } from 'react';
import BloomFilter from 'bloom-filter-new';

// Create the context for the Bloom Filter
const BloomFilterContext = createContext();

// Custom hook to use Bloom Filter Context
export const useBloomFilter = () => {
  return useContext(BloomFilterContext);
};

// Bloom Filter Provider Component
export const BloomFilterProvider = ({ children }) => {
  const [bloomFilter, setBloomFilter] = useState(null); // State to store BloomFilter
  const [loading, setLoading] = useState(true); // State to handle loading state
  const [error, setError] = useState(null); // State to handle errors

  // Load Bloom Filter from file
  useEffect(() => {
    const loadBloomFilter = async () => {
      try {
        const filePath = 'assets/collection.txt'; // Ensure the file path is correct
        const filter = await BloomFilter.fromFile(filePath, 100000, 0.001); // Set size and error rate
        setBloomFilter(filter); // Set the BloomFilter in state
        setLoading(false); // Set loading to false once done
      } catch (error) {
        console.error('Error loading Bloom Filter:', error);
        setError('Failed to load Bloom Filter.');
        setLoading(false); // Stop loading in case of error
      }
    };

    loadBloomFilter(); // Load the filter when the component mounts
  }, []);

  // Provide the context value to children components
  return (
    <BloomFilterContext.Provider value={{ bloomFilter, loading, error }}>
      {children}
    </BloomFilterContext.Provider>
  );
};
