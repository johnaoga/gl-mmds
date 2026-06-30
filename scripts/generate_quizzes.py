#!/usr/bin/env python3
"""
Generate interactive quiz pages from GitHub Issues.

This script:
1. Fetches issues with the 'quiz' label from the GitHub repository
2. Parses the issue body to extract quiz questions
3. Generates RST files with embedded HTML/JS for interactive quizzes
"""
import os
import re
import json
import html
from pathlib import Path
from collections import defaultdict

try:
    import requests
except ImportError:
    requests = None


def parse_issue_body(body: str) -> dict:
    """Parse the GitHub issue body to extract question data."""
    data = {}
    
    # Pattern to match ### Header\n\nContent or ### Header\nContent
    sections = re.split(r'\n### ', body)
    
    for section in sections:
        if not section.strip():
            continue
        
        lines = section.strip().split('\n', 1)
        if len(lines) < 2:
            continue
        
        header = lines[0].strip().lower()
        content = lines[1].strip() if len(lines) > 1 else ""
        
        # Remove "No response" or empty markers
        if content.lower() in ['no response', '_no response_', 'none']:
            content = ""
        
        if 'quiz id' in header:
            data['quiz_id'] = content.strip()
        elif 'question type' in header:
            # Extract type from format like "number (numeric answer)"
            match = re.match(r'(\w+)', content)
            data['type'] = match.group(1) if match else content.strip()
        elif 'question' in header and 'type' not in header:
            data['question'] = content.strip()
        elif 'options' in header:
            if content:
                data['options'] = [opt.strip() for opt in content.strip().split('\n') if opt.strip()]
        elif 'answer' in header and 'case' not in header:
            data['answer'] = content.strip()
        elif 'tolerance' in header:
            data['tolerance'] = float(content) if content else 0
        elif 'case sensitive' in header:
            data['case_sensitive'] = content.strip().lower() == 'true'
        elif 'explanation' in header:
            data['explanation'] = content.strip()
    
    return data


def fetch_issues_from_github(repo: str, token: str = None) -> list:
    """Fetch issues with 'quiz' label from GitHub API."""
    if requests is None:
        print("Warning: requests library not available, skipping GitHub fetch")
        return []
    
    headers = {'Accept': 'application/vnd.github.v3+json'}
    if token:
        headers['Authorization'] = f'Bearer {token}'
    
    url = f'https://api.github.com/repos/{repo}/issues'
    params = {'labels': 'quiz', 'state': 'open', 'per_page': 100}
    
    print(f"  API URL: {url}")
    print(f"  Token provided: {'yes' if token else 'no'}")
    
    all_issues = []
    page = 1
    
    while True:
        params['page'] = page
        try:
            response = requests.get(url, headers=headers, params=params, timeout=30)
            
            if response.status_code != 200:
                print(f"Warning: GitHub API returned {response.status_code}")
                print(f"  Response: {response.text[:500]}")
                break
            
            issues = response.json()
            if not issues:
                break
            
            all_issues.extend(issues)
            print(f"  Fetched {len(issues)} issues from page {page}")
            page += 1
        except Exception as e:
            print(f"Warning: GitHub API request failed: {e}")
            break
    
    return all_issues


def load_issues_from_files(issues_dir: Path) -> list:
    """Load issues from local markdown files (for testing/backup)."""
    issues = []
    
    if not issues_dir.exists():
        return issues
    
    for md_file in issues_dir.glob("*.md"):
        with open(md_file, 'r', encoding='utf-8') as f:
            content = f.read()
        
        issues.append({
            'number': int(md_file.stem.split('_')[0]) if md_file.stem[0].isdigit() else 0,
            'title': md_file.stem,
            'body': content
        })
    
    return issues


def escape_html(text: str) -> str:
    """Escape HTML special characters."""
    return html.escape(text)


