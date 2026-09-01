#!/usr/bin/env python3
"""Build interactive Mock Exam HTMLs with 130-min timer and domain score breakdown"""

import sys
import os
import re
import json

def parse_mock_md(md_path):
    with open(md_path, 'r', encoding='utf-8') as f:
        text = f.read()

    # Split into questions and answers
    ans_split = re.split(r"#+\s*Answer Key\s*(?:&|and)?\s*Explanations?", text, flags=re.I)
    if len(ans_split) < 2:
        raise ValueError(f"Could not split Answer Key & Explanations in {md_path}")

    q_text, a_text = ans_split[0], ans_split[1]

    # Parse answers
    ans_dict = {}
    for line in a_text.strip().split("\n"):
        line = line.strip()
        if not line:
            continue
        m = re.match(r"^(\d+)\.\s+([A-E](?:\s*(?:,|&|and)\s*[A-E])*)\s*[—\-–:]\s*(.*)$", line)
        if m:
            qnum = int(m.group(1))
            letters_raw = m.group(2)
            exp = m.group(3).strip()
            letters = re.findall(r"[A-E]", letters_raw)
            ans_indices = [ord(ch) - 65 for ch in letters]
            ans_dict[qnum] = (ans_indices, exp)

    # Parse questions
    q_items = []
    q_raw_blocks = re.split(r"\n(?=\d+\.\s+)", "\n" + q_text)

    for b in q_raw_blocks:
        b = b.strip()
        if not b:
            continue
        m = re.match(r"^(\d+)\.\s+(.*)", b, re.DOTALL)
        if not m:
            continue
        qnum = int(m.group(1))
        body = m.group(2).strip()

        # Split into question text and options
        lines = body.split("\n")
        stem_lines = []
        opt_lines = []
        for l in lines:
            l = l.strip()
            if not l:
                continue
            if re.match(r"^[A-E]\)", l):
                opt_lines.append(l)
            elif not opt_lines:
                stem_lines.append(l)
            else:
                opt_lines[-1] += " " + l

        stem = " ".join(stem_lines).strip()
        options = [re.sub(r"\s*---\s*$", "", re.sub(r"^[A-E]\)\s*", "", o)).strip() for o in opt_lines]

        if len(options) < 2:
            continue

        # Assign Domain based on question number (1-21: D1, 22-38: D2, 39-54: D3, 55-65: D4)
        if qnum <= 21:
            domain_id = 1
            domain_name = "Domain 1: Development with AWS Services (32%)"
        elif qnum <= 38:
            domain_id = 2
            domain_name = "Domain 2: Security (26%)"
        elif qnum <= 54:
            domain_id = 3
            domain_name = "Domain 3: Deployment (24%)"
        else:
            domain_id = 4
            domain_name = "Domain 4: Troubleshooting & Optimization (18%)"

        if qnum in ans_dict:
            a_indices, exp = ans_dict[qnum]
            is_multi = len(a_indices) > 1 or "(Select TWO)" in stem or "(Select THREE)" in stem
            q_items.append({
                "num": qnum,
                "q": stem,
                "o": options,
                "a": a_indices,
                "multi": is_multi,
                "e": exp,
                "d_id": domain_id,
                "d_name": domain_name
            })

    q_items.sort(key=lambda x: x["num"])
    return q_items

