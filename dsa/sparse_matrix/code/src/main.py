from typing import Dict, List, Tuple
from sparse_matrix import SparseMatrix
import os

class MatrixCompatibilityChecker:
    """A class to check compatibility between sparse matrices for various operations."""
    
    def __init__(self, input_folder: str):
        """Initialize the compatibility checker.
        
        Args:
            input_folder: Path to folder containing matrix files
            
        Raises:
            ValueError: If input folder doesn't exist or has insufficient files
        """
        if not os.path.exists(input_folder):
            raise ValueError(f"Input folder does not exist: {input_folder}")
            
        self.input_folder = input_folder
        self.sample_files = self._load_sample_files()
        self.compatible_pairs: Dict[str, List[Tuple[str, str, str]]] = {
            'addition': [],
            'subtraction': [],
            'multiplication': []
        }
    
    def _load_sample_files(self) -> List[str]:
        """Load matrix files from the input folder.
        
        Returns:
            List of matrix file names
            
        Raises:
            ValueError: If folder contains less than 2 matrix files
        """
        try:
            files = [f for f in os.listdir(self.input_folder) if f.endswith('.txt')]
            if len(files) < 2:
                raise ValueError(f"Not enough matrix files found in {self.input_folder}. Need at least 2 files.")
            return files
        except Exception as e:
            raise ValueError(f"Error loading matrix files: {str(e)}")
    
    def display_files(self) -> None:
        """Display available matrix files with their indices."""
        print("\nAvailable matrix files:")
        for idx, file in enumerate(self.sample_files, start=1):
            print(f"{idx}. {file}")
        print()
    
    def check_compatibility(self) -> None:
        """Check compatibility between all matrix pairs for operations.
        
        Raises:
            ValueError: If no compatible pairs are found
        """
        try:
            matrices = {
                file: SparseMatrix(os.path.join(self.input_folder, file)) 
                for file in self.sample_files
            }
            
            for i, file1 in enumerate(self.sample_files):
                for file2 in self.sample_files[i+1:]:
                    self._evaluate_pair(matrices[file1], matrices[file2], file1, file2)
            
            if not any(self.compatible_pairs.values()):
                raise ValueError("No compatible matrix pairs found for operations.")
        except Exception as e:
            raise ValueError(f"Error checking matrix compatibility: {str(e)}")
    
    def _evaluate_pair(self, matrix1: SparseMatrix, matrix2: SparseMatrix, 
                      file1: str, file2: str) -> None:
        """Evaluate compatibility between two matrices for operations.
        
        Args:
            matrix1: First sparse matrix
            matrix2: Second sparse matrix
            file1: Name of first matrix file
            file2: Name of second matrix file
        """
        # Check addition/subtraction compatibility
        if matrix1.numRows == matrix2.numRows and matrix1.numCols == matrix2.numCols:
            self.compatible_pairs['addition'].append((file1, file2, "Same dimensions"))
            self.compatible_pairs['subtraction'].append((file1, file2, "Same dimensions"))
        else:
            print(f"\nAddition/Subtraction not possible between {file1} and {file2}:")
            print(f"  Matrix 1: {matrix1.numRows}x{matrix1.numCols}")
            print(f"  Matrix 2: {matrix2.numRows}x{matrix2.numCols}")
        
        # Check multiplication compatibility
        if matrix1.numCols == matrix2.numRows:
            self.compatible_pairs['multiplication'].append((file1, file2, "Cols of first = Rows of second"))
        else:
            print(f"\nMultiplication not possible between {file1} and {file2}:")
            print(f"  Matrix 1 columns: {matrix1.numCols}")
            print(f"  Matrix 2 rows: {matrix2.numRows}")
    
    def display_compatible_pairs(self) -> None:
        """Display all compatible matrix pairs for operations."""
        print("\nCompatible matrix pairs for operations:")
        for operation, pairs in self.compatible_pairs.items():
            if pairs:
                print(f"\n{operation.capitalize()}:")
                for idx, (file1, file2, condition) in enumerate(pairs, start=1):
                    print(f"{idx}. {file1} <-> {file2} | Condition: {condition}")
        print()

def main() -> None:
    """Main function to run the matrix compatibility checker."""
    try:
        input_folder = 'dsa/sparse_matrix/sample_inputs'
        checker = MatrixCompatibilityChecker(input_folder)
        checker.display_files()
        checker.check_compatibility()
        checker.display_compatible_pairs()
    except Exception as e:
        print(f"\nError: {str(e)}")
        print("Please check your input files and try again.")

if __name__ == "__main__":
    main()
