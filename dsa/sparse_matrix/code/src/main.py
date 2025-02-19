from sparse_matrix import SparseMatrix
import os

def print_menu():
    print("\nMatrix Operations Menu:")
    print("1. Add Matrices")
    print("2. Subtract Matrices")
    print("3. Multiply Matrices")
    print("4. Exit")

def load_matrices_from_folder(folder_path):
    matrices = []
    for filename in os.listdir(folder_path):
        if filename.endswith(".txt"):
            try:
                matrix = SparseMatrix(os.path.join(folder_path, filename))
                matrices.append(matrix)
            except Exception as e:
                print(f"Failed to load {filename}: {str(e)}")
    return matrices

def get_compatible_matrices(matrices, operation):
    compatible = []
    for i in range(len(matrices)):
        for j in range(len(matrices)):
            if i != j:
                if operation == 'add' or operation == 'subtract':
                    if matrices[i].numRows == matrices[j].numRows and matrices[i].numCols == matrices[j].numCols:
                        compatible.append((i, j))
                elif operation == 'multiply':
                    if matrices[i].numCols == matrices[j].numRows:
                        compatible.append((i, j))
    return compatible

def validate_and_perform_operations(matrices):
    if len(matrices) < 2:
        print("\nError: Need at least 2 matrices to perform operations")
        return

    print("\nSelect operation:")
    print("1. Addition")
    print("2. Subtraction")
    print("3. Multiplication")
    op_choice = input("Enter operation number (1-3): ")
    
    if op_choice not in ['1', '2', '3']:
        print("Invalid operation choice")
        return
        
    operation = 'add' if op_choice == '1' else 'subtract' if op_choice == '2' else 'multiply'
    compatible_pairs = get_compatible_matrices(matrices, operation)
    
    if not compatible_pairs:
        print("\nNo compatible matrix pairs found for this operation")
        return
        
    print("\nCompatible Matrix Pairs:")
    for pair_idx, (i, j) in enumerate(compatible_pairs, 1):
        print(f"\nPair {pair_idx}:")
        print(f"Matrix {i+1}:")
        print(matrices[i])
        print(f"Matrix {j+1}:")
        print(matrices[j])

    print("\nSelect a matrix pair to perform operation:")
    try:
        pair_num = int(input("Enter pair number: ")) - 1
        
        if pair_num < 0 or pair_num >= len(compatible_pairs):
            print("Invalid pair selection")
            return
            
        mat1_idx, mat2_idx = compatible_pairs[pair_num]
        matrix1 = matrices[mat1_idx]
        matrix2 = matrices[mat2_idx]
        
        if op_choice == '1':
            try:
                result = matrix1.add(matrix2)
                print("\nAddition Result:")
                print(result)
            except ValueError as e:
                print(f"\nError: {str(e)}")
        elif op_choice == '2':
            try:
                result = matrix1.subtract(matrix2)
                print("\nSubtraction Result:")
                print(result)
            except ValueError as e:
                print(f"\nError: {str(e)}")
        elif op_choice == '3':
            try:
                result = matrix1.multiply(matrix2)
                print("\nMultiplication Result:")
                print(result)
            except ValueError as e:
                print(f"\nError: {str(e)}")
        else:
            print("Invalid operation choice")
    except ValueError:
        print("Invalid input. Please enter numbers only.")

def main_menu():
    while True:
        print_menu()
        choice = input("Enter your choice (1-4): ")
        
        if choice == '4':
            print("Exiting...")
            return
        elif choice in ['1', '2', '3']:
            folder_path = "dsa/sparse_matrix/sample_inputs"
            matrices = load_matrices_from_folder(folder_path)
            if matrices:
                validate_and_perform_operations(matrices)
            else:
                print("\nNo valid matrices found in the input folder.")
        else:
            print("Invalid choice. Please try again.")

if __name__ == "__main__":
    main_menu()
