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

def validate_and_perform_operations(matrices):
    if len(matrices) < 2:
        print("\nError: Need at least 2 matrices to perform operations")
        return

    print("\nLoaded Matrices:")
    for idx, matrix in enumerate(matrices, 1):
        print(f"\nMatrix {idx}:")
        print(matrix)

    print("\nSelect two matrices to perform operations:")
    try:
        mat1_idx = int(input("Enter first matrix number: ")) - 1
        mat2_idx = int(input("Enter second matrix number: ")) - 1
        
        if mat1_idx < 0 or mat1_idx >= len(matrices) or mat2_idx < 0 or mat2_idx >= len(matrices):
            print("Invalid matrix selection")
            return
            
        matrix1 = matrices[mat1_idx]
        matrix2 = matrices[mat2_idx]
        
        print("\nSelect operation:")
        print("1. Addition")
        print("2. Subtraction")
        print("3. Multiplication")
        op_choice = input("Enter operation number (1-3): ")
        
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
