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
import BloomFilter from "bloom-filter-new";
import { ignoreSingleChars, isSingleCharacter } from "../services/editorUtils";
//import SymSpell from "node-symspell-new";

const QuillEditor = () => {
  const [content, setContent] = useState("");
  const [pages, setPages] = useState([0]);
  const [pageSize, setPageSize] = useState({ width: 816, height: 1056 }); // Default A4 size
  const quillRef = useRef(null);
  const [mouseDown, setMouseDown] = useState(false); // Track if mouse is down

  const [text, setText] = useState(""); // Set initial text
  const [errors, setErrors] = useState([]);
  const [suggestions, setSuggestions] = useState({});
  const [clickedWord, setClickedWord] = useState(null);
  const [tooltipPosition, setTooltipPosition] = useState({});
  const [replacementWord, setReplacementWord] = useState("");
  const [isModalOpen, setIsModalOpen] = useState(false);
  const [isLoading, setIsLoading] = useState(false);
  const [bloomFilter, setBloomFilter] = useState(null);
  //const symSpell = new SymSpell(maxEditDistance, prefixLength);

  const maxEditDistance = 3;
  const prefixLength = 7;

  //const values
  const specialChars = "!@#$%^&*()_+[]{}|;:',.<>/?~-=\\\"";

  // Load BloomFilter from a file when the component mounts
  useEffect(() => {
    const filePath = "assets/collection.txt";

    const loadBloomFilter = async () => {
      try {
        const filter = await BloomFilter.fromFile(filePath, 100000, 0.001);
        setBloomFilter(filter);
        // Load the dictionary via IPC as well
        //const dictionaryPath = "../assets/word_frequency.txt";
        //await symSpell.loadDictionary(dictionaryPath, 0, 1); // Load dictionary from the file content
      } catch (error) {
        console.error("Error loading Bloom Filter:", error);
      }
    };

    loadBloomFilter();
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
        console.log(word);
        handleCheckWord(word);

        //const suggestions = await getSuggestions(word);
        //console.log("Suggestions:", suggestions);

        // Get detailed SymSpell info
        //const info = await getSymSpellInfo();
        //console.log("SymSpell Info:", info);
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
            const isContained = await bloomFilter.contains(lastWord); //returns true or false

            //if flase then underline
            if (!isContained) {
              setErrors((prevErrors) => [...prevErrors, lastWord]);
              const quill = quillRef.current?.getEditor();
              underlineWordInEditor(quill, lastWord);
            }
          }
        }
      }, 300); // Adjust the debounce time as needed
    }
  };
  return (
    <div className="editor-container">
      <div className="editor-toolbar-container">
        <EditorToolbar
          quillRef={quillRef} // Pass the quill reference to the toolbar
          setPageSize={setPageSize}
        />
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
    </div>
  );
};

export default QuillEditor;
