import React from "react";
import { SampleBase } from "./components/sample-base";
import Editor from "./components/Editor";
import { L10n, setCulture } from "@syncfusion/ej2-base";
import * as EJ2_LOCALE from "../src/assets/kn.json";

L10n.load({ kn: EJ2_LOCALE.kn });
setCulture("kn");

export default class App extends SampleBase {
  render() {
    return (
      <div className="control-pane">
        <div className="col-lg-12">
          <Editor />
        </div>
      </div>
    );
  }
}
