import sys

def is_valid(assignment, words, result):
    """
    Checks if a partial assignment is consistent with the constraints.
    A partial assignment is valid if:
    1. All assigned letters have unique digit values.
    2. The first letter of each word is not 0.
    """
    
    # Check for unique digit assignments
    if len(set(assignment.values())) != len(assignment.values()):
        return False

    # Check that the first letter of a word is not 0
    if assignment.get(words[0][0], None) == 0:
        return False
    if assignment.get(words[1][0], None) == 0:
        return False
    if assignment.get(result[0], None) == 0:
        return False

    return True

def solve_cryptarithmetic(letters, words, result, assignment):
    """
    Recursive backtracking function to solve the puzzle.
    """
    
    # Base Case: All letters have been assigned a value
    if not letters:
        if evaluate(assignment, words, result):
            print("\n--- Solution Found ---")
            print(f"Final assignment: {assignment}")
            return assignment
        return None
    
    # Get the next unassigned letter
    letter = letters[0]
    remaining_letters = letters[1:]
    
    # Try assigning a digit from 0 to 9 to the letter
    for digit in range(10):
        new_assignment = assignment.copy()
        new_assignment[letter] = digit
        
        # Check if the partial assignment is valid
        if is_valid(new_assignment, words, result):
            sys.stdout.write(f"\nTrying to assign '{letter}' = {digit}. Current assignment: {new_assignment}")
            sys.stdout.flush()
            
            # Recurse with the new assignment
            solution = solve_cryptarithmetic(remaining_letters, words, result, new_assignment)
            if solution:
                return solution
    
    return None

def evaluate(assignment, words, result):
    """
    Evaluates the full equation based on the final assignment.
    """
    num1 = int("".join([str(assignment[letter]) for letter in words[0]]))
    num2 = int("".join([str(assignment[letter]) for letter in words[1]]))
    res = int("".join([str(assignment[letter]) for letter in result]))
    
    print(f"\nEquation check: {num1} + {num2} == {res}")
    return num1 + num2 == res

def main():
    """
    Main function to set up and solve the problem.
    """
    puzzle = input("Enter the cryptarithmetic puzzle (e.g., SEND + MORE = MONEY): ")
    puzzle = puzzle.replace(" ", "").upper()
    
    if "+" not in puzzle or "=" not in puzzle:
        print("Invalid puzzle format. Use 'WORD1 + WORD2 = RESULT'.")
        return
    
    parts = puzzle.split('+')
    word1 = parts[0]
    word2_result = parts[1].split('=')
    word2 = word2_result[0]
    result = word2_result[1]
    
    words = [word1, word2]
    
    # Get all unique letters
    all_letters = sorted(list(set(word1 + word2 + result)))
    
    print("\n" + "="*50)
    print("SOLVING CRYPTARITHMETIC PUZZLE")
    print("="*50)
    print(f"Puzzle: {word1} + {word2} = {result}")
    print(f"Unique letters to assign: {all_letters}")
    
    initial_assignment = {}
    solution = solve_cryptarithmetic(all_letters, words, result, initial_assignment)
    
    if solution:
        print("\nSolution found!")
        print(f"Assignment: {solution}")
    else:
        print("\nNo solution found.")

if __name__ == "__main__":
    main()