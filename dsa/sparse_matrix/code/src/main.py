from sparse_matrix import SparseMatrix

def print_menu():
    print("\nMatrix Operations Menu:")
    print("1. Add Matrices")
    print("2. Subtract Matrices")
    print("3. Multiply Matrices")
    print("4. Exit")

def main():
    try:
        # Load matrices from files
        matrix1 = SparseMatrix("dsa/sparse_matrix/sample_inputs/matrix1.txt")
        matrix2 = SparseMatrix("dsa/sparse_matrix/sample_inputs/matrix2.txt")
        
        while True:
            print_menu()
            choice = input("Enter your choice (1-4): ")
            
            if choice == '1':
                result = matrix1.add(matrix2)
                print("\nMatrix Addition Result:")
                print(result)
            elif choice == '2':
                result = matrix1.subtract(matrix2)
                print("\nMatrix Subtraction Result:")
                print(result)
            elif choice == '3':
                result = matrix1.multiply(matrix2)
                print("\nMatrix Multiplication Result:")
                print(result)
            elif choice == '4':
                print("Exiting...")
                break
            else:
                print("Invalid choice. Please try again.")
                
    except Exception as e:
        print(f"An error occurred: {str(e)}")

if __name__ == "__main__":
    main()
