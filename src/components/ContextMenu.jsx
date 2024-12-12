import React, { useEffect } from "react";

const ContextMenu = ({ container }) => {
  useEffect(() => {
    // Ensure container and documentEditor are initialized before using them
    if (container.current && container.current.documentEditor) {
      const contextMenu = container.current.documentEditor.contextMenu;
      if (contextMenu) {
        const menuItems = [
          {
            text: 'Search In Google',
            id: 'search_in_google',
            iconCss: 'e-icons e-de-ctnr-find',
          },
        ];

        // Adding custom menu items
        contextMenu.addCustomMenu(menuItems, false);

        // Handle custom menu selection
        container.current.documentEditor.customContextMenuSelect = (args) => {
          let id = container.current.documentEditor.element.id;
          if (args.id === id + 'search_in_google') {
            let searchContent = container.current.documentEditor.selection.text;
            if (searchContent && /\S/.test(searchContent)) {
              window.open('http://google.com/search?q=' + searchContent);
            }
          }
        };

        // Handle showing/hiding menu options based on selection
        container.current.documentEditor.customContextMenuBeforeOpen = (args) => {
          let search = document.getElementById(args.ids[0]);
          search.style.display = 'none';
          let searchContent = container.current.documentEditor.selection.text;
          if (searchContent && /\S/.test(searchContent)) {
            search.style.display = 'block';
          }
        };
      }
    }
  }, [container]); // Effect will run when container is initialized

  return null; // No UI is rendered by this component
};

export default ContextMenu;
