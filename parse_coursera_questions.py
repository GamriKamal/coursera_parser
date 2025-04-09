from bs4 import BeautifulSoup
import os

def load_counter(filename):
    if os.path.exists(filename):
        with open(filename, 'r', encoding='utf-8') as file:
            value = file.read().strip()
            if value.isdigit():
                return int(value)
    return 0

def save_counter(filename, counter):
    with open(filename, 'w', encoding='utf-8') as file:
        file.write(str(counter))

def parse_html_content(html_content, start_counter):
    soup = BeautifulSoup(html_content, 'html.parser')
    questions_divs = soup.find_all('div', id=lambda x: x and x.startswith('prompt-autoGradableResponseId~'))
    parsed_data = []

    counter = start_counter

    for question_div in questions_divs:
        counter += 1
        question_number = str(counter)

        question_text_container = question_div.find('div', class_='rc-CML')
        question_text = question_text_container.get_text(strip=True) if question_text_container else '???'

        question_wrapper = question_div.find_parent('div', class_='css-1i6fgnf')
        if not question_wrapper:
            continue

        options_divs = question_wrapper.find_all('div', class_='css-1f00xev')
        options = []

        for option_div in options_divs:
            label = option_div.find('label', class_='cui-Checkbox')
            if not label:
                continue

            classes = label.get('class', [])
            is_correct = 'cui-isChecked' in classes

            text_container = label.find('span', class_='_bc4egv')
            if not text_container:
                continue

            option_text = text_container.get_text(strip=True)

            if is_correct:
                options.append(f"<TrueVariant>{option_text}</TrueVariant>")
            else:
                options.append(f"<Variant>{option_text}</Variant>")

        parsed_data.append({
            'number': question_number,
            'question': question_text,
            'options': options
        })

    return parsed_data, counter

def save_to_txt(parsed_data, filename):
    file_exists = os.path.exists(filename)

    with open(filename, 'a', encoding='utf-8') as f:
        if file_exists:
            f.write("\n")

        for question in parsed_data:
            f.write(f"<Question>{question['number']}.{question['question']}</Question>\n")
            for option in question['options']:
                f.write(f"{option}\n")
            f.write("\n")

if __name__ == "__main__":
    counter_file = "counter.txt"
    
    current_counter = load_counter(counter_file)
    print(f"Current counter: {current_counter}")
    
    with open('input.txt', 'r', encoding='utf-8') as file:
        html_content = file.read()

    parsed_data, new_counter = parse_html_content(html_content, current_counter)
    
    save_to_txt(parsed_data, 'output.txt')
    save_counter(counter_file, new_counter)
    
    print("Parsing complete. Results saved to output.txt.")
    print(f"New counter: {new_counter}")