def format_code_for_html(code: str, lang: str) -> str:
    """Format code block for HTML, preserving indentation and newlines."""
    # Escape HTML special characters
    code_escaped = html.escape(code.strip())
    # Preserve indentation: convert leading spaces to &nbsp;
    lines = code_escaped.split('\n')
    formatted_lines = []
    for line in lines:
        # Count leading spaces and convert to &nbsp;
        stripped = line.lstrip(' ')
        indent_count = len(line) - len(stripped)
        indent = '&nbsp;' * indent_count
        formatted_lines.append(indent + stripped)
    # Join with <br> for line breaks
    code_html = '<br>'.join(formatted_lines)
    return f'<pre><code class="language-{lang}">{code_html}</code></pre>'


def markdown_to_html(text: str) -> str:
    """Convert markdown to HTML, handling code blocks and newlines."""
    # Handle fenced code blocks (```language ... ```)
    def replace_code_block(match):
        lang = match.group(1) or ''
        code = match.group(2)
        return format_code_for_html(code, lang)
    
    text = re.sub(r'```(\w*)\n?(.*?)```', replace_code_block, text, flags=re.DOTALL)
    
    # Handle {python}, {cpp}, {r} style code blocks
    def replace_brace_code(match):
        lang = match.group(1) or ''
        code = match.group(2)
        return format_code_for_html(code, lang)
    
    text = re.sub(r'\{(\w+)\}\n(.*?)(?=\n\n|$)', replace_brace_code, text, flags=re.DOTALL)
    
    # Convert inline code (single backticks)
    text = re.sub(r'`([^`]+)`', r'<code>\1</code>', text)
    # Convert bold
    text = re.sub(r'\*\*([^*]+)\*\*', r'<strong>\1</strong>', text)
    # Convert italic  
    text = re.sub(r'\*([^*]+)\*', r'<em>\1</em>', text)
    # Convert remaining newlines to <br> for HTML display
    text = text.replace('\n', '<br>')
    return text


def generate_question_html(qid: str, qnum: int, question: dict) -> tuple:
    """Generate HTML for a single question and return (html, answer_data)."""
    qtype = question['type']
    # Don't escape first - let markdown_to_html handle code blocks properly
    q_text = markdown_to_html(question['question'])
    
    answer_data = {'id': qid, 'type': qtype}
    
    if qtype == 'number':
        html_content = f'''
        <div class="quiz-question" data-qid="{qid}">
          <p class="question-text"><strong>Q{qnum}.</strong> {q_text}</p>
          <input type="number" step="any" name="q{qid}" class="quiz-input" placeholder="Votre réponse..." />
        </div>
        '''
        answer_data['answer'] = float(question['answer'])
        answer_data['tolerance'] = question.get('tolerance', 0)
        
    elif qtype == 'text':
        html_content = f'''
        <div class="quiz-question" data-qid="{qid}">
          <p class="question-text"><strong>Q{qnum}.</strong> {q_text}</p>
          <input type="text" name="q{qid}" class="quiz-input" placeholder="Votre réponse..." />
        </div>
        '''
        answer_data['answer'] = question['answer']
        answer_data['case_sensitive'] = question.get('case_sensitive', False)
        
    elif qtype == 'single':
        options_html = ""
        for i, opt in enumerate(question.get('options', [])):
            opt_escaped = markdown_to_html(escape_html(opt))
            options_html += f'''
            <label class="quiz-option">
              <input type="radio" name="q{qid}" value="{i}" />
              <span>{opt_escaped}</span>
            </label>
            '''
        
        html_content = f'''
        <div class="quiz-question" data-qid="{qid}">
          <p class="question-text"><strong>Q{qnum}.</strong> {q_text}</p>
          <div class="quiz-options">{options_html}</div>
        </div>
        '''
        answer_data['answer'] = int(question['answer'])
        
    elif qtype == 'multiple':
        options_html = ""
        for i, opt in enumerate(question.get('options', [])):
            opt_escaped = markdown_to_html(escape_html(opt))
            options_html += f'''
            <label class="quiz-option">
              <input type="checkbox" name="q{qid}" value="{i}" />
              <span>{opt_escaped}</span>
            </label>
            '''
        
        html_content = f'''
        <div class="quiz-question" data-qid="{qid}">
          <p class="question-text"><strong>Q{qnum}.</strong> {q_text}</p>
          <p class="question-hint"><em>(Plusieurs réponses possibles)</em></p>
          <div class="quiz-options">{options_html}</div>
        </div>
        '''
        # Parse comma-separated indices
        answers = [int(x.strip()) for x in question['answer'].split(',')]
        answer_data['answers'] = answers
    
    else:
        html_content = f'<div class="quiz-question">Unknown question type: {qtype}</div>'
    
    # Add explanation if present
    if question.get('explanation'):
        expl = markdown_to_html(escape_html(question['explanation']))
        answer_data['explanation'] = question['explanation']
    
    return html_content, answer_data


