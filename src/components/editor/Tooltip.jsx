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
  // Kannada labels for localized messages
  const labels = {
    addToDictionary: "Add to Dictionary",
    replaceAll: "Replace All",
    ignoreAll: "Ignore All",
    noSuggestions: "ಯಾವುದೇ ಸಲಹೆಗಳಿಲ್ಲ", // Kannada translation
  };

  const tooltipRef = useRef(null); // Reference to the tooltip container
  const isReplaceAllClickedRef = useRef(false); // Tracks if "Replace All" was clicked

  // Close tooltip when clicking outside
  useEffect(() => {
    const handleClickOutside = (event) => {
      if (tooltipRef.current && !tooltipRef.current.contains(event.target)) {
        if (!isReplaceAllClickedRef.current) {
          setClickedWord(null); // Close tooltip only if "Replace All" was not clicked
        }
      }
    };

    document.addEventListener("mousedown", handleClickOutside);

    return () => {
      document.removeEventListener("mousedown", handleClickOutside);
    };
  }, [setClickedWord]);

  // Handle "Replace All" action
  const handleReplaceAll = () => {
    isReplaceAllClickedRef.current = true; // Flag to prevent tooltip closure
    replaceAll(); // Call the replaceAll function
  };

  // Close the tooltip
  const handleCloseTooltip = () => {
    setClickedWord(null);
  };

  return (
    <div
      ref={tooltipRef}
      className="absolute bg-white border border-gray-300 rounded-lg shadow-lg p-4 z-40"
      style={{
        top: tooltipPosition.top + 100,
        left: tooltipPosition.left,
        minWidth: "200px",
      }}
    >
      {/* Close Button */}
      <button
        className="absolute top-2 right-2 text-gray-600 hover:text-red-600"
        onClick={handleCloseTooltip}
        aria-label="Close Tooltip"
      >
        &times;
      </button>

      <div className="space-y-2 mt-4">
        {/* Suggestions */}
        {suggestions[clickedWord]?.length > 0 ? (
          suggestions[clickedWord].map((suggestion, index) => (
            <div key={suggestion}>
              <div
                className="cursor-pointer text-blue-600 hover:bg-gray-100 text-sm px-2 py-1 rounded"
                onClick={() => replaceWord(suggestion)}
              >
                {suggestion}
              </div>
              {index < suggestions[clickedWord].length - 1 && (
                <hr className="border-gray-200" />
              )}
            </div>
          ))
        ) : (
          <div className="text-gray-500 text-sm">{labels.noSuggestions}</div>
        )}

        <hr className="border-gray-200" />

        {/* Additional Actions */}
        <div
          className="cursor-pointer text-gray-800 hover:bg-gray-100 text-sm px-2 py-1 rounded"
          onClick={addDictionary}
        >
          {labels.addToDictionary}
        </div>
        <div
          className="cursor-pointer text-gray-800 hover:bg-gray-100 text-sm px-2 py-1 rounded"
          onClick={handleReplaceAll}
        >
          {labels.replaceAll}
        </div>
        <div
          className="cursor-pointer text-gray-800 hover:bg-gray-100 text-sm px-2 py-1 rounded"
          onClick={ignoreAll}
        >
          {labels.ignoreAll}
        </div>
      </div>
    </div>
  );
};

export default Tooltip;
