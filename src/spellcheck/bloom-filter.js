const fs = require('fs').promises; // Use fs.promises for async/await with file system
const { BloomFilter } = require('bloomfilter'); // Destructure import for better clarity

export class WordBloomFilter {
  constructor(filename, size = 10000, falsePositiveRate = 0.01) {
    this.filename = filename;
    this.filter = new BloomFilter(size, falsePositiveRate);
    this.loadFilter();
  }

  // Load words from file and populate the Bloom filter
  async loadFilter() {
    try {
      const words = await this.readWordsFromFile(this.filename);
      words.forEach(word => {
        this.filter.add(word); // Add word to the Bloom filter
      });
      console.log('Bloom filter populated.');
    } catch (err) {
      console.error('Error loading filter:', err);
    }
  }

  // Read words from the .txt file
  async readWordsFromFile(filename) {
    try {
      const data = await fs.readFile(filename, 'utf8');
      return data.split(/\r?\n/).map(word => word.trim()).filter(word => word.length > 0);
    } catch (err) {
      throw new Error(`Failed to read file: ${err.message}`);
    }
  }

  // Check if a word exists in the Bloom filter
  isWordFound(word) {
    return this.filter.test(word);
  }
}