QUIZ_TITLES = {
    'quiz1_bigdata_mapreduce': 'Quiz 1 : Big Data (5V) & MapReduce',
    'quiz2_reco_fim': 'Quiz 2 : Recommandation & Frequent Itemset Mining',
    'quiz3_lsh_graphes': 'Quiz 3 : Similarité (LSH), graphes & PageRank',
}


def indent_html(html_str: str, spaces: int = 3) -> str:
    """Indent all lines of HTML for RST raw directive."""
    indent = ' ' * spaces
    lines = html_str.strip().split('\n')
    return '\n'.join(indent + line for line in lines)


def generate_quiz_rst(quiz_id: str, questions: list) -> str:
    """Generate RST content for a quiz."""
    title = QUIZ_TITLES.get(quiz_id, quiz_id.replace('_', ' ').title())
    
    questions_html_parts = []
    quiz_data = {"questions": []}
    
    for i, q in enumerate(questions):
        qid = f"{quiz_id}_{i}"
        q_html, answer_data = generate_question_html(qid, i + 1, q)
        # Normalize the HTML - remove extra whitespace/newlines and make single line per question
        q_html_clean = ' '.join(q_html.split())
        questions_html_parts.append(q_html_clean)
        quiz_data['questions'].append(answer_data)
    
    questions_html = '\n'.join(questions_html_parts)
    
    # Generate underline for title
    title_underline = '=' * len(title)
    
    # Build the HTML as a single block, then indent for RST
    html_block = f'''<div class="quiz-container" id="quiz-{quiz_id}">
<form id="quiz-form-{quiz_id}" onsubmit="return false;">
{questions_html}
</form>
<div class="quiz-actions">
<button type="button" class="quiz-btn quiz-btn-check" onclick="checkQuiz('{quiz_id}')">✓ Vérifier mes réponses</button>
<button type="button" class="quiz-btn quiz-btn-reset" onclick="resetQuiz('{quiz_id}')">↺ Recommencer</button>
</div>
<div id="result-{quiz_id}" class="quiz-result"></div>
<div id="explanations-{quiz_id}" class="quiz-explanations"></div>
</div>
<script>
if (typeof window.quizData === 'undefined') window.quizData = {{}};
window.quizData['{quiz_id}'] = {json.dumps(quiz_data, ensure_ascii=False)};
</script>'''
    
    indented_html = indent_html(html_block)
    
    rst_content = f'''{title}
{title_underline}

.. raw:: html

{indented_html}

'''
    return rst_content


