// CustomSizeDialog.js
import React from "react";
import { Dialog, DialogTitle, DialogContent, TextField, DialogActions, Button } from "@mui/material";

const CustomSizeDialog = ({ openModal, customSize, handleCustomWidthChange, handleCustomHeightChange, applyCustomSize, handleCloseModal }) => (
  <Dialog open={openModal} onClose={handleCloseModal}>
    <DialogTitle>Enter Custom Page Size</DialogTitle>
    <DialogContent>
      <TextField
        label="Width (px)"
        type="number"
        fullWidth
        value={customSize.width}
        onChange={handleCustomWidthChange}
        margin="normal"
      />
      <TextField
        label="Height (px)"
        type="number"
        fullWidth
        value={customSize.height}
        onChange={handleCustomHeightChange}
        margin="normal"
      />
    </DialogContent>
    <DialogActions>
      <Button onClick={handleCloseModal} color="secondary">Cancel</Button>
      <Button onClick={applyCustomSize} color="primary">Apply</Button>
    </DialogActions>
  </Dialog>
);

export default CustomSizeDialog;
