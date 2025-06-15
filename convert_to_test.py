import re
from pathlib import Path

def parse_latex_to_html(latex_file):
    with open(latex_file, 'r', encoding='utf-8') as f:
        content = f.read()

    # Extract main enumerate block for questions
    main_enumerate_pattern = re.compile(
        r'\\begin{enumerate}\[label=\\arabic\*\.?\](.*?)\\section\*{Answer Sheet}',
        re.DOTALL
    )
    main_enumerate_match = main_enumerate_pattern.search(content)
    if not main_enumerate_match:
        raise ValueError("Could not find the main enumerate environment containing questions")

    question_block = main_enumerate_match.group(1)

    # Find all questions with their options
    question_pattern = re.compile(
        r'\\item\s*(.*?)\s*\\begin{enumerate}\[label=\(\\alph\*\)\](.*?)\\end{enumerate}',
        re.DOTALL
    )

    questions = []
    for qmatch in question_pattern.finditer(question_block):
        question_text = qmatch.group(1).strip().replace('\n', ' ')
        options_block = qmatch.group(2)

        # Extract individual options
        option_pattern = re.compile(r'\\item\s*(.*?)(?=\\item|$)', re.DOTALL)
        options = [opt.strip().replace('\n', ' ') for opt in option_pattern.findall(options_block)]

        questions.append({
            'text': question_text,
            'options': options
        })

    # Extract answers
    answer_section_pattern = re.compile(
        r'\\section\*{Answer Sheet}(.*?)\\end{enumerate}',
        re.DOTALL
    )
    answer_section = answer_section_pattern.search(content)
    answers = []

    if answer_section:
        answer_block = answer_section.group(1)
        answer_lines = answer_block.split('\n')
        for line in answer_lines:
            line = line.strip()
            if line.startswith(r'\item'):
                answer_match = re.match(r'\\item\s*([a-z])', line)
                if answer_match:
                    answers.append(answer_match.group(1).lower())

    return questions, answers

def generate_html(questions, answers, output_file):
    html = f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Interactive MCQ Test</title>
    <style>
        body {{
            font-family: Arial, sans-serif;
            line-height: 1.6;
            max-width: 800px;
            margin: 0 auto;
            padding: 20px;
        }}
        .instructions {{
            background-color: #f8f8f8;
            padding: 15px;
            border-radius: 5px;
            margin-bottom: 20px;
        }}
        .question {{
            margin-bottom: 20px;
            padding: 15px;
            border: 1px solid #ddd;
            border-radius: 5px;
        }}
        .options {{
            margin-left: 20px;
        }}
        .option {{
            margin: 5px 0;
        }}
        label {{
            cursor: pointer;
        }}
        button {{
            margin-top: 20px;
            padding: 10px 15px;
            background-color: #4CAF50;
            color: white;
            border: none;
            border-radius: 4px;
            cursor: pointer;
            font-size: 16px;
        }}
        button:hover {{
            background-color: #45a049;
        }}
        .results {{
            margin-top: 30px;
            padding: 15px;
            background-color: #f8f8f8;
            border-radius: 5px;
        }}
        .correct {{
            color: green;
        }}
        .incorrect {{
            color: red;
        }}
        .score {{
            font-size: 18px;
            font-weight: bold;
            margin-bottom: 15px;
        }}
    </style>
</head>
<body>
    <h1>Interactive MCQ Test</h1>
    
    <div class="instructions">
        <h2>Instructions</h2>
        <p>This is a multiple-choice practice test. For each question, select the best answer from the given options (a), (b), (c), or (d).</p>
    </div>
    
    <form id="quizForm">
"""

    for i, question in enumerate(questions):
        html += f"""
        <div class="question">
            <p><strong>Question {i+1}:</strong> {question['text']}</p>
            <div class="options">
        """
        
        for j, option in enumerate(question['options']):
            letter = chr(97 + j)  # a, b, c, etc.
            html += f"""
                <div class="option">
                    <input type="radio" id="q{i+1}_{letter}" name="q{i+1}" value="{letter}">
                    <label for="q{i+1}_{letter}">({letter}) {option}</label>
                </div>
            """
        
        html += """
            </div>
        </div>
        """

    html += f"""
        <button type="button" onclick="checkAnswers()">Submit Answers</button>
    </form>
    
    <div id="results" class="results" style="display: none;">
        <h2>Results</h2>
        <p id="score" class="score"></p>
        <div id="answerDetails"></div>
    </div>
    
    <script>
        const correctAnswers = {answers};
        
        function checkAnswers() {{
            let score = 0;
            let answerDetails = '';
            
            for (let i = 0; i < {len(questions)}; i++) {{
                const questionNum = i + 1;
                const selectedOption = document.querySelector(`input[name="q${{questionNum}}"]:checked`);
                
                if (selectedOption) {{
                    const userAnswer = selectedOption.value;
                    const isCorrect = userAnswer === correctAnswers[i];
                    
                    if (isCorrect) {{
                        score++;
                        answerDetails += `<p class="correct">Question ${{questionNum}}: Correct!</p>`;
                    }} else {{
                        answerDetails += `<p class="incorrect">Question ${{questionNum}}: Incorrect. The correct answer is ${{correctAnswers[i].toUpperCase()}}.</p>`;
                    }}
                }} else {{
                    answerDetails += `<p class="incorrect">Question ${{questionNum}}: Not answered. The correct answer is ${{correctAnswers[i].toUpperCase()}}.</p>`;
                }}
            }}
            
            const percentage = Math.round((score / {len(questions)}) * 100);
            document.getElementById('score').innerHTML = `Score: ${{score}}/${{ {len(questions)} }} (${{percentage}}%)`;
            document.getElementById('answerDetails').innerHTML = answerDetails;
            document.getElementById('results').style.display = 'block';
            
            // Scroll to results
            document.getElementById('results').scrollIntoView({{ behavior: 'smooth' }});
        }}
    </script>
</body>
</html>
"""

    with open(output_file, 'w', encoding='utf-8') as f:
        f.write(html)

def main():
    latex_file = input('Enter path to the LaTeX file: ')
    output_file = input('Enter path for the output HTML file: ')
    
    try:
        questions, answers = parse_latex_to_html(latex_file)
        
        if len(questions) != len(answers):
            print(f"Warning: Number of questions ({len(questions)}) doesn't match number of answers ({len(answers)})")
        
        generate_html(questions, answers, output_file)
        print(f"Successfully generated interactive test: {output_file}")
    except Exception as e:
        print(f"An error occurred: {str(e)}")

if __name__ == "__main__":
    main()