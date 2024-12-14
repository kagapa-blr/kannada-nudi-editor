import React, { useRef, useEffect, useMemo } from "react";
import SunEditor from "suneditor-react";
import "suneditor/dist/css/suneditor.min.css"; // Import Sun Editor's CSS File
import knLang from "./assets/kn.json"; // Import the custom Kannada JSON file
import katex from "katex";
import "katex/dist/katex.min.css"; // Import KaTeX styles
// Import toolbar configuration
import toolbarConfig from "./components/toolbarOptions";

const App = () => {
  const editor = useRef();

  // Memoize the language and toolbar config to avoid recreating them on every render
  const memoizedLang = useMemo(() => knLang, []); // Memoize language config
  const memoizedToolbarConfig = useMemo(() => toolbarConfig, []); // Memoize toolbar config

  // The sunEditor parameter will be set to the core suneditor instance when this function is called
  const getSunEditorInstance = (sunEditor) => {
    editor.current = sunEditor;
  };

  // Example function to insert HTML content
  const insertHTMLContent = () => {
    if (editor.current) {
      try {
        editor.current.insertHTML("<p>This is inserted HTML</p>");
      } catch (error) {
        console.error("Error inserting HTML:", error);
      }
    }
  };

  useEffect(() => {
    // Insert content only after editor is initialized
    if (editor.current) {
      insertHTMLContent();
    }
  }, []);

  return (
    <div>
      <SunEditor
        lang={memoizedLang} // Use memoized language config
        getSunEditorInstance={getSunEditorInstance}
        height="600px"
        minHeight="300px"
        maxWidth="100%"
        maxHeight="800px"
        katex={katex}
        setOptions={memoizedToolbarConfig} 
        spellcheck = {false}
      />
    </div>
  );
};

export default App;
