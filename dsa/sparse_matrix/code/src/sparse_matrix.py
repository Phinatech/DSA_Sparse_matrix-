class SparseMatrix:
    _cache = {}  # Class-level cache for loaded matrices

    def __str__(self):
        """Returns a formatted string representation of the matrix"""
        output = []
        for row in range(self.numRows):
            row_data = []
            for col in range(self.numCols):
                row_data.append(str(self.getElement(row, col)))
            output.append(" ".join(row_data))
        return "\n".join(output)

    def __init__(self, matrixFilePath=None, numRows=None, numCols=None):
        if matrixFilePath is not None:
            if matrixFilePath in self._cache:
                cached = self._cache[matrixFilePath]
                self.numRows = cached.numRows
                self.numCols = cached.numCols
                self.data = cached.data.copy()
            else:
                self.load_from_file(matrixFilePath)
                self._cache[matrixFilePath] = self
        elif numRows is not None and numCols is not None:
            self.numRows = numRows
            self.numCols = numCols
            self.data = {}
        else:
            raise ValueError("Either matrixFilePath or numRows and numCols must be provided.")

    def load_from_file(self, matrixFilePath):
        try:
            with open(matrixFilePath, 'r') as file:
                content = file.read()
                lines = content.splitlines()
                self.numRows = int(lines[0].split('=')[1].strip())
                self.numCols = int(lines[1].split('=')[1].strip())
                self.data = {}
                # Process all data lines in one go
                data_lines = [line.strip() for line in lines[2:] if line.strip()]
                for line in data_lines:
                    row, col, value = map(int, line.strip('()').split(','))
                    self.setElement(row, col, value)
        except Exception as e:
            raise ValueError(f"Error loading file: {e}")

    def getElement(self, currRow, currCol):
        return self.data.get((currRow, currCol), 0)

    def setElement(self, currRow, currCol, value):
        if value != 0:
            self.data[(currRow, currCol)] = value
        elif (currRow, currCol) in self.data:
            del self.data[(currRow, currCol)]

    def add(self, other):
        if self.numRows != other.numRows or self.numCols != other.numCols:
            raise ValueError("Matrices dimensions do not match for addition.")
        result = SparseMatrix(numRows=self.numRows, numCols=self.numCols)
        for (row, col) in set(self.data.keys()).union(other.data.keys()):
            sum_val = self.getElement(row, col) + other.getElement(row, col)
            result.setElement(row, col, sum_val)
        return result

    def subtract(self, other):
        if self.numRows != other.numRows or self.numCols != other.numCols:
            raise ValueError("Matrices dimensions do not match for subtraction.")
        result = SparseMatrix(numRows=self.numRows, numCols=self.numCols)
        for (row, col) in set(self.data.keys()).union(other.data.keys()):
            sub_val = self.getElement(row, col) - other.getElement(row, col)
            result.setElement(row, col, sub_val)
        return result

    def multiply(self, other):
        if self.numCols != other.numRows:
            raise ValueError("Number of columns in the first matrix must equal the number of rows in the second matrix.")
        print()
        result = SparseMatrix(numRows=self.numRows, numCols=other.numCols)
        
        # Precompute columns for each row in the second matrix
        other_cols = {}
        for (row, col), val in other.data.items():
            if row not in other_cols:
                other_cols[row] = []
            other_cols[row].append(col)
        
        # Perform optimized multiplication
        for (row_a, col_a), val_a in self.data.items():
            if col_a in other_cols:
                for col_b in other_cols[col_a]:
                    val_b = other.getElement(col_a, col_b)
                    if val_b != 0:
                        result.setElement(row_a, col_b, result.getElement(row_a, col_b) + val_a * val_b)
        return result
