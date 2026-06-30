/**
 * Quiz functionality for interactive QCM
 */

function checkQuiz(quizId) {
  const data = window.quizData[quizId];
  if (!data || !data.questions) {
    console.error('Quiz data not found for:', quizId);
    return;
  }

  let score = 0;
  let total = data.questions.length;
  const explanations = [];

  data.questions.forEach((q, index) => {
    const questionDiv = document.querySelector(`[data-qid="${q.id}"]`);
    if (!questionDiv) return;

    let correct = false;
    let userAnswer = '';

    if (q.type === 'number') {
      const input = document.querySelector(`[name="q${q.id}"]`);
      if (input && input.value !== '') {
        const val = parseFloat(input.value);
        userAnswer = val.toString();
        correct = Math.abs(val - q.answer) <= (q.tolerance || 0);
      }
    } else if (q.type === 'text') {
      const input = document.querySelector(`[name="q${q.id}"]`);
      if (input && input.value.trim() !== '') {
        userAnswer = input.value.trim();
        const expectedAnswer = q.answer.trim();
        if (q.case_sensitive) {
          correct = userAnswer === expectedAnswer;
        } else {
          correct = userAnswer.toLowerCase() === expectedAnswer.toLowerCase();
        }
      }
    } else if (q.type === 'single') {
      const checked = document.querySelector(`[name="q${q.id}"]:checked`);
      if (checked) {
        userAnswer = checked.value;
        correct = parseInt(checked.value) === q.answer;
      }
    } else if (q.type === 'multiple') {
      const checked = document.querySelectorAll(`[name="q${q.id}"]:checked`);
      const selected = Array.from(checked).map(c => parseInt(c.value)).sort((a, b) => a - b);
      userAnswer = selected.join(',');
      const expectedAnswers = (q.answers || []).slice().sort((a, b) => a - b);
      correct = JSON.stringify(selected) === JSON.stringify(expectedAnswers);
    }

    // Update visual feedback
    questionDiv.classList.remove('correct', 'incorrect');
    questionDiv.classList.add(correct ? 'correct' : 'incorrect');

    if (correct) {
      score++;
    }

    // Collect explanation if available
    if (q.explanation) {
      explanations.push({
        num: index + 1,
        correct: correct,
        explanation: q.explanation
      });
    }
  });

  // Display result
  const percentage = Math.round((score / total) * 100);
  let resultClass = 'result-poor';
  let emoji = '😕';
  
  if (percentage >= 80) {
    resultClass = 'result-excellent';
    emoji = '🎉';
  } else if (percentage >= 60) {
    resultClass = 'result-good';
    emoji = '👍';
  } else if (percentage >= 40) {
    resultClass = 'result-average';
    emoji = '📚';
  }

  const resultDiv = document.getElementById(`result-${quizId}`);
  resultDiv.innerHTML = `
    <div class="result-box ${resultClass}">
      <span class="result-emoji">${emoji}</span>
      <span class="result-score">Score : ${score}/${total} (${percentage}%)</span>
      <span class="result-message">${getResultMessage(percentage)}</span>
    </div>
  `;
  resultDiv.style.display = 'block';

  // Display explanations
  if (explanations.length > 0) {
    const explDiv = document.getElementById(`explanations-${quizId}`);
    let explHtml = '<h4>Explications</h4>';
    explanations.forEach(e => {
      const icon = e.correct ? '✓' : '✗';
      const cls = e.correct ? 'expl-correct' : 'expl-incorrect';
      explHtml += `
        <div class="explanation-item ${cls}">
          <strong>${icon} Question ${e.num} :</strong> ${e.explanation}
        </div>
      `;
    });
    explDiv.innerHTML = explHtml;
    explDiv.style.display = 'block';
  }

  // Scroll to results
  resultDiv.scrollIntoView({ behavior: 'smooth', block: 'nearest' });
}

function getResultMessage(percentage) {
  if (percentage >= 90) return 'Excellent ! Vous maîtrisez parfaitement ce sujet !';
  if (percentage >= 80) return 'Très bien ! Continuez comme ça !';
  if (percentage >= 60) return 'Bien ! Quelques révisions seraient utiles.';
  if (percentage >= 40) return 'Des efforts supplémentaires sont nécessaires.';
  return 'Revoyez le cours et réessayez !';
}

function resetQuiz(quizId) {
  // Reset all inputs
  const form = document.getElementById(`quiz-form-${quizId}`);
  if (form) {
    form.reset();
  }

  // Remove visual feedback
  const questions = document.querySelectorAll(`#quiz-${quizId} .quiz-question`);
  questions.forEach(q => {
    q.classList.remove('correct', 'incorrect');
  });

  // Hide results and explanations
  const resultDiv = document.getElementById(`result-${quizId}`);
  if (resultDiv) {
    resultDiv.style.display = 'none';
    resultDiv.innerHTML = '';
  }

  const explDiv = document.getElementById(`explanations-${quizId}`);
  if (explDiv) {
    explDiv.style.display = 'none';
    explDiv.innerHTML = '';
  }

  // Scroll to top of quiz
  const quizContainer = document.getElementById(`quiz-${quizId}`);
  if (quizContainer) {
    quizContainer.scrollIntoView({ behavior: 'smooth', block: 'start' });
  }
}

// Initialize quizzes on page load
document.addEventListener('DOMContentLoaded', function() {
  // Add keyboard support for form submission
  document.querySelectorAll('.quiz-container form').forEach(form => {
    form.addEventListener('keypress', function(e) {
      if (e.key === 'Enter' && e.target.tagName !== 'TEXTAREA') {
        e.preventDefault();
        const quizId = this.id.replace('quiz-form-', '');
        checkQuiz(quizId);
      }
    });
  });
});
