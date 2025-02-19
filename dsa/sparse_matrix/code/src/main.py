from sparse_matrix import SparseMatrix
import os

class MatrixCompatibilityChecker:
    def __init__(self, input_folder):
        self.input_folder = input_folder
        self.sample_files = self._load_sample_files()
        self.compatible_pairs = {'addition': [], 'subtraction': [], 'multiplication': []}
    
    def _load_sample_files(self):
        files = [f for f in os.listdir(self.input_folder) if f.endswith('.txt')]
        if len(files) < 2:
            raise ValueError("Not enough sample input files to proceed.")
        return files
    
    def display_files(self):
        print("\nAvailable matrix files:")
        for idx, file in enumerate(self.sample_files, start=1):
            print(f"{idx}. {file}")
    
    def check_compatibility(self):
        matrices = {file: SparseMatrix(os.path.join(self.input_folder, file)) for file in self.sample_files}
        
        for i, file1 in enumerate(self.sample_files):
            for file2 in self.sample_files[i+1:]:
                self._evaluate_pair(matrices[file1], matrices[file2], file1, file2)
        
        if not any(self.compatible_pairs.values()):
            raise ValueError("No compatible matrix pairs found for operations.")
    
    def _evaluate_pair(self, matrix1, matrix2, file1, file2):
        if matrix1.numRows == matrix2.numRows and matrix1.numCols == matrix2.numCols:
            self.compatible_pairs['addition'].append((file1, file2, "Same dimensions"))
            self.compatible_pairs['subtraction'].append((file1, file2, "Same dimensions"))
        else:
            print(f"\nAddition/Subtraction not possible between {file1} and {file2}:\n  Matrix 1: {matrix1.numRows}x{matrix1.numCols}\n  Matrix 2: {matrix2.numRows}x{matrix2.numCols}")
        
        if matrix1.numCols == matrix2.numRows:
            self.compatible_pairs['multiplication'].append((file1, file2, "Cols of first = Rows of second"))
        else:
            print(f"\nMultiplication not possible between {file1} and {file2}:\n  Matrix 1 columns: {matrix1.numCols}\n  Matrix 2 rows: {matrix2.numRows}")
    
    def display_compatible_pairs(self):
        print("\nCompatible matrix pairs for operations:")
        for operation, pairs in self.compatible_pairs.items():
            if pairs:
                print(f"\n{operation.capitalize()}:")
                for idx, (file1, file2, condition) in enumerate(pairs, start=1):
                    print(f"{idx}. {file1} <-> {file2} | Condition: {condition}")

def main():
    input_folder = 'dsa/sparse_matrix/sample_inputs'
    checker = MatrixCompatibilityChecker(input_folder)
    checker.display_files()
    checker.check_compatibility()
    checker.display_compatible_pairs()

if __name__ == "__main__":
    main()