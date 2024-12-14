import React from "react";

const PAGE_HEIGHT = 1056; // 11 inches at 96 DPI
const PAGE_WIDTH = 816;   // 8.5 inches at 96 DPI

export default function Page({ pageIndex, isLast }) {
  return (
    <>
      <div
        className="absolute left-0 right-0 bg-white shadow-lg border-2 border-gray-300 rounded-lg"
        style={{
          top: `${pageIndex * PAGE_HEIGHT}px`,
          width: `${PAGE_WIDTH}px`,
          height: `${PAGE_HEIGHT}px`,
        }}
      >
        <div className="absolute bottom-4 right-4 text-sm text-gray-500">
          Page {pageIndex + 1}
        </div>
      </div>

      {/* Separation line between pages */}
      {!isLast && (
        <div
          className="absolute left-0 right-0 border-t-8 border-blue-600"
          style={{
            top: `${(pageIndex + 1) * PAGE_HEIGHT - 1}px`,
          }}
        />
      )}
    </>
  );
}
