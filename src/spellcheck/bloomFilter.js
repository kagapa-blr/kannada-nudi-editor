export default class BloomFilter {
    /**
     * Create a Bloom Filter.
     * @param {number} expectedItems - The expected number of items to store.
     * @param {number} falsePositiveRate - The desired false positive rate (e.g., 0.01 for 1%).
     */
    constructor(expectedItems = 1000, falsePositiveRate = 0.01) {
        this.expectedItems = expectedItems;
        this.falsePositiveRate = falsePositiveRate;
        this.size = this.calculateOptimalSize(expectedItems, falsePositiveRate);
        this.bitArray = new Array(this.size).fill(0);
        this.hashCount = this.calculateOptimalHashCount(expectedItems);
        this.itemsAdded = 0; // To track the number of added items
        console.log(`Bit array size: ${this.size}, Hash functions: ${this.hashCount}`);
    }

    /**
     * Calculate the optimal bit array size.
     * Formula: m = -(n * log(p)) / (log(2)^2)
     * @param {number} expectedItems
     * @param {number} falsePositiveRate
     * @returns {number}
     */
    calculateOptimalSize(expectedItems, falsePositiveRate) {
        return Math.ceil(-(expectedItems * Math.log(falsePositiveRate)) / (Math.log(2) ** 2));
    }

    /**
     * Calculate the optimal number of hash functions.
     * Formula: k = (m / n) * log(2)
     * @param {number} expectedItems
     * @returns {number}
     */
    calculateOptimalHashCount(expectedItems) {
        return Math.ceil((this.size / expectedItems) * Math.log(2));
    }

    /**
     * Generate a hash value based on the seed, compatible with UTF-8 characters.
     * @param {string} value - The input value to hash.
     * @param {number} seed - The seed to generate different hashes.
     * @returns {number}
     */
    hash(value, seed) {
        let hash = 5381 + seed; // Initial prime number for djb2, varied by seed
        for (let i = 0; i < value.length; i++) {
            hash = (hash * 33 + value.charCodeAt(i)) % this.size;
        }
        return Math.abs(hash); // Ensure the hash index is positive
    }

    /**
     * Add an element to the Bloom Filter.
     * @param {string} value - The value to add.
     */
    add(value) {
        for (let i = 0; i < this.hashCount; i++) {
            const hash = this.hash(value, i + 1);
            this.bitArray[hash] = 1;
        }
        this.itemsAdded += 1;
    }

    /**
     * Check if an element might be in the Bloom Filter.
     * @param {string} value - The value to check.
     * @returns {boolean} - Returns true if the value might be present, otherwise false.
     */
    contains(value) {
        for (let i = 0; i < this.hashCount; i++) {
            const hash = this.hash(value, i + 1);
            if (this.bitArray[hash] !== 1) {
                return false; // Definitely not in the set
            }
        }
        return true; // Possibly in the set
    }

    /**
     * Load words from a .txt file and add them to the Bloom Filter.
     * @param {string} filePath - Path to the .txt file.
     */
    async loadFromFile(filePath) {
        try {
            const response = await fetch(filePath);
            if (!response.ok) {
                throw new Error(`Failed to fetch file: ${response.statusText}`);
            }

            const text = await response.text();
            const words = text
                .split(/\r?\n/)                // Split on newlines (handles Windows and Unix formats)
                .map(word => word.trim())      // Trim each word
                .filter(word => word.length > 0); // Filter out empty lines

            words.forEach(word => this.add(word));
            console.log(`${words.length} words added to the Bloom Filter.`);
        } catch (error) {
            console.error(`Error loading file: ${error.message}`);
        }
    }

    /**
     * Get detailed information about the Bloom Filter.
     * @returns {object} - An object containing details about the Bloom Filter.
     */
    getInfo() {
        const filledBits = this.bitArray.filter(bit => bit === 1).length;
        const fillPercentage = ((filledBits / this.size) * 100).toFixed(2);

        return {
            expectedItems: this.expectedItems,
            itemsAdded: this.itemsAdded,
            size: this.size,
            hashCount: this.hashCount,
            falsePositiveRate: this.falsePositiveRate,
            filledBits: filledBits,
            fillPercentage: `${fillPercentage}%`,
        };
    }

    /**
     * Static method to create and load a Bloom Filter from a file.
     * @param {string} filePath - Path to the .txt file.
     * @param {number} expectedItems - Expected number of items in the file.
     * @param {number} falsePositiveRate - Desired false positive rate.
     * @returns {Promise<BloomFilter>} - A Promise resolving to a loaded Bloom Filter.
     */
    static async fromFile(filePath, expectedItems = 1000, falsePositiveRate = 0.01) {
        const bloomFilter = new BloomFilter(expectedItems, falsePositiveRate);
        await bloomFilter.loadFromFile(filePath);
        return bloomFilter;
    }
}
