import BloomFilter from 'bloom-filter-new';

const specialChars = "೧^l=F–೬B#yJwfz•+2umE<'!CxULvr]8o೦VNd0hH‘_>)- :sYQ7.g9n%W,G`1…\"&?6೯I”೮೨Tb“@೭೫ʼKX4೪[iDScM;*t’{5k/pa(PAeZ~O3R|j}q೩$";
// Escape special characters for regex
const escapedSpecialChars = specialChars.replace(/[-[\]{}()*+?.,\\^$|#\s]/g, '\\$&');
const specialCharsRegex = new RegExp(`[${escapedSpecialChars}]`, 'g');


export const getWrongWords = async (quill, bloomFilter) => {
    const fullText = quill.getText();


    // Split the text into words and clean them
    const words = fullText
        .split(/\s+/) // Split by spaces
        .filter(word => word.length > 0) // Remove empty strings
        .map(word => word.replace(specialCharsRegex, '').trim()) // Clean special characters
        .filter(word => word.length > 0); // Remove any remaining empty strings after cleaning

    // Get unique words
    const uniqueWords = [...new Set(words)];

    const wrongWords = [];

    try {
        for (const word of uniqueWords) {
            const isContained = await bloomFilter.contains(word);
            if (!isContained) {
                wrongWords.push(word);
            }
        }

        return wrongWords; // Return the list of wrong words
    } catch (error) {
        console.error('Error checking word correctness:', error);
        return []; // Return an empty list on error
    }
};


export const loadBloomFilter = async (filePath, size, errorRate) => {
  try {
    const filter = await BloomFilter.fromFile(filePath, size, errorRate); // Create BloomFilter from file
    return filter;
  } catch (error) {
    console.error('Error loading Bloom Filter:', error);
    throw error; // Re-throw error for the calling function to handle
  }
};
