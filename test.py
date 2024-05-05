
import os
import re
import shutil
import ast


def read_text_file(file_path):
    try:
        with open(file_path, 'r', encoding='utf-8') as file:
            content = file.read()
            return content
    except FileNotFoundError:
        print(f"Error: File not found at {file_path}")
        return None
    except Exception as e:
        print(f"An error occurred: {e}")
        return None


def write_text_file(output_file_path, content):
    try:
        with open(output_file_path, 'w', encoding='utf-8') as file:
            file.write(content)
            print(f"File successfully updated. Changes saved in {output_file_path}.")
    except Exception as e:
        print(f"An error occurred while writing to the file: {e}")


######################################################################################    
def delete_words_in_file(file_path, output_file_path, words_to_delete):
    try:
        with open(file_path, 'r') as file:
            content = file.read()

        # Add "axiom" to the list of words to delete
        # words_to_delete.append('axiom')

        # Create a regex pattern to match whole words
        pattern = re.compile(r'\b(?:' + '|'.join(re.escape(word) for word in words_to_delete) + r')\b', flags=re.IGNORECASE)
        result_content = pattern.sub('', content)
        
        # Remove any remaining dot and comma
        result_content = result_content.replace('.', '').replace(',', '')

        # Write the modified content back to the file
        with open(output_file_path, 'w') as file:
            file.write(result_content)
        
        print(f"Successfully deleted specified words from '{output_file_path}'. Changes saved in '{output_file_path}'.")
    except Exception as e:
        print(f"An error occurred while deleting words from file: {e}")
# #####################################################


def extract_equivalents(expression):
    if isinstance(expression, ast.Call) and expression.func.id == "equivalent":
        first_arg = extract_equivalents(expression.args[0])
        second_arg = extract_equivalents(expression.args[1])
        return f"(({first_arg} implies {second_arg}) and ({second_arg} implies {first_arg}))"
    elif isinstance(expression, ast.BoolOp):
        op = " or " if isinstance(expression.op, ast.Or) else " and "
        return f"({op.join(extract_equivalents(operand) for operand in expression.values)})"
    elif isinstance(expression, ast.Name):
        return expression.id
    elif isinstance(expression, ast.UnaryOp) and isinstance(expression.op, ast.Not):
        operand = extract_equivalents(expression.operand)
        return f"(not {operand})"
    elif isinstance(expression, (ast.Constant, ast.Num)):
        return str(expression.s if isinstance(expression, ast.Constant) else expression.n)
    elif isinstance(expression, ast.Call):
        # Handle the case of ast.Call objects (recursively extract and transform arguments)
        args = [extract_equivalents(arg) for arg in expression.args]
        return f"{expression.func.id}({', '.join(args)})"
    else:
        return expression

def transform_equivalent(expression):
    # Replace all occurrences of '.' to remove side brackets
    expression = expression.replace(".", "")
    print(f"Transforming equivalent in: {expression}")
    try:
        tree = ast.parse(expression, mode='eval')
    except SyntaxError as e:
        print(f"Syntax error: {e}")
        return None
    
    # Convert the AST back to a string
    transformed_expression = extract_equivalents(tree.body)
    
    if not isinstance(transformed_expression, str):
        print(f"Error: Transformed expression is not a string.")
        return None
    
    print(f"Transformed equivalent: {transformed_expression}")
    return transformed_expression

def transform_equivalent_in_file(file_path, output_file_path):
    try:
        # Read expressions from input file
        with open(file_path, 'r', encoding='utf-8') as input_file:
            expressions = input_file.readlines()

        # Filter out empty lines and invalid characters
        expressions = [expr.strip() for expr in expressions if expr.strip()]

        # Transform expressions
        transformed_expressions = []
        for expr in expressions:
            transformed_expr = transform_equivalent(expr)
            if transformed_expr is not None:
                transformed_expressions.append(transformed_expr)

        # Write transformed expressions to output file
        with open(output_file_path, 'w', encoding='utf-8') as output_file:
            for expr in transformed_expressions:
                output_file.write(expr + '\n')  # Ensure each expression is on a new line

        print(f"Transformed expressions written to {output_file_path}.")
    except Exception as e:
        print(f"An error occurred: {e}")  # Print any exceptions that occur