def generate_mock_html(title, eyebrow, storage_key, q_items):
    total_q = len(q_items)
    q_json = json.dumps(q_items, ensure_ascii=False)

    html_template = f"""<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>{title} — AWS Certified Developer Associate (DVA-C02)</title>
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&family=JetBrains+Mono:wght@400;500&display=swap" rel="stylesheet">
<style>
:root {{
  --bg-primary: #0a0e17;
  --bg-secondary: #111827;
  --bg-card: #1a2234;
  --bg-card-hover: #222d42;
  --border-color: #2a364f;
  --border-focus: #ff9900;
  --text-primary: #f1f5f9;
  --text-secondary: #94a3b8;
  --text-muted: #64748b;
  --accent-aws: #ff9900;
  --accent-aws-hover: #ec7211;
  --accent-blue: #38bdf8;
  --correct: #10b981;
  --correct-bg: rgba(16, 185, 129, 0.12);
  --incorrect: #ef4444;
  --incorrect-bg: rgba(239, 68, 68, 0.12);
  --flagged: #f59e0b;
  --flagged-bg: rgba(245, 158, 11, 0.15);
}}
* {{ box-sizing: border-box; margin: 0; padding: 0; }}
body {{
  font-family: 'Inter', system-ui, sans-serif;
  background-color: var(--bg-primary);
  color: var(--text-primary);
  line-height: 1.6;
  min-height: 100vh;
  display: flex;
  flex-direction: column;
}}
header {{
  background-color: var(--bg-secondary);
  border-bottom: 1px solid var(--border-color);
  padding: 0.875rem 1.5rem;
  position: sticky;
  top: 0;
  z-index: 50;
  display: flex;
  align-items: center;
  justify-content: space-between;
}}
.header-left {{ display: flex; align-items: center; gap: 1rem; }}
.eyebrow {{ font-size: 0.75rem; font-weight: 700; color: var(--accent-aws); text-transform: uppercase; letter-spacing: 0.08em; }}
h1 {{ font-size: 1.125rem; font-weight: 700; color: var(--text-primary); }}
.timer-box {{
  font-family: 'JetBrains Mono', monospace;
  font-size: 1.125rem;
  font-weight: 700;
  background: var(--bg-card);
  border: 1px solid var(--border-color);
  padding: 0.35rem 0.85rem;
  border-radius: 6px;
  color: var(--accent-blue);
  display: flex;
  align-items: center;
  gap: 0.5rem;
}}
.timer-warning {{ color: var(--flagged); border-color: var(--flagged); animation: pulse 1.5s infinite; }}
.timer-danger {{ color: var(--incorrect); border-color: var(--incorrect); animation: pulse 0.8s infinite; }}
@keyframes pulse {{ 0%, 100% {{ opacity: 1; }} 50% {{ opacity: 0.6; }} }}

.main-container {{
  display: grid;
  grid-template-columns: 1fr 320px;
  max-width: 1280px;
  margin: 0 auto;
  padding: 1.5rem;
  gap: 1.5rem;
  flex: 1;
  width: 100%;
}}
@media (max-width: 900px) {{
  .main-container {{ grid-template-columns: 1fr; }}
}}

.q-card {{
  background: var(--bg-secondary);
  border: 1px solid var(--border-color);
  border-radius: 10px;
  padding: 1.75rem;
  display: flex;
  flex-direction: column;
  gap: 1.25rem;
}}
.q-header {{
  display: flex;
  justify-content: space-between;
  align-items: center;
  border-bottom: 1px solid var(--border-color);
  padding-bottom: 0.75rem;
}}
.domain-badge {{
  font-size: 0.75rem;
  font-weight: 600;
  background: rgba(56, 189, 248, 0.12);
  color: var(--accent-blue);
  padding: 0.25rem 0.6rem;
  border-radius: 4px;
}}
.q-stem {{ font-size: 1.05rem; font-weight: 500; color: #f8fafc; line-height: 1.6; }}
.options-list {{ display: flex; flex-direction: column; gap: 0.75rem; }}
.option-item {{
  background: var(--bg-card);
  border: 1px solid var(--border-color);
  border-radius: 8px;
  padding: 0.875rem 1rem;
  cursor: pointer;
  transition: all 0.15s ease;
  display: flex;
  align-items: flex-start;
  gap: 0.75rem;
}}
.option-item:hover {{ background: var(--bg-card-hover); border-color: #475569; }}
.option-item.selected {{
  background: rgba(255, 153, 0, 0.12);
  border-color: var(--accent-aws);
}}
.opt-label {{
  font-weight: 700;
  color: var(--text-secondary);
  min-width: 1.5rem;
}}
.opt-text {{ color: var(--text-primary); font-size: 0.95rem; }}

.sidebar {{
  background: var(--bg-secondary);
  border: 1px solid var(--border-color);
  border-radius: 10px;
  padding: 1.25rem;
  height: fit-content;
  display: flex;
  flex-direction: column;
  gap: 1rem;
}}
.grid-title {{ font-size: 0.85rem; font-weight: 700; text-transform: uppercase; color: var(--text-muted); }}
.nav-grid {{
  display: grid;
  grid-template-columns: repeat(5, 1fr);
  gap: 0.4rem;
  max-height: 380px;
  overflow-y: auto;
}}
.nav-btn {{
  background: var(--bg-card);
  border: 1px solid var(--border-color);
  color: var(--text-secondary);
  font-size: 0.8rem;
  font-weight: 600;
  padding: 0.5rem 0;
  border-radius: 4px;
  cursor: pointer;
  transition: all 0.1s ease;
}}
.nav-btn:hover {{ border-color: var(--accent-aws); color: var(--text-primary); }}
.nav-btn.active {{ border-color: var(--accent-blue); background: rgba(56, 189, 248, 0.15); color: #fff; }}
.nav-btn.answered {{ background: #22384f; border-color: #38bdf8; color: #fff; }}
.nav-btn.flagged {{ border-color: var(--flagged); background: var(--flagged-bg); color: var(--flagged); }}

.action-bar {{
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding-top: 1rem;
  border-top: 1px solid var(--border-color);
}}
.btn {{
  padding: 0.6rem 1.25rem;
  border-radius: 6px;
  font-weight: 600;
  font-size: 0.9rem;
  cursor: pointer;
  border: none;
  transition: all 0.15s ease;
}}
.btn-primary {{ background: var(--accent-aws); color: #000; }}
.btn-primary:hover {{ background: var(--accent-aws-hover); }}
.btn-secondary {{ background: var(--bg-card); color: var(--text-primary); border: 1px solid var(--border-color); }}
.btn-secondary:hover {{ background: var(--bg-card-hover); }}
.btn-flag {{ background: transparent; color: var(--flagged); border: 1px solid var(--flagged); }}
.btn-flag.active {{ background: var(--flagged); color: #000; }}
.btn-finish {{ background: var(--correct); color: #000; width: 100%; }}
.btn-finish:hover {{ background: #059669; }}

/* Results Screen */
.results-card {{
  background: var(--bg-secondary);
  border: 1px solid var(--border-color);
  border-radius: 10px;
  padding: 2.5rem;
  max-width: 860px;
  margin: 2rem auto;
  display: flex;
  flex-direction: column;
  gap: 2rem;
}}
.score-banner {{
  text-align: center;
  padding: 2rem;
  background: var(--bg-card);
  border-radius: 8px;
  border: 1px solid var(--border-color);
}}
.scaled-score {{ font-size: 3rem; font-weight: 800; color: var(--accent-aws); }}
.pass-badge {{
  display: inline-block;
  padding: 0.35rem 1.25rem;
  border-radius: 20px;
  font-weight: 700;
  font-size: 0.9rem;
  text-transform: uppercase;
  margin-top: 0.75rem;
}}
.pass-badge.pass {{ background: var(--correct-bg); color: var(--correct); border: 1px solid var(--correct); }}
.pass-badge.fail {{ background: var(--incorrect-bg); color: var(--incorrect); border: 1px solid var(--incorrect); }}

.breakdown-table {{
  width: 100%;
  border-collapse: collapse;
}}
.breakdown-table th, .breakdown-table td {{
  padding: 0.875rem 1rem;
  border-bottom: 1px solid var(--border-color);
  text-align: left;
}}
.breakdown-table th {{ color: var(--text-muted); font-size: 0.8rem; text-transform: uppercase; }}
.review-item {{
  background: var(--bg-card);
  border: 1px solid var(--border-color);
  border-radius: 8px;
  padding: 1.5rem;
  margin-bottom: 1.25rem;
}}
.explanation-box {{
  margin-top: 1rem;
  padding: 1rem;
  background: rgba(15, 23, 42, 0.6);
  border-left: 3px solid var(--accent-blue);
  border-radius: 4px;
  font-size: 0.9rem;
}}
</style>
</head>
<body>

<header>
  <div class="header-left">
    <div>
      <div class="eyebrow">{eyebrow}</div>
      <h1>{title}</h1>
    </div>
  </div>
  <div id="timerDisplay" class="timer-box">⏳ 130:00</div>
</header>

<div id="examContainer" class="main-container">
  <main class="q-card">
    <div class="q-header">
      <span id="qNumber" style="font-weight:700; color:var(--text-secondary);">Question 1 of {total_q}</span>
      <span id="domainBadge" class="domain-badge">Domain 1</span>
    </div>
    <div id="qStem" class="q-stem"></div>
    <div id="optionsContainer" class="options-list"></div>
    <div class="action-bar">
      <button id="prevBtn" class="btn btn-secondary">Previous</button>
      <button id="flagBtn" class="btn btn-flag">🚩 Flag for Review</button>
      <button id="nextBtn" class="btn btn-primary">Next</button>
    </div>
  </main>

  <aside class="sidebar">
    <div class="grid-title">Question Navigator</div>
    <div id="navGrid" class="nav-grid"></div>
    <button id="finishExamBtn" class="btn btn-finish">Submit Exam</button>
  </aside>
</div>

<div id="resultsContainer" style="display:none; padding: 1.5rem;">
  <div class="results-card">
    <div class="score-banner">
      <div style="color:var(--text-muted); text-transform:uppercase; font-size:0.85rem; font-weight:700;">Scaled Score (Passing: 720)</div>
      <div id="scoreNumber" class="scaled-score">0</div>
      <div id="scoreSummary" style="color:var(--text-secondary); margin-top:0.25rem;">0 / 65 correct (0%)</div>
      <div id="passBadge" class="pass-badge">Pass</div>
    </div>

    <div>
      <h3 style="margin-bottom:1rem; font-size:1.1rem;">Domain Performance Breakdown</h3>
      <table class="breakdown-table">
        <thead>
          <tr>
            <th>Domain</th>
            <th>Weight</th>
            <th>Score</th>
            <th>Percentage</th>
          </tr>
        </thead>
        <tbody id="domainBreakdownBody"></tbody>
      </table>
    </div>

    <div>
      <h3 style="margin-bottom:1rem; font-size:1.1rem;">Question Review</h3>
      <div id="reviewList"></div>
    </div>
  </div>
</div>

<script>
const questions = {q_json};
let currentIndex = 0;
let userAnswers = {{}}; // qIndex -> [selected indices]
let flagged = new Set();
let timeLeft = 130 * 60; // 130 minutes in seconds
let timerInterval = null;
let examSubmitted = false;

function init() {{
  renderNavGrid();
  loadQuestion(0);
  startTimer();

  document.getElementById('prevBtn').onclick = () => {{ if (currentIndex > 0) loadQuestion(currentIndex - 1); }};
  document.getElementById('nextBtn').onclick = () => {{ if (currentIndex < questions.length - 1) loadQuestion(currentIndex + 1); }};
  document.getElementById('flagBtn').onclick = toggleFlag;
  document.getElementById('finishExamBtn').onclick = confirmSubmit;
}}

function startTimer() {{
  const display = document.getElementById('timerDisplay');
  timerInterval = setInterval(() => {{
    if (timeLeft <= 0) {{
      clearInterval(timerInterval);
      submitExam();
      return;
    }}
    timeLeft--;
    const mins = Math.floor(timeLeft / 60);
    const secs = timeLeft % 60;
    display.textContent = `⏳ ${{String(mins).padStart(2, '0')}}:${{String(secs).padStart(2, '0')}}`;

    if (timeLeft <= 900) display.className = 'timer-box timer-warning';
    if (timeLeft <= 300) display.className = 'timer-box timer-danger';
  }}, 1000);
}}

function renderNavGrid() {{
  const grid = document.getElementById('navGrid');
  grid.innerHTML = '';
  questions.forEach((q, idx) => {{
    const btn = document.createElement('button');
    btn.className = 'nav-btn';
    btn.textContent = idx + 1;
    btn.onclick = () => loadQuestion(idx);
    grid.appendChild(btn);
  }});
}}

function updateNavGrid() {{
  const btns = document.querySelectorAll('.nav-btn');
  btns.forEach((btn, idx) => {{
    btn.className = 'nav-btn';
    if (idx === currentIndex) btn.classList.add('active');
    if (userAnswers[idx] && userAnswers[idx].length > 0) btn.classList.add('answered');
    if (flagged.has(idx)) btn.classList.add('flagged');
  }});
}}

function loadQuestion(idx) {{
  currentIndex = idx;
  const q = questions[idx];

  document.getElementById('qNumber').textContent = `Question ${{idx + 1}} of ${{questions.length}}`;
  document.getElementById('domainBadge').textContent = q.d_name;
  document.getElementById('qStem').textContent = q.q;

  const flagBtn = document.getElementById('flagBtn');
  flagBtn.className = flagged.has(idx) ? 'btn btn-flag active' : 'btn btn-flag';

  const container = document.getElementById('optionsContainer');
  container.innerHTML = '';

  const selected = userAnswers[idx] || [];

  q.o.forEach((opt, optIdx) => {{
    const item = document.createElement('div');
    item.className = 'option-item' + (selected.includes(optIdx) ? ' selected' : '');
    const letter = String.fromCharCode(65 + optIdx);
    item.innerHTML = `<span class="opt-label">${{letter}})</span><span class="opt-text">${{opt}}</span>`;
    item.onclick = () => selectOption(idx, optIdx, q.multi);
    container.appendChild(item);
  }});

  document.getElementById('prevBtn').disabled = (idx === 0);
  document.getElementById('nextBtn').textContent = (idx === questions.length - 1) ? 'Review & Submit' : 'Next';
  updateNavGrid();
}}

function selectOption(qIdx, optIdx, isMulti) {{
  if (examSubmitted) return;
  if (!userAnswers[qIdx]) userAnswers[qIdx] = [];

  if (isMulti) {{
    const pos = userAnswers[qIdx].indexOf(optIdx);
    if (pos > -1) userAnswers[qIdx].splice(pos, 1);
    else userAnswers[qIdx].push(optIdx);
  }} else {{
    userAnswers[qIdx] = [optIdx];
  }}
  loadQuestion(qIdx);
}}

function toggleFlag() {{
  if (flagged.has(currentIndex)) flagged.delete(currentIndex);
  else flagged.add(currentIndex);
  loadQuestion(currentIndex);
}}

function confirmSubmit() {{
  const answeredCount = Object.keys(userAnswers).filter(k => userAnswers[k].length > 0).length;
  const unanswered = questions.length - answeredCount;
  const msg = unanswered > 0 
    ? `You have ${{unanswered}} unanswered questions. Are you sure you want to submit?`
    : 'Are you ready to submit your exam and view your score?';
  if (confirm(msg)) submitExam();
}}

function submitExam() {{
  examSubmitted = true;
  clearInterval(timerInterval);

  document.getElementById('examContainer').style.display = 'none';
  document.getElementById('resultsContainer').style.display = 'block';

  let totalCorrect = 0;
  const domainStats = {{
    1: {{ name: 'Domain 1: Development with AWS Services (32%)', total: 0, correct: 0 }},
    2: {{ name: 'Domain 2: Security (26%)', total: 0, correct: 0 }},
    3: {{ name: 'Domain 3: Deployment (24%)', total: 0, correct: 0 }},
    4: {{ name: 'Domain 4: Troubleshooting & Optimization (18%)', total: 0, correct: 0 }}
  }};

  questions.forEach((q, idx) => {{
    domainStats[q.d_id].total++;
    const userSel = (userAnswers[idx] || []).sort();
    const correctAns = (q.a || []).sort();

    const isCorrect = userSel.length === correctAns.length && userSel.every((val, i) => val === correctAns[i]);
    if (isCorrect) {{
      totalCorrect++;
      domainStats[q.d_id].correct++;
    }}
  }});

  // Scaled Score: 100 to 1000 scale
  const rawPct = (totalCorrect / questions.length);
  const scaledScore = Math.round(100 + rawPct * 900);
  const passed = scaledScore >= 720;

  document.getElementById('scoreNumber').textContent = scaledScore;
  document.getElementById('scoreSummary').textContent = `${{totalCorrect}} / ${{questions.length}} correct (${{Math.round(rawPct * 100)}}%)`;

  const badge = document.getElementById('passBadge');
  badge.textContent = passed ? 'PASSED' : 'FAILED';
  badge.className = passed ? 'pass-badge pass' : 'pass-badge fail';

  // Domain breakdown table
  const tbody = document.getElementById('domainBreakdownBody');
  tbody.innerHTML = '';
  Object.keys(domainStats).forEach(dId => {{
    const d = domainStats[dId];
    const pct = d.total > 0 ? Math.round((d.correct / d.total) * 100) : 0;
    const row = document.createElement('tr');
    row.innerHTML = `
      <td style="font-weight:600;">${{d.name}}</td>
      <td>${{dId == 1 ? '32%' : dId == 2 ? '26%' : dId == 3 ? '24%' : '18%'}}</td>
      <td>${{d.correct}} / ${{d.total}}</td>
      <td style="font-weight:700; color:${{pct >= 72 ? 'var(--correct)' : 'var(--incorrect)'}};">${{pct}}%</td>
    `;
    tbody.appendChild(row);
  }});

  // Review List
  const reviewList = document.getElementById('reviewList');
  reviewList.innerHTML = '';
  questions.forEach((q, idx) => {{
    const userSel = (userAnswers[idx] || []).sort();
    const correctAns = (q.a || []).sort();
    const isCorrect = userSel.length === correctAns.length && userSel.every((val, i) => val === correctAns[i]);

    const card = document.createElement('div');
    card.className = 'review-item';
    card.innerHTML = `
      <div style="display:flex; justify-content:space-between; margin-bottom:0.5rem;">
        <span style="font-weight:700; color:${{isCorrect ? 'var(--correct)' : 'var(--incorrect)'}};">
          ${{isCorrect ? '✓ Correct' : '✗ Incorrect'}} — Question ${{idx + 1}}
        </span>
        <span class="domain-badge">${{q.d_name}}</span>
      </div>
      <div style="font-size:0.95rem; margin-bottom:0.75rem; color:#f1f5f9;">${{q.q}}</div>
      <div style="font-size:0.875rem; color:var(--text-secondary);">
        <strong>Your Answer:</strong> ${{userSel.map(i => String.fromCharCode(65 + i)).join(', ') || 'None'}}<br>
        <strong>Correct Answer:</strong> ${{correctAns.map(i => String.fromCharCode(65 + i)).join(', ')}}
      </div>
      <div class="explanation-box">
        <strong>Explanation:</strong> ${{q.e}}
      </div>
    `;
    reviewList.appendChild(card);
  }});
}}

window.onload = init;
</script>
</body>
</html>
"""
    return html_template

def main():
    mocks = [
        ("18-Mock-Exams/mock-exam-1.md", "18-Mock-Exams/mock-exam-1.html", "DVA-C02 Timed Mock Exam 1", "AWS Certified Developer Associate • Full Mock Exam 1", "aws-dva-mock-1"),
        ("18-Mock-Exams/mock-exam-2.md", "18-Mock-Exams/mock-exam-2.html", "DVA-C02 Timed Mock Exam 2", "AWS Certified Developer Associate • Full Mock Exam 2", "aws-dva-mock-2")
    ]

    for md_path, html_path, title, eyebrow, storage_key in mocks:
        if not os.path.exists(md_path):
            print(f"File not found: {md_path}")
            continue
        q_items = parse_mock_md(md_path)
        html_content = generate_mock_html(title, eyebrow, storage_key, q_items)
        with open(html_path, 'w', encoding='utf-8') as f:
            f.write(html_content)
        print(f"Generated {html_path} with {len(q_items)} questions.")

if __name__ == "__main__":
    main()
