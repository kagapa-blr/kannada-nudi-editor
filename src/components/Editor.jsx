import React, { useEffect, useRef } from "react";
import {
  DocumentEditorContainerComponent,
  Toolbar,
} from "@syncfusion/ej2-react-documenteditor";
import { TitleBar } from "./TitleBar";
import { L10n, setCulture } from "@syncfusion/ej2-base";
import * as EJ2_LOCALE from "../../src/assets/kn.json"; // Localization (optional, if you want Kannada locale)

DocumentEditorContainerComponent.Inject(Toolbar);

const Editor = () => {
  const container = useRef(null); // Reference to the DocumentEditorContainerComponent
  let titleBar; // Reference to the TitleBar instance

  // Set the culture for localization
  L10n.load({ kn: EJ2_LOCALE.kn });
  setCulture("kn");

  const hostUrl =
    "https://services.syncfusion.com/react/production/api/documenteditor/";

  const onLoadDefault = () => {
    container.current.documentEditor.documentName = "Getting Started";
    if (titleBar) {
      titleBar.updateDocumentTitle();
    }

    // When document changes, update the title
    container.current.documentChange = () => {
      if (titleBar) {
        titleBar.updateDocumentTitle();
      }
      container.current.documentEditor.focusIn();
    };
  };

  // Handle setup after the document editor has been created
  const renderComplete = () => {
    window.onbeforeunload = () => {
      return "ನಿಮ್ಮ ಬದಲಾವಣೆಗಳನ್ನು ಉಳಿಸಲು ಬಯಸುವಿರಾ?";
    };

    container.current.documentEditor.pageOutline = "#E0E0E0";
    container.current.documentEditor.acceptTab = true;
    container.current.documentEditor.resize();

    // Initialize the TitleBar only if it's not already created
    if (!titleBar) {
      titleBar = new TitleBar(
        document.getElementById("documenteditor_titlebar"),
        container.current.documentEditor,
        true // Ensure the export button is shown
      );
      onLoadDefault();
    }
  };

  // `created()` function to configure additional settings like showing ruler
  const created = () => {
    container.current.documentEditorSettings.showRuler = true;
  };

  // Call renderComplete when the component mounts
  useEffect(() => {
    renderComplete();
  }, []);

  return (
    <div className="control-pane">
      <div className="control-section">
        {/* Title Bar */}
        <div id="documenteditor_titlebar" className="e-de-ctn-title"></div>

        {/* Document Editor Container */}
        <div id="documenteditor_container_body">
          <DocumentEditorContainerComponent
            id="container"
            ref={container}
            style={{ display: "block" }}
            height={"590px"}
            serviceUrl={hostUrl}
            enableToolbar={true}
            locale="kn"
            created={created} // Add created function here
            showPropertiesPane={false}
          />
        </div>
      </div>
    </div>
  );
};

export default Editor;