def main():
    # Configuration
    repo = os.environ.get('GITHUB_REPOSITORY', 'johnaoga/gl-mmds')
    token = os.environ.get('GITHUB_TOKEN', '')
    
    project_root = Path(__file__).parent.parent
    output_dir = project_root / 'docs' / 'source' / 'part6' / 'quizzes'
    issues_dir = project_root / 'docs' / 'source' / 'part6' / 'quiz_issues'
    
    output_dir.mkdir(parents=True, exist_ok=True)
    
    # Collect questions by quiz_id
    quizzes = defaultdict(list)
    
    # Try to fetch from GitHub first
    print(f"Fetching quiz issues from {repo}...")
    issues = fetch_issues_from_github(repo, token)
    print(f"Found {len(issues)} issues from GitHub")
    
    # Also load from local files as backup/testing
    local_issues = load_issues_from_files(issues_dir)
    print(f"Found {len(local_issues)} local issue files")
    issues.extend(local_issues)
    
    # Parse all issues
    for issue in issues:
        body = issue.get('body', '')
        if not body:
            continue
        
        try:
            question_data = parse_issue_body(body)
            quiz_id = question_data.get('quiz_id', '').strip()
            
            if quiz_id and question_data.get('question') and question_data.get('type'):
                question_data['issue_number'] = issue.get('number', 0)
                quizzes[quiz_id].append(question_data)
                print(f"  Added question to {quiz_id} from issue #{issue.get('number', 'local')}")
        except Exception as e:
            print(f"  Warning: Failed to parse issue #{issue.get('number', '?')}: {e}")
    
    # Generate RST files for each quiz
    for quiz_id, questions in quizzes.items():
        # Sort by issue number for consistent ordering
        questions.sort(key=lambda x: x.get('issue_number', 0))
        
        rst_content = generate_quiz_rst(quiz_id, questions)
        output_file = output_dir / f"{quiz_id}.rst"
        output_file.write_text(rst_content, encoding='utf-8')
        print(f"Generated: {output_file} ({len(questions)} questions)")
    
    # Generate index for part6 if quizzes were created
    if quizzes:
        generate_part6_index(output_dir.parent, list(quizzes.keys()))
    
    print(f"\nDone! Generated {len(quizzes)} quiz files.")


def generate_part6_index(part6_dir: Path, quiz_ids: list):
    """Update the part6 index.rst toctree with generated quizzes."""
    index_file = part6_dir / 'index.rst'
    
    # Sort quiz IDs
    quiz_ids = sorted(quiz_ids)
    toctree_entries = '\n   '.join([f'quizzes/{qid}' for qid in quiz_ids])
    
    # If index exists, update only the toctree section
    if index_file.exists():
        content = index_file.read_text(encoding='utf-8')
        # Find and replace the toctree content
        pattern = r'(.. toctree::\n   :maxdepth: 1\n\n)(   quizzes/[^\n]+\n?)+'
        replacement = f'\\1   {toctree_entries}\n'
        new_content, count = re.subn(pattern, replacement, content)
        if count > 0:
            index_file.write_text(new_content, encoding='utf-8')
            print(f"Updated toctree in: {index_file}")
        else:
            print(f"Warning: Could not find toctree to update in {index_file}")
        return
    
    # Create new index if it doesn't exist
    content = f'''.. _part6:

*************************************************************************************************
QCM - Questionnaires d'auto-évaluation
*************************************************************************************************

Vue d'ensemble
==============

Cette partie contient des questionnaires à choix multiples (QCM) pour vous auto-évaluer
sur les concepts vus dans ce cours. Chaque quiz est interactif : vous pouvez vérifier
vos réponses immédiatement et voir les explications.

**Types de questions :**

- **Numériques** : Entrez un nombre comme réponse
- **Texte court** : Entrez un mot ou une courte phrase
- **Choix unique** : Sélectionnez une seule bonne réponse
- **Choix multiples** : Sélectionnez toutes les bonnes réponses

.. tip::
   Ces quiz sont conçus pour l'auto-évaluation. N'hésitez pas à les refaire
   plusieurs fois pour consolider vos connaissances !


Quizzes disponibles
===================

.. toctree::
   :maxdepth: 1

   {toctree_entries}

'''
    
    index_file.write_text(content, encoding='utf-8')
    print(f"Generated: {index_file}")


if __name__ == "__main__":
    main()
