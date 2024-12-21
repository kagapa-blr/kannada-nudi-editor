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
