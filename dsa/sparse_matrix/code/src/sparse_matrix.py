class SparseMatrix:
    def __init__(self, matrixFilePath=None, numRows=0, numCols=0):
        """
        Initialize a sparse matrix from a file or with given dimensions.
        """
        self.matrix = {}
        self.rows = numRows
        self.cols = numCols
        
        if matrixFilePath:
            self.load_from_file(matrixFilePath)

    def load_from_file(self, filePath):
        """
        Load a sparse matrix from a file.
        """
        try:
            with open(filePath, 'r') as file:
                lines = file.readlines()
                self.rows = int(lines[0].split('=')[1].strip())
                self.cols = int(lines[1].split('=')[1].strip())
                
                for line in lines[2:]:
                    line = line.strip()
                    if not line:
                        continue
                    if not (line.startswith('(') and line.endswith(')')):
                        raise ValueError("Invalid format in input file")
                    
                    row, col, value = map(int, line[1:-1].split(','))
                    self.setElement(row, col, value)
                    
        except Exception as e:
            raise ValueError(f"Error reading file: {str(e)}")

    def getElement(self, currRow, currCol):
        """
        Get the element at the specified row and column.
        """
        return self.matrix.get((currRow, currCol), 0)

    def setElement(self, currRow, currCol, value):
        """
        Set the element at the specified row and column.
        """
        if value != 0:
            self.matrix[(currRow, currCol)] = value
        elif (currRow, currCol) in self.matrix:
            del self.matrix[(currRow, currCol)]

    def add(self, other):
        """
        Add two sparse matrices.
        """
        if self.rows != other.rows or self.cols != other.cols:
            raise ValueError("Matrices dimensions must match for addition")
        
        result = SparseMatrix(numRows=self.rows, numCols=self.cols)
        for (row, col), value in self.matrix.items():
            result.setElement(row, col, value + other.getElement(row, col))
        return result

    def subtract(self, other):
        """
        Subtract one sparse matrix from another.
        """
        if self.rows != other.rows or self.cols != other.cols:
            raise ValueError("Matrices dimensions must match for subtraction")
        
        result = SparseMatrix(numRows=self.rows, numCols=self.cols)
        for (row, col), value in self.matrix.items():
            result.setElement(row, col, value - other.getElement(row, col))
        return result

    def multiply(self, other):
        """
        Multiply two sparse matrices.
        """
        if self.cols != other.rows:
            raise ValueError("Number of columns in first matrix must match number of rows in second matrix")
        
        result = SparseMatrix(numRows=self.rows, numCols=other.cols)
        for (i, k), val1 in self.matrix.items():
            for j in range(other.cols):
                val2 = other.getElement(k, j)
                if val2 != 0:
                    result.setElement(i, j, result.getElement(i, j) + val1 * val2)
        return result

    def __str__(self):
        """
        String representation of the sparse matrix showing non-zero values.
        """
        result = []
        for row in range(self.rows):
            row_values = []
            for col in range(self.cols):
                value = self.getElement(row, col)
                row_values.append(f"{value:>5}")  # Right-align values with 5 spaces
            result.append(" ".join(row_values))
        return "\n".join(result) + f"\n\nSparseMatrix(rows={self.rows}, cols={self.cols}, non_zero_elements={len(self.matrix)})"
