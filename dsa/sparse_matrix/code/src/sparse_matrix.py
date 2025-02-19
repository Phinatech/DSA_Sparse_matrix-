import os

class SparseMatrix:
    _cache = {}  # Class-level cache to store loaded matrices

    def __init__(self, file_path=None, rows=None, cols=None):
        if file_path:
            self._load_or_cache(file_path)
        elif rows is not None and cols is not None:
            self.numRows, self.numCols = rows, cols
            self.data = {}
        else:
            raise ValueError("Provide either a file path or matrix dimensions.")

    def _load_or_cache(self, file_path):
        if file_path in self._cache:
            cached = self._cache[file_path]
            self.numRows, self.numCols, self.data = cached.numRows, cached.numCols, cached.data.copy()
        else:
            self._load_from_file(file_path)
            self._cache[file_path] = self

    def _load_from_file(self, file_path):
        try:
            with open(file_path, 'r') as file:
                lines = file.read().strip().split("\n")

            # Extracting matrix dimensions
            self.numRows = int(lines[0].split('=')[1].strip())
            self.numCols = int(lines[1].split('=')[1].strip())
            self.data = {}

            # Extract matrix entries
            for line in lines[2:]:
                if line.strip():
                    parts = line.strip("()").split(',')
                    if len(parts) == 3:
                        row, col, value = map(int, parts)
                        self.data[(row, col)] = value

        except Exception as e:
            raise ValueError(f"Error reading matrix file: {e}")

    def get(self, row, col):
        return self.data.get((row, col), 0)

    def set(self, row, col, value):
        if value:
            self.data[(row, col)] = value
        else:
            self.data.pop((row, col), None)

    def operate(self, other, operation):
        if self.numRows != other.numRows or self.numCols != other.numCols:
            raise ValueError(f"Matrices must have the same dimensions for {operation}.")
        result = SparseMatrix(rows=self.numRows, cols=self.numCols)
        for key in set(self.data.keys()).union(other.data.keys()):
            new_val = operation(self.get(*key), other.get(*key))
            result.set(*key, new_val)
        return result

    def add(self, other):
        return self.operate(other, lambda x, y: x + y)

    def subtract(self, other):
        return self.operate(other, lambda x, y: x - y)

    def multiply(self, other):
        if self.numCols != other.numRows:
            raise ValueError("Matrix multiplication requires first matrix cols to match second matrix rows.")
        result = SparseMatrix(rows=self.numRows, cols=other.numCols)
        other_transposed = other.transpose()
        for (r1, c1), v1 in self.data.items():
            for c2 in other_transposed.get_row_entries(c1):
                result.set(r1, c2, result.get(r1, c2) + v1 * other.get(c1, c2))
        return result

    def transpose(self):
        transposed = SparseMatrix(rows=self.numCols, cols=self.numRows)
        for (row, col), value in self.data.items():
            transposed.set(col, row, value)
        return transposed

    def get_row_entries(self, row):
        return {col for (r, col) in self.data.keys() if r == row}