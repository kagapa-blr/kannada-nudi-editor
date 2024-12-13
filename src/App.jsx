import { useState } from "react";
import WordLikeEditor from "./WordLikeEditor";

function App() {
  return (
    <>
      <main className="container mx-auto px-4 py-8">
        <h1 className="text-3xl font-bold mb-6 text-center">
          Enhanced Word-like Document Editor (JavaScript)
        </h1>
        <WordLikeEditor />
      </main>
    </>
  );
}

export default App;
