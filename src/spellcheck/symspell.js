class SymSpell {
    static Modes = {
        TOP: 0,
        SMALLEST: 2,
        ALL: 10
    };

    constructor(maxEditDistance = 2, mode = SymSpell.Modes.ALL) {
        this.maxEditDistance = maxEditDistance;
        this.mode = mode;
        this.dictionary = {};
    }

    // Adds words to the dictionary from a corpus or from CSV
    addWords(corpus, tokenizer = this.tokenize) {
        const words = tokenizer(corpus);
        words.forEach(word => this.addWord(word));
    }

    // Loads words from a CSV file and adds them to the dictionary using fetch
    async loadFromCSV(filePath) {
        try {
            const response = await fetch(filePath); // Fetch CSV file
            const data = await response.text(); // Get the file's text content
            const words = data.split('\n'); // Split the file into lines (words)

            words.forEach(word => {
                const trimmedWord = word.trim(); // Remove any surrounding spaces or newline characters
                if (trimmedWord) {
                    this.addWordWithFrequency(trimmedWord, 1); // Default frequency is 1
                }
            });

            console.log('CSV file successfully loaded.');
        } catch (error) {
            console.error('Error loading CSV file:', error);
        }
    }

    // Adds a word to the dictionary with an optional frequency
    addWordWithFrequency(word, frequency = 1) {
        let item = this.dictionary[word];

        if (!item) {
            item = new DictionaryItem();
            item.term = word;
            item.count = frequency;
            this.dictionary[word] = item;
        } else {
            item.count += frequency; // Increment frequency if the word already exists
        }

        // You can add more logic here if needed (like computing permutations, etc.)
    }

    // Suggests corrections for a word and returns all matching suggestions
    getSuggestions(word) {
        return this.lookup(word);
    }

    // Suggests corrections for a word
    lookup(word) {
        let candidates = [new EditItem(word, 0)];
        let suggestions = [];

        const sort = () => {
            suggestions = suggestions.sort((a, b) => {
                const distanceDiff = a.distance - b.distance;
                return distanceDiff ? distanceDiff : b.count - a.count;
            }).filter(a => a.term);

            return this.mode === SymSpell.Modes.TOP && suggestions.length > 1 ? [suggestions[0]] : suggestions;
        };

        while (candidates.length > 0) {
            const candidate = candidates.shift();
            if (
                (this.mode !== SymSpell.Modes.ALL && suggestions.length && candidate.distance > suggestions[0].distance) ||
                candidate.distance > this.maxEditDistance
            ) {
                return sort();
            }

            const key = candidate.term;
            if (this.dictionary[key]) {
                const si = new SuggestItem(this.dictionary[key].term, this.dictionary[key].count, candidate.distance);
                if (!this.wordListContains(suggestions, si)) {
                    suggestions.push(si);
                    if (this.mode !== SymSpell.Modes.ALL && !candidate.distance) return sort();
                }

                this.dictionary[key].suggestions.forEach(suggestion => {
                    if (!this.wordListContains(suggestions, suggestion)) {
                        const distance = this.realEditDistance(suggestion, candidate, word);
                        if (this.mode !== SymSpell.Modes.ALL && suggestions.length) {
                            if (suggestions[0].distance > distance) {
                                suggestions.length = 0;
                            } else if (distance > suggestions[0].distance) {
                                return;
                            }
                        }
                        if (distance < this.maxEditDistance && this.dictionary[suggestion.term]) {
                            const di = this.dictionary[suggestion.term];
                            const sim = new SuggestItem(di.term, di.count, distance);
                            suggestions.push(sim);
                        }
                    }
                });
            }

            if (candidate.distance < this.maxEditDistance) {
                const perms = this.computePermutations(candidate.term, candidate.distance, 0);
                perms.forEach(perm => {
                    if (!this.wordListContains(candidates, perm)) {
                        candidates.push(perm);
                    }
                });
            }
        }

        return sort();
    }

    // Helper function to tokenize input
    tokenize(corpus) {
        return corpus.toLowerCase().match(/([\w\d_](-[\w\d_])?('(t|d|s|m|ll|re|ve))?)+/g);
    }

    // Computes variations of a word by deleting characters
    computePermutations(word, editDistance = 0, maxEditDistance) {
        editDistance += 1;
        const permutations = [];
        const len = word.length;

        if (len > 1) {
            for (let i = 0; i < len; i++) {
                const p = new EditItem(word.slice(0, i) + word.slice(i + 1), editDistance);
                if (!permutations.includes(p)) {
                    permutations.push(p);
                    if (maxEditDistance && editDistance < maxEditDistance) {
                        const nextPermutations = this.computePermutations(p.term, editDistance, maxEditDistance);
                        nextPermutations.forEach(perm => {
                            if (!permutations.includes(perm)) {
                                permutations.push(perm);
                            }
                        });
                    }
                }
            }
        }
        return permutations;
    }

    // Checks if a list of items contains a given item value
    wordListContains(list, value) {
        return list.some(item => item.equals(value));
    }

    // Adds or terminates early if necessary based on the mode
    addOrTerminateEarly(suggestions, suggestion) {
        if (this.mode !== SymSpell.Modes.ALL && suggestions.length && suggestions[0].distance > suggestion.distance) {
            suggestions.length = 0;
        }
        if (this.mode === SymSpell.Modes.ALL || !suggestions.length || suggestions[0].distance >= suggestion.distance) {
            suggestions.push(suggestion);
        }
    }

    // Real edit distance calculation
    realEditDistance(dictItem, inputPermutation, input) {
        if (dictItem.term === input) return 0;
        if (!dictItem.distance) return inputPermutation.distance;
        if (!inputPermutation.distance) return dictItem.distance;
        return this.distance(dictItem.term, input);
    }

    // Damerau-Levenshtein distance calculation
    distance(source, target) {
        if (!source) return target ? target.length : 0;
        if (!target) return source.length;

        const m = source.length, n = target.length;
        const INF = m + n;
        const score = Array.from({ length: m + 2 }, () => Array(n + 2).fill(INF));
        const sd = {};

        score[0][0] = INF;
        for (let i = 0; i <= m; i++) score[i + 1][1] = i;
        for (let j = 0; j <= n; j++) score[1][j + 1] = j;

        for (let i = 1; i <= m; i++) {
            let DB = 0;
            for (let j = 1; j <= n; j++) {
                const i1 = sd[target[j - 1]], j1 = DB;
                if (source[i - 1] === target[j - 1]) {
                    score[i + 1][j + 1] = score[i][j];
                    DB = j;
                } else {
                    score[i + 1][j + 1] = Math.min(score[i][j], Math.min(score[i + 1][j], score[i][j + 1])) + 1;
                }
                score[i + 1][j + 1] = Math.min(score[i + 1][j + 1], score[i1] ? score[i1][j1] + (i - i1 - 1) + 1 + (j - j1 - 1) : Infinity);
            }
            sd[source[i - 1]] = i;
        }
        return score[m + 1][n + 1];
    }
}

// Helper classes
class Word {
    constructor(term = '') {
        this.term = term;
    }

    equals(obj) {
        return obj && obj.term === this.term;
    }
}

class DictionaryItem extends Word {
    constructor() {
        super();
        this.suggestions = [];
        this.count = 0;
    }
}

class EditItem extends Word {
    constructor(term = '', distance = 0) {
        super(term);
        this.distance = distance;
    }
}

class SuggestItem extends Word {
    constructor(term = '', count = 0, distance = 0) {
        super(term);
        this.count = count;
        this.distance = distance;
    }
}

export default SymSpell;
