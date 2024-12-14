// src/components/toolbar/CustomSizeDialog.jsx

import React, { useState } from "react";
import {
  Dialog,
  DialogActions,
  DialogContent,
  DialogTitle,
  TextField,
  Button,
} from "@mui/material";

const CustomSizeDialog = ({ open, onClose, onApply }) => {
  const [customSize, setCustomSize] = useState({ width: "", height: "" });

  const handleWidthChange = (e) => {
    setCustomSize((prev) => ({ ...prev, width: e.target.value }));
  };

  const handleHeightChange = (e) => {
    setCustomSize((prev) => ({ ...prev, height: e.target.value }));
  };

  const applyCustomSize = () => {
    if (customSize.width && customSize.height) {
      onApply({
        width: parseInt(customSize.width),
        height: parseInt(customSize.height),
      });
    }
  };

  return (
    <Dialog open={open} onClose={onClose}>
      <DialogTitle>ಕಸ್ಟಮ್ ಪುಟದ ಗಾತ್ರವನ್ನು ನಮೂದಿಸಿ</DialogTitle>
      <DialogContent>
        <TextField
          label="ಅಗಲ (ಪಿಕ್ಸೆಲ್)"
          type="number"
          fullWidth
          value={customSize.width}
          onChange={handleWidthChange}
          margin="normal"
        />
        <TextField
          label="ಎತ್ತರ (ಪಿಕ್ಸೆಲ್)"
          type="number"
          fullWidth
          value={customSize.height}
          onChange={handleHeightChange}
          margin="normal"
        />
      </DialogContent>
      <DialogActions>
        <Button onClick={onClose} color="secondary">
          ರದ್ದು ಮಾಡಿ
        </Button>
        <Button onClick={applyCustomSize} color="primary">
          ಅನ್ವಯಿಸು
        </Button>
      </DialogActions>
    </Dialog>
  );
};

export default CustomSizeDialog;
