from editor.components.ascii_unicode_ConversionDialog import show_error_popup


class TableFunctionality:
    def __init__(self):
        pass
    def removeRow(self, table, cursor):
        try:
            # Get the cursor position
            cursor_position = cursor.position()
            # Find the cell containing the cursor
            cell = table.cellAt(cursor_position)
            # Check if a valid cell is found
            if cell.isValid():
                # Get the row index of the cell
                row_index = cell.row()
                # Remove the row
                table.removeRows(row_index, 1)
        except Exception as e:
            show_error_popup(str(e))

    def removeCol(self, table, cursor):
        col = cursor.columnNumber()
        table.removeColumns(col, 1)

    def insertRow(self, table, cursor):
        row = cursor.blockNumber()
        table.insertRows(row, 1)

    def insertCol(self, table, cursor):
        col = cursor.columnNumber()
        table.insertColumns(col, 1)

    def mergeCells(self, table, cursor):
        table.mergeCells(cursor)

    def splitCell(self, table, cursor):
        cell = table.cellAt(cursor)
        if cell.rowSpan() > 1 or cell.columnSpan() > 1:
            table.splitCell(cell.row(), cell.column(), 1, 1)