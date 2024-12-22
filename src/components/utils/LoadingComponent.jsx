import { CircularProgress } from "@mui/material";

const LoadingComponent = () => {
  const label = "ದಯವಿಟ್ಟು ನಿರೀಕ್ಷಿಸಿ...";

  return (
    <div className="fixed inset-0 flex items-center justify-center z-50 bg-opacity-75 bg-gray-700">
      {/* Customize the CircularProgress with a color */}
      <CircularProgress
        size={60} // Adjust the size for a larger spinner
        thickness={4} // Change thickness to make it more prominent
        color="success" // Use Material UI secondary color or provide a custom color
        className="animate-spin" // Add animation class from Tailwind to create smooth spinning effect
      />
      <span className="ml-4 text-white text-2xl font-bold text-shadow-lg">
        {label}
      </span>
    </div>
  );
};

export default LoadingComponent;
