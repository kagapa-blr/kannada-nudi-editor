import { SampleBase } from "./sample-base";
import {
  DocumentEditorContainerComponent,
  Toolbar,
} from "@syncfusion/ej2-react-documenteditor";
import { TitleBar } from "./title-bar";
import { L10n, setCulture } from "@syncfusion/ej2-base";
import * as EJ2_LOCALE from "../src/assets/kn.json";
L10n.load({ kn: EJ2_LOCALE.kn });
setCulture("kn");
DocumentEditorContainerComponent.Inject(Toolbar);

export default class App extends SampleBase {
  items = [
    "New",
    "Open",
    "Undo",
    "Redo",
    "Comments",
    "Image",
    "Table",
    "Hyperlink",
    "Bookmark",
    "TableOfContents",
    "Header",
    "Footer",
    "PageSetup",
    "PageNumber",
    "Break",
    "Find",
    "LocalClipboard",
    "RestrictEditing",
  ];
  hostUrl =
    "https://services.syncfusion.com/react/production/api/documenteditor/";
  container;
  titleBar;

  rendereComplete() {
    window.onbeforeunload = function () {
      return "Want to save your changes?";
    };
    this.container.documentEditor.pageOutline = "#E0E0E0";
    this.container.documentEditor.acceptTab = true;
    this.container.documentEditor.resize();
    this.titleBar = new TitleBar(
      document.getElementById("documenteditor_titlebar"),
      this.container.documentEditor,
      true
    );
    this.onLoadDefault();
  }

  render() {
    return (
      <div className="control-pane">
        <div className="col-lg-12 control-section">
          <div id="documenteditor_titlebar" className="e-de-ctn-title"></div>
          <div id="documenteditor_container_body">
            <DocumentEditorContainerComponent
              id="container"
              ref={(scope) => {
                this.container = scope;
              }}
              style={{ display: "block" }}
              height={"590px"}
              serviceUrl={this.hostUrl}
              enableToolbar={true}
              //toolbarItems={this.items} 
              showPropertiesPane={false}
            />
          </div>
        </div>
      </div>
    );
  }

  onLoadDefault = () => {
    // Set default editor settings
    this.container.documentEditor.documentEditorSettings.showRuler = true;
    this.container.documentChange = () => {
      this.titleBar.updateDocumentTitle();
      this.container.documentEditor.focusIn();
    };

    // Set default title to "Untitled"
    this.container.documentEditor.documentTitle = "Untitled";
  };
}