# ##########################################################################


def transform_implies(expression):
    # Define the regular expression pattern
    pattern = re.compile(r'implies\(([^,]+),\s*([^)]+)\)')

    # Recursively transform implies expressions
    while re.search(pattern, expression):
        expression = re.sub(pattern, r'(\1 implies \2)', expression)

    return expression

def transform_implies_in_file(file_path, output_file_path):
    try:
        # Read expressions from input file
        with open(file_path, 'r', encoding='utf-8') as input_file:
            expressions = input_file.readlines()

        # Transform expressions
        transformed_expressions = [transform_implies(expr.strip()) for expr in expressions]

        # Write transformed expressions to output file
        with open(output_file_path, 'w', encoding='utf-8') as output_file:
            for expr in transformed_expressions:
                output_file.write(expr + '\n')  # Ensure each expression is on a new line

        print(f"Transformed expressions written to {output_file_path}.")
    except Exception as e:
        print(f"An error occurred: {e}")  # Print any exceptions that occur






###################################################################################
def process_input_directories(input_dir, output_dir):
    # Check if output directory exists, if not, create it
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    # Iterate over subdirectories in the input directory
    for subdir in os.listdir(input_dir):
        input_subdir = os.path.join(input_dir, subdir)
        output_subdir = os.path.join(output_dir, subdir)
        
        # Check if the path is a directory
        if os.path.isdir(input_subdir):
            # Process files in the current subdirectory
            process_files_in_directory(input_subdir, output_subdir)

# Function to process files in a directory
def process_files_in_directory(input_subdir, output_subdir):
    # Check if output subdirectory exists, if not, create it
    if not os.path.exists(output_subdir):
        os.makedirs(output_subdir)

    # Iterate over files in the input subdirectory
    for file_name in os.listdir(input_subdir):
        if file_name.endswith(".txt"):  # Filter only text files
            input_file_path = os.path.join(input_subdir, file_name)
            output_file_path = os.path.join(output_subdir, file_name)

            # Process input file
            process_file(file_path, output_file_path)

# Function to process a single input file
def process_file(file_path, output_file_path):
    # Your existing code here to perform transformations and write to output file
    # For example:
    file_content = read_text_file(file_path)
        
#########################################################        

if __name__ == "__main__":
   
    input_files = ["input_file.txt", "input1_file.txt", "input2_file.txt"]

    # Define the input and output directories using raw string literals
    input_directory = r"C:\Users\vardn\OneDrive\Desktop\python1"
    output_directory = r"C:\Users\vardn\OneDrive\Desktop\python1"

    for input_file_name in input_files:
        input_file_path = os.path.join(input_directory, input_file_name)
        
        # Create output file name by adding a prefix or suffix to the input file name
        output_file_name = "output_" + input_file_name  # For example, adding "output_" prefix
        output_file_path = os.path.join(output_directory, output_file_name)

        if not input_file_path.endswith(input_file_name):
            print(f"Error: The entered file path does not end with '{input_file_name}'.")
        else:
            file_content = read_text_file(input_file_path)

        if file_content is not None:

            print(file_content)

            # Replace "~" with "not"
            modified_content = file_content.replace('&', 'and')
            
            # Replace "&" with "and"
            modified_content = file_content.replace('~', 'not')
            
            # Replace "|" with "or"
            modified_content = modified_content.replace('|', 'or')
            
            # Replace "->" with "implies"
            modified_content = modified_content.replace('->', 'implies')
            
            # Write the modified content back to the output file
           
            
            # Write the modified content back to the output file
            write_text_file(output_file_path, modified_content)     
            
            
            # Transform equivalent expressions in the file
            transform_equivalent_in_file(output_file_path, output_file_path)

            # Transform implies expressions in the file
            transform_implies_in_file(output_file_path, output_file_path)

            # Delete specified words from the file
            words_to_delete = ['cnf', 'is_a_theorem', 'condensed_detachment', 'axiom', 'xcb']
            delete_words_in_file(output_file_path, output_file_path, words_to_delete)

            # Process input directories recursively
            process_input_directories(input_directory, output_directory)
            
            
            
            
            
            
            
            
            
            


            

       

