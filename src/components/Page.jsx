import React from "react";

export default function Page({ pageIndex, isLast, pageSize }) {
  const { width, height } = pageSize;

  return (
    <>
      <div
        className="absolute left-0 right-0 bg-white shadow-lg border-2 border-gray-300 rounded-lg"
        style={{
          top: `${pageIndex * height}px`,
          width: `${width}px`,
          height: `${height}px`,
        }}
      >
        <div className="absolute bottom-4 right-4 text-sm text-gray-500">
          Page {pageIndex + 1}
        </div>
      </div>

      {/* Separation line between pages */}
      {!isLast && (
        <div
          className="absolute left-0 right-0 border-t-16 border-blue-600" // Increased border thickness
          style={{
            top: `${(pageIndex + 1) * height - 1}px`,
          }}
        />
      )}
    </>
  );
}
