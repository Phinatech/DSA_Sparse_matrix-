import os
from typing import Dict, Tuple, Optional, Union, Set

class SparseMatrix:
    """A class to represent and operate on sparse matrices efficiently."""
    
    _cache: Dict[str, 'SparseMatrix'] = {}  # Class-level cache to store loaded matrices

    def __init__(self, file_path: Optional[str] = None, 
                 rows: Optional[int] = None, 
                 cols: Optional[int] = None):
        """Initialize a sparse matrix from file or with given dimensions.
        
        Args:
            file_path: Path to matrix file (optional)
            rows: Number of rows (required if file_path not provided)
            cols: Number of columns (required if file_path not provided)
            
        Raises:
            ValueError: If neither file_path nor dimensions are provided
        """
        if file_path:
            self._load_or_cache(file_path)
        elif rows is not None and cols is not None:
            self.numRows, self.numCols = rows, cols
            self.data: Dict[Tuple[int, int], int] = {}
        else:
            raise ValueError("Provide either a file path or matrix dimensions.")

    def _load_or_cache(self, file_path: str) -> None:
        """Load matrix from file or use cached version if available.
        
        Args:
            file_path: Path to matrix file
            
        Raises:
            ValueError: If file cannot be loaded
        """
        if not os.path.exists(file_path):
            raise ValueError(f"File not found: {file_path}")
            
        if file_path in self._cache:
            cached = self._cache[file_path]
            self.numRows, self.numCols, self.data = cached.numRows, cached.numCols, cached.data.copy()
        else:
            self._load_from_file(file_path)
            self._cache[file_path] = self

    def _load_from_file(self, file_path: str) -> None:
        """Load matrix data from file.
        
        Args:
            file_path: Path to matrix file
            
        Raises:
            ValueError: If file format is invalid
        """
        try:
            with open(file_path, 'r') as file:
                lines = file.read().strip().split("\n")
                if len(lines) < 2:
                    raise ValueError("Invalid file format: missing dimension lines")

            # Validate and extract matrix dimensions
            try:
                self.numRows = int(lines[0].split('=')[1].strip())
                self.numCols = int(lines[1].split('=')[1].strip())
            except (IndexError, ValueError) as e:
                raise ValueError("Invalid dimension format in file") from e

            if self.numRows <= 0 or self.numCols <= 0:
                raise ValueError("Matrix dimensions must be positive integers")
            
            self.data = {}
            
            # Validate and extract matrix entries
            for line in lines[2:]:
                if line.strip():
                    try:
                        parts = line.strip("()").split(',')
                        if len(parts) != 3:
                            raise ValueError("Invalid entry format")
                        row, col, value = map(int, parts)
                        if row < 0 or col < 0:
                            raise ValueError("Row and column indices must be non-negative")
                        self.data[(row, col)] = value
                    except ValueError as e:
                        raise ValueError(f"Invalid matrix entry: {line}") from e

        except Exception as e:
            raise ValueError(f"Error reading matrix file {file_path}: {str(e)}")

    def get(self, row: int, col: int) -> int:
        """Get the value at a specific matrix position.
        
        Args:
            row: Row index (0-based)
            col: Column index (0-based)
            
        Returns:
            The value at (row, col) or 0 if the position is empty
            
        Raises:
            ValueError: If row or col are out of bounds
        """
        if row < 0 or row > self.numRows or col < 0 or col > self.numCols:
            print(self.numRows, self.numCols)
            raise ValueError(f"Position ({row}, {col}) is out of bounds")
        return self.data.get((row, col), 0)

    def set(self, row: int, col: int, value: int) -> None:
        """Set the value at a specific matrix position.
        
        Args:
            row: Row index (0-based)
            col: Column index (0-based)
            value: Value to set (0 will remove the entry)
            
        Raises:
            ValueError: If row or col are out of bounds
        """
        if row < 0 or row > self.numRows or col < 0 or col > self.numCols:
            raise ValueError(f"Position ({row}, {col}) is out of bounds")
        if value:
            self.data[(row, col)] = value
        else:
            self.data.pop((row, col), None)

    def operate(self, other: 'SparseMatrix', operation: callable) -> 'SparseMatrix':
        """Perform element-wise operation between two matrices.
        
        Args:
            other: Another SparseMatrix to operate with
            operation: Function to apply to corresponding elements
            
        Returns:
            New SparseMatrix containing the result
            
        Raises:
            ValueError: If matrices have different dimensions
            TypeError: If other is not a SparseMatrix
        """
        if not isinstance(other, SparseMatrix):
            raise TypeError("Operation requires another SparseMatrix")
            
        if self.numRows != other.numRows or self.numCols != other.numCols:
            raise ValueError(f"Matrices must have the same dimensions for operation")
            
        result = SparseMatrix(rows=self.numRows, cols=self.numCols)
        for key in set(self.data.keys()).union(other.data.keys()):
            new_val = operation(self.get(*key), other.get(*key))
            result.set(*key, new_val)
        return result

    def add(self, other: 'SparseMatrix') -> 'SparseMatrix':
        """Add another matrix to this one.
        
        Args:
            other: Another SparseMatrix to add
            
        Returns:
            New SparseMatrix containing the sum
            
        Raises:
            ValueError: If matrices have different dimensions
            TypeError: If other is not a SparseMatrix
        """
        return self.operate(other, lambda x, y: x + y)

    def subtract(self, other: 'SparseMatrix') -> 'SparseMatrix':
        """Subtract another matrix from this one.
        
        Args:
            other: Another SparseMatrix to subtract
            
        Returns:
            New SparseMatrix containing the difference
            
        Raises:
            ValueError: If matrices have different dimensions
            TypeError: If other is not a SparseMatrix
        """
        return self.operate(other, lambda x, y: x - y)

    def multiply(self, other: 'SparseMatrix') -> 'SparseMatrix':
        """Multiply this matrix with another one."""

        if not isinstance(other, SparseMatrix):
            raise TypeError("Multiplication requires another SparseMatrix")

        if self.numCols != other.numRows:
            raise ValueError(
                f"Matrix multiplication requires first matrix cols ({self.numCols}) "
                f"to match second matrix rows ({other.numRows})"
            )

        result = SparseMatrix(rows=self.numRows, cols=other.numCols)
        other_transposed = other.transpose()

        for (r1, c1), v1 in self.data.items():
            row_entries = other_transposed.get_row_entries(c1)
            for c2 in row_entries:
                v2 = other.get(c1, c2)
                current_value = result.get(r1, c2)
                result.set(r1, c2, current_value + v1 * v2)

        return result



    def transpose(self) -> 'SparseMatrix':
        """Create and return the transpose of this matrix.
        
        Returns:
            New SparseMatrix that is the transpose of this one
        """
        transposed = SparseMatrix(rows=self.numCols, cols=self.numRows)
        for (row, col), value in self.data.items():
            transposed.set(col, row, value)
        return transposed

    def get_row_entries(self, row: int) -> Set[int]:
        """Get all column indices with non-zero entries in a given row.
        
        Args:
            row: Row index to examine
            
        Returns:
            Set of column indices with non-zero entries
            
        Raises:
            ValueError: If row is out of bounds
        """
        if row < 0 or row > self.numRows:
            raise ValueError(f"Row index {row} is out of bounds")
        return {col for (r, col) in self.data.keys() if r == row}
