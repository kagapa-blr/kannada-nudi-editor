import React, { useState, useRef, useEffect } from "react";
import ReactQuill from "react-quill-new";
import "react-quill-new/dist/quill.snow.css"; // Quill CSS
import LoadingComponent from "../utils/LoadingComponent";
import EditorButtons from "../editor/EditorButtons";
import { ignoreSingleChars, isSingleCharacter } from "../../utils/editorUtils";
import {
  checkWord,
  getSuggestions,
  addWordToDictionary,
  refreshWords,
} from "../../services/spellcheckApiService";
import { addWordToCache, getSuggestionsFromCache } from "../../utils/cache"; // Adjust the path as needed
import { useLocation } from "react-router-dom";

import { useWrongWords } from "../../context/WrongWordsContext";
import { editorModules } from "../../services/editorMaterialService";
import {
  getWordAtPosition,
  underlineWordInEditor,
  cleanWord,
} from "../../services/editorService";

import Tooltip from "../editor/ToolTip";

const SpellCheckEditor = () => {
  const location = useLocation();
  const uploadedContent = location.state?.uploadedContent || ""; // Get uploaded content

  const [text, setText] = useState(""); // Set initial text
  const [errors, setErrors] = useState([]);
  const [suggestions, setSuggestions] = useState({});
  const [clickedWord, setClickedWord] = useState(null);
  const [tooltipPosition, setTooltipPosition] = useState({});
  const [replacementWord, setReplacementWord] = useState("");
  const [isModalOpen, setIsModalOpen] = useState(false);
  const [isLoading, setIsLoading] = useState(false);
  const [mouseDown, setMouseDown] = useState(false); // Track if mouse is down
  const quillRef = useRef(null);
  const specialChars = "!@#$%^&*()_+[]{}|;:',.<>/?~-=\\\"";
  // Access the wrong words from the WrongWordsContext
  const { wrongWords, setWrongWords } = useWrongWords();

  useEffect(() => {
    if (quillRef.current) {
      quillRef.current.getEditor().root.setAttribute("spellcheck", "false");
    }
  }, []);

  useEffect(() => {
    if (uploadedContent.length == 0) {
      setWrongWords([]);
      return;
    }
    // Set text if uploadedContent exists
    if (uploadedContent) {
      console.log("updating content into editor ....");
      setText(uploadedContent);
    }

    // Exit if wrongWords is null or empty
    if (!wrongWords || wrongWords.length === 0) return;
    setErrors([]);
    console.log("Wrong Words Updated:", wrongWords.length);
    console.log("Errors Updated:", errors.length);
    setIsLoading(true);

    const timeoutId = setTimeout(() => {
      const quill = quillRef.current?.getEditor();
      // Underline new errors in the editor
      console.log("Underlining the wrong words");
      wrongWords.forEach((word) => underlineWordInEditor(quill, word));
      setIsLoading(false);
    }, 3000);

    // Cleanup function to clear the timeout if the component unmounts or dependencies change
    return () => clearTimeout(timeoutId);
  }, [uploadedContent]);

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
          if (errors.includes(word) || wrongWords.includes(word)) {
            let suggestionList = getSuggestionsFromCache(word);

            if (suggestionList.length === 0) {
              try {
                suggestionList = await getSuggestions(word);
                addWordToCache(word, false, suggestionList);
              } catch (error) {
                console.error("Error fetching suggestions:", error);
              }
            }

            setClickedWord(word);
            setSuggestions((prevSuggestions) => ({
              ...prevSuggestions,
              [word]: suggestionList,
            }));

            const bounds = quill.getBounds(range.index);
            setTooltipPosition({
              top: bounds.bottom + 90,
              left: bounds.left,
            });
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
  }, [errors, mouseDown]);

  const handleInputChange = (value) => {
    setText(value);
  };

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

          if (errors.includes(cleanWord(lastWord))) {
            underlineWordInEditor(quill, lastWord);
          } else if (lastWord && !/^[a-zA-Z0-9]+$/.test(lastWord)) {
            const response = await checkWord(lastWord);
            if (!response.status) {
              setErrors((prevErrors) => [...prevErrors, lastWord]);
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
    setErrors(errors.filter((word) => word !== clickedWord));
    setClickedWord(null);
  };

  const addDictionary = async () => {
    if (clickedWord) {
      try {
        const response = await addWordToDictionary(cleanWord(clickedWord));
        if (response) {
          const quill = quillRef.current.getEditor();
          const fullText = quill.getText();
          let index = fullText.indexOf(clickedWord);

          if (index !== -1) {
            while (index !== -1) {
              // Remove underline and reset color
              quill.formatText(index, clickedWord.length, {
                underline: false,
                color: "",
              });
              index = fullText.indexOf(clickedWord, index + clickedWord.length);
            }
          }

          setWrongWords((prevWrongWords) =>
            prevWrongWords.filter((word) => word !== clickedWord)
          );
          setErrors(errors.filter((word) => word !== clickedWord));
          setClickedWord(null);
          console.log(response);
        } else {
          console.error("Failed to add the word to the dictionary.");
        }
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

    setWrongWords((prevWrongWords) =>
      prevWrongWords.filter((word) => word !== clickedWord)
    );
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
    setErrors(errors.filter((word) => word !== clickedWord));
    setWrongWords((prevWrongWords) =>
      prevWrongWords.filter((word) => word !== clickedWord)
    );
  };

  const handleRefresh = async () => {
    console.log("Refresh called");
    setIsLoading(true);
    const quill = quillRef.current?.getEditor();

    // Clear previous errors before refreshing
    setErrors([]);

    // Fetch new wrong words (spellcheck the content again)
    const wrongWordList = await refreshWords(quill);
    if (wrongWordList) {
      const removedSinglechar = ignoreSingleChars(wrongWordList);
      setWrongWords(removedSinglechar);
      // Underline new errors in the editor
      removedSinglechar.forEach((word) => underlineWordInEditor(quill, word));

      // Update the errors state
      setErrors(removedSinglechar);
    }

    setIsLoading(false);
  };

  const handleInputClick = (e) => {
    e.target.focus(); // Focus the input when clicked
  };

  return (
    <div className="flex justify-center min-h-screen bg-gray-500 p-3">
      <div className="w-full max-w-full bg-white rounded-lg shadow-md p-4">
        {" "}
        {/* Set to max-w-full for better mobile handling */}
        {/* Buttons for downloading content */}
        <EditorButtons
          text={text}
          quillRef={quillRef}
          handleRefresh={handleRefresh}
        />
        <ReactQuill
          ref={quillRef}
          value={text}
          onChange={handleInputChange}
          onKeyDown={handleKeyDown}
          modules={editorModules}
          className=""
          style={{ height: "500px", minHeight: "400px", width: "100%" }} // Increase minHeight as needed
        />
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
                    !replacementWord.trim()
                      ? "opacity-50 cursor-not-allowed"
                      : ""
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
        {/* Tooltip for Suggestions */}
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
      </div>
      {isLoading && <LoadingComponent />}
    </div>
  );
};

export default SpellCheckEditor;