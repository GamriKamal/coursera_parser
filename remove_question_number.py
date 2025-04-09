import re

def remove_question_numbers(input_file, output_file):
    with open(input_file, 'r', encoding='utf-8') as file:
        lines = file.readlines()

    cleaned_lines = []
    pattern = re.compile(r'<Question>\d+\.(.*)')

    for line in lines:
        line = re.sub(pattern, r'<Question>\1', line)
        cleaned_lines.append(line)

    with open(output_file, 'w', encoding='utf-8') as file:
        file.writelines(cleaned_lines)

input_filename = 'input.txt' 
output_filename = 'output.txt'
remove_question_numbers(input_filename, output_filename)