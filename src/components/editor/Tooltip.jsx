import React, { useEffect, useRef } from "react";

const Tooltip = ({
  clickedWord,
  suggestions,
  tooltipPosition,
  setClickedWord,
  replaceWord,
  addDictionary,
  replaceAll,
  ignoreAll,
}) => {

  // Kannada labels
  const labels = {
    addToDictionary: "Add to Dictionary",
    replaceAll: "Replace All",
    ignoreAll: "Ignore All",
    noSuggestions: "ಯಾವುದೇ ಸಲಹೆಗಳಿಲ್ಲ", // Kannada translation
  };

  const tooltipRef = useRef(null); // Reference to the tooltip container
  const isReplaceAllClickedRef = useRef(false); // Track if "Replace All" was clicked

  useEffect(() => {
    const handleClickOutside = (event) => {
      if (tooltipRef.current && !tooltipRef.current.contains(event.target)) {
        if (!isReplaceAllClickedRef.current) {
          setClickedWord(null); // Close tooltip if "Replace All" was not clicked
        }
      }
    };

    document.addEventListener("mousedown", handleClickOutside);

    return () => {
      document.removeEventListener("mousedown", handleClickOutside);
    };
  }, [setClickedWord]);

  const handleReplaceAll = () => {
    isReplaceAllClickedRef.current = true; // Indicate "Replace All" was clicked
    replaceAll(); // Call the replaceAll function
  };

  const handleCloseTooltip = () => {
    setClickedWord(null); // Close tooltip on click
  };

  return (
    <div
      ref={tooltipRef}
      className="absolute bg-white border border-green-900 p-2 mt-16 rounded shadow-lg z-40"
      style={{
        top: tooltipPosition.top + 100,
        left: tooltipPosition.left,
        minWidth: "150px",
      }}
    >
      {/* Close button */}
      <span
        className="absolute top-0 right-2 cursor-pointer text-red-600 hover:bg-gray-600 text-3xl"
        onClick={handleCloseTooltip}
        aria-label="Close"
      >
        &times;
      </span>
      <div className="mt-3 space-y-0.5">
        {suggestions[clickedWord]?.length > 0 ? (
          suggestions[clickedWord].map((suggestion, index) => (
            <div key={suggestion}>
              <div
                className="cursor-pointer text-green-700 hover:bg-gray-200 text-sm hover:font-bold"
                onClick={() => replaceWord(suggestion)}
              >
                {suggestion}
              </div>
              {index < suggestions[clickedWord].length - 1 && (
                <hr className="my-0 border-t border-gray-300" />
              )}
            </div>
          ))
        ) : (
          <div className="text-gray-500 text-sm">
            {labels.noSuggestions}
          </div>
        )}
        <hr className="my-1 border-t border-gray-300" />
        <div
          className="cursor-pointer text-black hover:bg-gray-200 text-sm hover:font-bold"
          onClick={addDictionary}
        >
          {labels.addToDictionary}
        </div>
        <hr className="my-1 border-t border-gray-300" />
        <div
          className="cursor-pointer text-black hover:bg-gray-200 text-sm hover:font-bold"
          onClick={handleReplaceAll}
        >
          {labels.replaceAll}
        </div>
        <hr className="my-1 border-t border-gray-300" />
        <div
          className="cursor-pointer text-black hover:bg-gray-200 text-sm hover:font-bold"
          onClick={ignoreAll}
        >
          {labels.ignoreAll}
        </div>
      </div>
    </div>
  );
};

export default Tooltip;
