import { useState, useRef, useEffect } from "react";
import ReactQuill from "react-quill-new";
import "react-quill-new/dist/quill.snow.css";
import Page from "./Page";
import EditorToolbar from "./toolbar/QuillToolbar";
import { formats } from "../constants/formats";
import { modules } from "../constants/editorModules";
import {
  getWordAtPosition,
  underlineWordInEditor,
  cleanWord,
} from "../services/editorService";
import Tooltip from "../components/editor/Tooltip";
import { loadBloomFilter } from "../spellcheck/bloomFilter";

import LoadingComponent from "./utils/LoadingComponent";
import { ignoreSingleChars, isSingleCharacter } from "../services/editorUtils";
import SymSpellService from "../spellcheck/symspell";
import { getWrongWords } from "../spellcheck/bloomFilter";

const QuillEditor = () => {
  const [content, setContent] = useState("");
  const [pages, setPages] = useState([0]);
  const [pageSize, setPageSize] = useState({ width: 816, height: 1056 }); // Default A4 size
  const quillRef = useRef(null);
  const [mouseDown, setMouseDown] = useState(false); // Track if mouse is down

  const [wrongwords, setWrongWords] = useState([]);
  const [suggestions, setSuggestions] = useState({});
  const [clickedWord, setClickedWord] = useState(null);
  const [tooltipPosition, setTooltipPosition] = useState({});
  const [replacementWord, setReplacementWord] = useState("");
  const [isModalOpen, setIsModalOpen] = useState(false);
  const [isLoading, setIsLoading] = useState(false);
  const [bloomFilter, setBloomFilter] = useState(null); // State to store BloomFilter
  const [currentFilePath, setCurrentFilePath] = useState("");

  const specialChars = "!@#$%^&*()_+[]{}|;:',.<>/?~-=\\\"";
  const [symSpell, setSymSpell] = useState(null);
  const dictionaryPath = "dist/assets/collection.txt";
  const word_frequency_path = "./assets/word_frequency.txt";

  // Open file handler
  const openFile = async () => {
    const filePath = await window.electron.openFile();
    if (filePath) {
      setCurrentFilePath(filePath);
      const content = await window.electron.readFile(filePath);
      // You can use this content to populate your editor or UI
    }
  };

  // Save file handler
  const saveFile = async () => {
    if (currentFilePath) {
      await window.electron.saveFile(currentFilePath, content);
      alert("File saved successfully!");
    } else {
      const filePath = await window.electron.saveFileAs(content);
      if (filePath) {
        setCurrentFilePath(filePath);
        alert("File saved successfully!");
      }
    }
  };

  // Append file handler (takes file path and content to append)
  const appendToFile = async (filePath, contentToAppend) => {
    console.log("filepaht: ", filePath, "contentToAppend: ", contentToAppend);
    if (filePath && contentToAppend) {
      const success = await window.electron.appendContent(
        filePath,
        contentToAppend+"\n"
      );
      if (success) {
        alert("Content appended successfully!");
      } else {
        alert("Failed to append content.");
      }
    } else {
      alert("Please provide both the file path and content to append.");
    }
  };

  // Load Bloom Filter on mount
  useEffect(() => {
    const size = 100000; // Define the size of the Bloom Filter
    const errorRate = 0.001; // Define the error rate

    console.log(`Starting to load Bloom Filter from: ${dictionaryPath}`);
    console.log(
      `Expected Bloom Filter size: ${size}, Error rate: ${errorRate}`
    );

    loadBloomFilter(dictionaryPath, size, errorRate)
      .then((filter) => {
        console.log("Bloom Filter loaded successfully.");
        setBloomFilter(filter); // Set the BloomFilter in state
      })
      .catch((err) => {
        console.error("Failed to load Bloom Filter. Error details:", err);
        // Optionally handle error state updates here if required
      });
  }, []);

  useEffect(() => {
    const loadSymSpell = async () => {
      const symSpellService = new SymSpellService();
      try {
        await symSpellService.loadSymSpell(
          symSpellService,
          word_frequency_path
        );
        setSymSpell(symSpellService);
        console.log("Successfully loaded symSpellService");
      } catch (error) {
        console.error("Error loading dictionary:", error);
      }
    };

    loadSymSpell();
  }, []);

  const handleCheckWord = (word) => {
    if (bloomFilter) {
      const isContained = bloomFilter.contains(word);
      console.log(
        isContained
          ? `${word} is in the filter`
          : `${word} is NOT in the filter`
      );
      //const quill = quillRef.current?.getEditor();
      //console.log("suggestions: ", symSpell.lookup(word, maxEditDistance));
      //underlineWordInEditor(quill, word);
    }
  };
  useEffect(() => {
    paginateContent();
  }, [content, pageSize]);

  useEffect(() => {
    if (quillRef.current) {
      quillRef.current.getEditor().root.setAttribute("spellcheck", "false");
    }
  }, []);

  const handleChange = (value) => {
    setContent(value);
  };

  const paginateContent = () => {
    const editor = quillRef?.current?.getEditor();
    const editorContent = editor.root;
    const contentHeight = editorContent.scrollHeight;
    const requiredPages = Math.ceil(contentHeight / pageSize.height);

    setPages(Array.from({ length: requiredPages }, (_, i) => i));
  };

  useEffect(() => {
    const fetchWrongWords = async () => {
      const quill = quillRef.current?.getEditor();
      if (quill && bloomFilter) {
        try {
          const wrongWordList = await getWrongWords(quill, bloomFilter);
          //console.log("wrongwords", wrongWordList);
          if (wrongWordList) {
            const removedSinglechar = ignoreSingleChars(wrongWordList);
            // Underline new errors in the editor
            removedSinglechar.forEach((word) =>
              underlineWordInEditor(quill, word)
            );
            // Update the errors state
            setWrongWords(removedSinglechar);
          }
        } catch (error) {
          console.error("Error fetching wrong words:", error);
        }
      }
    };

    fetchWrongWords();
  }, [content]); // Add dependencies as needed

  useEffect(() => {
    const quill = quillRef.current?.getEditor();

    const handleMouseDown = () => {
      setMouseDown(true); // Mouse is down
    };

    const handleMouseUp = () => {
      setMouseDown(false); // Mouse is up
    };

    const handleSelectionChange = async (range, source) => {
      // Only execute if mouse was clicked
      if (mouseDown && range && range.length === 0) {
        const fullText = quill.getText();
        const word = cleanWord(getWordAtPosition(fullText, range.index));

        if (word) {
          if (wrongwords.includes(word)) {
            try {
              const suggestionList = await symSpell.getSuggestions(word);
              setClickedWord(word);
              // Assuming the suggestionList is an array of suggestion objects
              setSuggestions((prevSuggestions) => ({
                ...prevSuggestions,
                [word]: suggestionList.map((suggestion) => suggestion.term), // Extracting only the 'term' from each suggestion
              }));

              const bounds = quill.getBounds(range.index);
              setTooltipPosition({
                top: bounds.bottom + 90,
                left: bounds.left,
              });
            } catch (error) {
              console.error("Error fetching suggestions:", error);
            }
          } else {
            setClickedWord(null);
          }
        }
      }
    };

    // Attach event listeners for mouse events
    document.addEventListener("mousedown", handleMouseDown);
    document.addEventListener("mouseup", handleMouseUp);

    quill.on("selection-change", handleSelectionChange);

    // Cleanup listeners on component unmount
    return () => {
      document.removeEventListener("mousedown", handleMouseDown);
      document.removeEventListener("mouseup", handleMouseUp);
      quill.off("selection-change", handleSelectionChange);
    };
  }, [wrongwords, mouseDown]);

  const handleKeyDown = async (e) => {
    if (e.key === " ") {
      // Debounce logic
      clearTimeout(window.debounceTimer);
      window.debounceTimer = setTimeout(async () => {
        const quill = quillRef.current.getEditor();
        const range = quill.getSelection();

        if (range) {
          const currentText = quill.getText(0, range.index).trim();
          const words = currentText.split(/\s+/);
          let lastWord = words[words.length - 1]
            .split("")
            .filter((char) => !specialChars.includes(char))
            .join("");
          if (isSingleCharacter(lastWord)) return;

          if (wrongwords.includes(cleanWord(lastWord))) {
            underlineWordInEditor(quill, lastWord);
          } else if (lastWord && !/^[a-zA-Z0-9]+$/.test(lastWord)) {
            const isContained = await bloomFilter.contains(lastWord); //returns true or false

            //if flase then underline
            if (!isContained) {
              setWrongWords((prevErrors) => [...prevErrors, lastWord]);
              const quill = quillRef.current?.getEditor();
              underlineWordInEditor(quill, lastWord);
            }
          }
        }
      }, 300); // Adjust the debounce time as needed
    }
  };

  const replaceWord = (replacement) => {
    const quill = quillRef.current.getEditor();
    const text = quill.getText();
    const clickedWordLength = clickedWord.length;

    // Create a regex pattern that matches the clickedWord surrounded by optional special characters
    const regex = new RegExp(`(\\W|^)(${clickedWord})(\\W|$)`, "g");

    let match;
    const positions = [];

    // Find all occurrences and store their positions
    while ((match = regex.exec(text)) !== null) {
      const startIndex = match.index + match[1].length; // Start of the clickedWord (after any special character)
      const length = clickedWordLength; // Length of the clickedWord

      // Store the position for replacement
      positions.push({ startIndex, length });
    }

    // Replace all occurrences in reverse order to prevent index shifting
    for (let i = positions.length - 1; i >= 0; i--) {
      const { startIndex, length } = positions[i];

      // Remove the original word
      quill.deleteText(startIndex, length);
      // Insert the replacement word
      quill.insertText(startIndex, replacement);
    }

    // Update errors and clickedWord state
    setWrongWords(wrongwords.filter((word) => word !== clickedWord));
    setClickedWord(null);
  };

  const addDictionary = async () => {
    if (clickedWord) {
      try {
        // const response = true; //= await addWordToDictionary(cleanWord(clickedWord));
        // if (response) {
        //   const quill = quillRef.current.getEditor();
        //   const fullText = quill.getText();
        //   let index = fullText.indexOf(clickedWord);

        //   if (index !== -1) {
        //     while (index !== -1) {
        //       // Remove underline and reset color
        //       quill.formatText(index, clickedWord.length, {
        //         underline: false,
        //         color: "",
        //       });
        //       index = fullText.indexOf(clickedWord, index + clickedWord.length);
        //     }
        //   }

        //   setWrongWords(wrongwords.filter((word) => word !== clickedWord));
        //   setClickedWord(null);
        //   console.log(response);
        // } else {
        //   console.error("Failed to add the word to the dictionary.");
        // }
        console.log("add to dictionary called", clickedWord);
        appendToFile(dictionaryPath, clickedWord);
      } catch (error) {
        console.error("Error adding word to dictionary:", error);
      }
    }
  };

  const replaceAll = () => {
    if (clickedWord) {
      // console.log("replace all called");
      setIsModalOpen(true);
    }
  };

  const handleReplaceAll = () => {
    const editor = quillRef.current.getEditor();
    const fullText = editor.getText();
    const clickedWordLength = clickedWord.length;

    // Create a regex pattern that matches the clickedWord surrounded by optional special characters
    const regex = new RegExp(`(\\W|^)(${clickedWord})(\\W|$)`, "g");

    // Store replacements to avoid altering indices during the loop
    let match;
    const replacements = []; // Array to store replacements

    // Find all matches
    while ((match = regex.exec(fullText)) !== null) {
      const startIndex = match.index + match[1].length; // Start of the clickedWord (after any special character)

      // Push the index and replacementWord into the array
      replacements.push({
        startIndex,
        word: replacementWord,
        clickedWordLength, // Length of the clickedWord to delete later
      });
    }

    // Replace matches in reverse order to avoid index shifting
    replacements
      .reverse()
      .forEach(({ startIndex, word, clickedWordLength }) => {
        editor.deleteText(startIndex, clickedWordLength); // Remove the clickedWord
        editor.insertText(startIndex, word); // Insert the replacementWord without formats
      });

    // Reset modal and state
    setIsModalOpen(false);
    setClickedWord(null);
    setReplacementWord("");
  };

  const ignoreAll = () => {
    const quill = quillRef.current?.getEditor();
    const fullText = quill.getText();
    let index = fullText.indexOf(clickedWord);

    if (index !== -1) {
      while (index !== -1) {
        quill.formatText(index, clickedWord.length, {
          underline: false,
          color: "",
        });
        index = fullText.indexOf(clickedWord, index + clickedWord.length);
      }
    }

    setClickedWord(null);
    setWrongWords(wrongwords.filter((word) => word !== clickedWord));
  };

  const handleRefresh = async () => {
    console.log("Refresh called");
    setIsLoading(true);
    const quill = quillRef.current?.getEditor();

    // Clear previous errors before refreshing
    setWrongWords([]);

    // Fetch new wrong words (spellcheck the content again)
    const wrongWordList = await refreshWords(quill);
    if (wrongWordList) {
      const removedSinglechar = ignoreSingleChars(wrongWordList);

      // Underline new errors in the editor
      removedSinglechar.forEach((word) => underlineWordInEditor(quill, word));

      // Update the errors state
      setWrongWords(removedSinglechar);
    }

    setIsLoading(false);
  };

  const handleInputClick = (e) => {
    e.target.focus(); // Focus the input when clicked
  };

  return (
    <div className="editor-container">
      <div className="editor-toolbar-container">
        <EditorToolbar quillRef={quillRef} setPageSize={setPageSize} />
      </div>
      <div className="editor-wrapper">
        <div className="relative">
          {pages.map((pageIndex, idx) => (
            <Page
              key={pageIndex}
              pageIndex={pageIndex}
              isLast={idx === pages.length - 1}
              pageSize={pageSize}
            />
          ))}
        </div>
        <ReactQuill
          ref={quillRef}
          theme="snow"
          value={content}
          onChange={handleChange}
          onKeyDown={handleKeyDown}
          modules={modules}
          formats={formats}
          style={{
            width: `${pageSize.width}px`,
            minHeight: `${pageSize.height}px`,
          }}
          className="quill-editor"
        />
      </div>

      {isModalOpen && (
        <div className="fixed inset-0 flex items-center justify-center z-50">
          <div className="bg-white border border-gray-300 p-4 rounded shadow-lg w-11/12 max-w-sm mx-auto">
            <h5 className="mb-2">Replace {clickedWord} with:</h5>
            <input
              type="text"
              autoFocus
              value={replacementWord}
              onChange={(e) => setReplacementWord(e.target.value)}
              onClick={handleInputClick}
              className="border border-gray-300 p-2 rounded w-full"
              placeholder="Replacement word"
            />
            <div className="mt-4 flex justify-end">
              <button
                onClick={handleReplaceAll}
                className={`bg-blue-500 text-white px-4 py-2 rounded mr-2 ${
                  !replacementWord.trim() ? "opacity-50 cursor-not-allowed" : ""
                }`}
                disabled={!replacementWord.trim()}
              >
                Replace All
              </button>
              <button
                onClick={() => setIsModalOpen(false)}
                className="bg-gray-300 px-4 py-2 rounded"
              >
                Cancel
              </button>
            </div>
          </div>
        </div>
      )}

      {clickedWord && suggestions[clickedWord] && (
        <Tooltip
          clickedWord={clickedWord}
          suggestions={suggestions}
          tooltipPosition={tooltipPosition}
          setClickedWord={setClickedWord}
          replaceWord={replaceWord}
          addDictionary={addDictionary}
          replaceAll={replaceAll}
          ignoreAll={ignoreAll}
        />
      )}

      {isLoading && <LoadingComponent />}
    </div>
  );
};

export default QuillEditor;
