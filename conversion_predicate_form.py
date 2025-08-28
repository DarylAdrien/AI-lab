def convert_to_predicate_form(sentence):
    """
    Converts a simple English sentence to a predicate logic form.
    This is a simplified, rule-based approach for demonstration.
    """
    
    # Rule 1: Universal Quantifier (For all)
    if sentence.lower().startswith('all') or sentence.lower().startswith('every'):
        parts = sentence.split()
        variable = parts[1] # e.g., 'man'
        
        # Simplistic assumption: a single predicate after the subject
        if "is" in parts:
            idx = parts.index("is")
            predicate = parts[idx + 1].capitalize()
            return f"∀x ({variable.capitalize()}(x) → {predicate}(x))"
        elif "are" in parts:
            idx = parts.index("are")
            predicate = parts[idx + 1].capitalize()
            return f"∀x ({variable.capitalize()}(x) → {predicate}(x))"
            
    # Rule 2: Existential Quantifier (There exists)
    if sentence.lower().startswith('some') or sentence.lower().startswith('a'):
        parts = sentence.split()
        variable = parts[1] # e.g., 'car'
        
        # Simplistic assumption: two predicates
        if "is" in parts:
            idx = parts.index("is")
            predicate1 = parts[idx - 1].capitalize()
            predicate2 = parts[idx + 1].capitalize()
            return f"∃x ({predicate1}(x) ∧ {predicate2}(x))"
    
    # Rule 3: Simple Atomic Sentence
    if "is" in sentence:
        parts = sentence.split()
        subject = parts[0].capitalize()
        predicate = parts[-1].capitalize()
        return f"{predicate}({subject})"

# Sample Input and Output
sentences = [
    "Apple and vegetables are food.",
    "John likes all kind of food.",
]

print("--- Conversion to Predicate Form ---")
for s in sentences:
    predicate_form = convert_to_predicate_form(s)
    print(f"Sentence: '{s}'")
    print(f"Predicate Form: {predicate_form}\n")