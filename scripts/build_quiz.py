#!/usr/bin/env python3
import sys
import os
import re
import json

def parse_questions_md(md_path):
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
    # Split by number followed by dot at start of line
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
                # Still in stem
                stem_lines.append(l)
            else:
                # Continuation of previous option
                opt_lines[-1] += " " + l

        stem = " ".join(stem_lines).strip()
        # Clean up any trailing dashes or dividers from options
        options = [re.sub(r"\s*---\s*$", "", re.sub(r"^[A-E]\)\s*", "", o)).strip() for o in opt_lines]

        if qnum in ans_dict:
            a_indices, exp = ans_dict[qnum]
            is_multi = len(a_indices) > 1 or "(Select TWO)" in stem or "(Select THREE)" in stem or "(Select all" in stem
            q_items.append({
                "num": qnum,
                "q": stem,
                "o": options,
                "a": a_indices,
                "multi": is_multi,
                "e": exp
            })
        else:
            print(f"Warning: Missing answer for question {qnum} in {md_path}")

    return q_items

def generate_quiz_html(module_title, eyebrow_text, storage_key, q_items):
    total_q = len(q_items)
    
    # Format questions array for JS
    q_objs = []
    for item in q_items:
        obj = {
            "q": item["q"],
            "o": item["o"],
            "a": item["a"],
        }
        if item["multi"]:
            obj["multi"] = True
        obj["e"] = item["e"]
        q_objs.append(obj)

    questions_json = json.dumps(q_objs, ensure_ascii=False, indent=2)

    html_content = f"""<title>{module_title}</title>
<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Public+Sans:wght@400;500;600;700;800&family=IBM+Plex+Mono:wght@500;600&display=swap">
<style>
:root{{
  --bg:#f5f6f4; --surface:#ffffff; --surface-2:#eceeec; --ink:#141a1f; --muted:#5c6670;
  --border:#dde1de; --accent:#0d7377; --accent-ink:#ffffff; --accent-soft:#e3f1f0;
  --success:#1f8a44; --success-bg:#e5f6ea; --success-border:#a9dfb8;
  --danger:#c8402f; --danger-bg:#fbe9e6; --danger-border:#f0b8ac;
  --radius:14px;
}}
@media (prefers-color-scheme: dark){{
  :root:not([data-theme="light"]){{
    --bg:#10151a; --surface:#171e25; --surface-2:#1d252c; --ink:#edf1f3; --muted:#93a3ac;
    --border:#2b343c; --accent:#37c9c2; --accent-ink:#08211f; --accent-soft:#173430;
    --success:#5fd489; --success-bg:#123321; --success-border:#256b45;
    --danger:#f38672; --danger-bg:#3a1c17; --danger-border:#7a3226;
  }}
}}
:root[data-theme="dark"]{{
  --bg:#10151a; --surface:#171e25; --surface-2:#1d252c; --ink:#edf1f3; --muted:#93a3ac;
  --border:#2b343c; --accent:#37c9c2; --accent-ink:#08211f; --accent-soft:#173430;
  --success:#5fd489; --success-bg:#123321; --success-border:#256b45;
  --danger:#f38672; --danger-bg:#3a1c17; --danger-border:#7a3226;
}}
*{{box-sizing:border-box;}}
body{{background:var(--bg); color:var(--ink); font-family:"Public Sans",system-ui,-apple-system,sans-serif; -webkit-font-smoothing:antialiased;}}
.wrap{{max-width:760px; margin:0 auto; padding:28px 20px 80px;}}
.eyebrow{{font-family:"IBM Plex Mono",monospace; font-size:12px; letter-spacing:.08em; text-transform:uppercase; color:var(--accent); font-weight:600;}}
h1{{font-size:22px; font-weight:800; margin:4px 0 18px; text-wrap:balance; letter-spacing:-.01em;}}
.topbar{{display:flex; align-items:center; justify-content:space-between; gap:16px; margin-bottom:8px; flex-wrap:wrap;}}
.stat{{display:flex; flex-direction:column; align-items:flex-end;}}
.stat .num{{font-family:"IBM Plex Mono",monospace; font-variant-numeric:tabular-nums; font-size:18px; font-weight:600;}}
.stat .lbl{{font-size:11px; color:var(--muted); text-transform:uppercase; letter-spacing:.06em;}}
.progress-track{{height:8px; background:var(--surface-2); border-radius:999px; overflow:hidden; margin:14px 0 28px; border:1px solid var(--border);}}
.progress-fill{{height:100%; background:var(--accent); border-radius:999px; transition:width .35s ease;}}
@media (prefers-reduced-motion: reduce){{ .progress-fill{{transition:none;}} }}

.card{{background:var(--surface); border:1px solid var(--border); border-radius:var(--radius); padding:26px; box-shadow:0 1px 2px rgba(0,0,0,.04);}}
.qnum{{font-family:"IBM Plex Mono",monospace; font-size:13px; color:var(--muted); font-variant-numeric:tabular-nums; margin-bottom:10px;}}
.qtext{{font-size:16.5px; font-weight:600; line-height:1.55; margin-bottom:20px; text-wrap:balance;}}
.multi-hint{{display:inline-block; font-size:12px; font-weight:600; color:var(--accent); background:var(--accent-soft); border-radius:999px; padding:3px 10px; margin-bottom:14px;}}

.opt{{display:flex; align-items:flex-start; gap:12px; width:100%; text-align:left; background:var(--surface); border:1.5px solid var(--border); border-radius:10px; padding:13px 14px; margin-bottom:10px; cursor:pointer; font:inherit; color:var(--ink); font-size:14.5px; line-height:1.5; transition:border-color .15s, background .15s;}}
.opt:hover{{border-color:var(--accent);}}
.opt:focus-visible{{outline:2px solid var(--accent); outline-offset:2px;}}
.opt .mark{{flex:0 0 22px; height:22px; border-radius:6px; border:1.5px solid var(--border); display:flex; align-items:center; justify-content:center; font-family:"IBM Plex Mono",monospace; font-size:12px; font-weight:600; color:var(--muted); margin-top:1px;}}
.opt.selected{{border-color:var(--accent); background:var(--accent-soft);}}
.opt.selected .mark{{border-color:var(--accent); color:var(--accent);}}
.opt.correct{{border-color:var(--success-border); background:var(--success-bg);}}
.opt.correct .mark{{border-color:var(--success); color:var(--success); background:var(--success-bg);}}
.opt.incorrect{{border-color:var(--danger-border); background:var(--danger-bg);}}
.opt.incorrect .mark{{border-color:var(--danger); color:var(--danger); background:var(--danger-bg);}}
.opt:disabled{{cursor:default;}}
.opt:disabled:hover{{border-color:var(--border);}}
.opt.correct:hover, .opt.incorrect:hover{{border-color:inherit;}}

.actions{{display:flex; gap:10px; margin-top:18px; flex-wrap:wrap;}}
button.btn{{font:inherit; font-weight:700; font-size:14px; border-radius:9px; padding:11px 18px; cursor:pointer; border:1.5px solid transparent;}}
.btn-primary{{background:var(--accent); color:var(--accent-ink); border-color:var(--accent);}}
.btn-primary:disabled{{opacity:.4; cursor:not-allowed;}}
.btn-ghost{{background:transparent; color:var(--ink); border-color:var(--border);}}
.btn-ghost:hover{{border-color:var(--accent);}}
button:focus-visible{{outline:2px solid var(--accent); outline-offset:2px;}}

.explain{{margin-top:16px; padding:14px 16px; border-radius:10px; font-size:14px; line-height:1.55; border:1px solid var(--border); background:var(--surface-2);}}
.explain b{{color:var(--accent);}}

.summary{{text-align:center; padding:10px 0 20px;}}
.score-big{{font-family:"IBM Plex Mono",monospace; font-size:52px; font-weight:600; font-variant-numeric:tabular-nums; letter-spacing:-.02em;}}
.score-pct{{color:var(--muted); font-size:15px; margin-top:2px;}}
.score-pct.pass{{color:var(--success); font-weight:700;}}
.score-pct.fail{{color:var(--danger); font-weight:700;}}
.miss-list{{margin-top:28px; text-align:left; border-top:1px solid var(--border); padding-top:20px;}}
.miss-list h3{{font-size:14px; text-transform:uppercase; letter-spacing:.06em; color:var(--muted); margin-bottom:12px; font-family:"IBM Plex Mono",monospace;}}
.miss-item{{padding:10px 12px; background:var(--surface-2); border-radius:8px; margin-bottom:8px; font-size:13.5px; line-height:1.45; border-left:3px solid var(--danger);}}
.miss-item b{{color:var(--ink);}}

.footer-note{{text-align:center; color:var(--muted); font-size:12px; margin-top:24px; font-family:"IBM Plex Mono",monospace;}}
</style>

<div class="wrap">
  <div class="topbar">
    <div>
      <div class="eyebrow">{eyebrow_text}</div>
      <h1>{module_title}</h1>
    </div>
    <div class="stat">
      <span class="num" id="posNum">1 / {total_q}</span>
      <span class="lbl">Question</span>
    </div>
    <div class="stat">
      <span class="num" id="scoreNum">0</span>
      <span class="lbl">Correct</span>
    </div>
  </div>
  <div class="progress-track"><div class="progress-fill" id="progressFill" style="width:0%"></div></div>

  <div id="quizArea"></div>
  <div class="footer-note">Progress is saved automatically in this browser. Use 1–5 or A–E on your keyboard to answer.</div>
</div>

<script>
const QUESTIONS = {questions_json};

let idx = 0, score = 0, answered = new Array(QUESTIONS.length).fill(false), correctFlags = new Array(QUESTIONS.length).fill(false), missed = [];
const STORAGE_KEY = "{storage_key}";

function save(){{
  try{{
    localStorage.setItem(STORAGE_KEY, JSON.stringify({{idx, score, answered, correctFlags}}));
  }}catch(e){{}}
}}
function load(){{
  try{{
    const raw = localStorage.getItem(STORAGE_KEY);
    if(!raw) return false;
    const d = JSON.parse(raw);
    if(d && Array.isArray(d.answered) && d.answered.length === QUESTIONS.length){{
      idx = d.idx; score = d.score; answered = d.answered; correctFlags = d.correctFlags;
      return true;
    }}
  }}catch(e){{}}
  return false;
}}

const quizArea = document.getElementById("quizArea");
const posNum = document.getElementById("posNum");
const scoreNum = document.getElementById("scoreNum");
const progressFill = document.getElementById("progressFill");

function updateTop(){{
  posNum.textContent = (idx+1) + " / " + QUESTIONS.length;
  scoreNum.textContent = score;
  const answeredCount = answered.filter(Boolean).length;
  progressFill.style.width = (answeredCount / QUESTIONS.length * 100) + "%";
}}

function renderQuestion(){{
  const item = QUESTIONS[idx];
  const isMulti = !!item.multi;
  const done = answered[idx];
  let html = "";
  html += '<div class="card">';
  html += '<div class="qnum">Question ' + (idx+1) + '</div>';
  if(isMulti) html += '<div class="multi-hint">Select all that apply</div><br>';
  html += '<div class="qtext">' + escapeHtml(item.q) + '</div>';
  item.o.forEach((optText, i)=>{{
    const letter = String.fromCharCode(65+i);
    let cls = "opt";
    if(done){{
      if(item.a.includes(i)) cls += " correct";
      else if(item.picked && item.picked.includes(i)) cls += " incorrect";
    }} else if(item.picked && item.picked.includes(i)){{
      cls += " selected";
    }}
    html += '<button class="' + cls + '" data-i="' + i + '" ' + (done?'disabled':'') + '>' +
      '<span class="mark">' + letter + '</span><span>' + escapeHtml(optText) + '</span></button>';
  }});
  if(done){{
    html += '<div class="explain"><b>' + (correctFlags[idx] ? "Correct. " : "Not quite. ") + '</b>' + escapeHtml(item.e) + '</div>';
  }}
  html += '<div class="actions">';
  if(isMulti && !done){{
    html += '<button class="btn btn-primary" id="submitBtn" disabled>Submit answer</button>';
  }}
  if(done){{
    if(idx < QUESTIONS.length - 1){{
      html += '<button class="btn btn-primary" id="nextBtn">Next question</button>';
    }} else {{
      html += '<button class="btn btn-primary" id="finishBtn">See results</button>';
    }}
  }}
  html += '<button class="btn btn-ghost" id="resetBtn">Reset progress</button>';
  html += '</div></div>';
  quizArea.innerHTML = html;
  updateTop();
  wireOptions(item, isMulti, done);
}}

function escapeHtml(s){{
  return s.replace(/&/g,"&amp;").replace(/</g,"&lt;").replace(/>/g,"&gt;");
}}

function wireOptions(item, isMulti, done){{
  const opts = quizArea.querySelectorAll(".opt");
  opts.forEach(btn=>{{
    btn.addEventListener("click", ()=>{{
      if(done) return;
      const i = parseInt(btn.dataset.i, 10);
      if(isMulti){{
        item.picked = item.picked || [];
        const pos = item.picked.indexOf(i);
        if(pos >= 0) item.picked.splice(pos,1); else item.picked.push(i);
        renderQuestion();
        const submitBtn = document.getElementById("submitBtn");
        if(submitBtn) submitBtn.disabled = !(item.picked && item.picked.length > 0);
      }} else {{
        item.picked = [i];
        commitAnswer(item);
      }}
    }});
  }});
  const submitBtn = document.getElementById("submitBtn");
  if(submitBtn){{
    submitBtn.disabled = !(item.picked && item.picked.length > 0);
    submitBtn.addEventListener("click", ()=> commitAnswer(item));
  }}
  const nextBtn = document.getElementById("nextBtn");
  if(nextBtn) nextBtn.addEventListener("click", ()=>{{ idx++; save(); renderQuestion(); }});
  const finishBtn = document.getElementById("finishBtn");
  if(finishBtn) finishBtn.addEventListener("click", renderSummary);
  const resetBtn = document.getElementById("resetBtn");
  if(resetBtn) resetBtn.addEventListener("click", resetAll);
}}

function commitAnswer(item){{
  if(answered[idx]) return;
  answered[idx] = true;
  const correct = item.picked.length === item.a.length && item.picked.every(p => item.a.includes(p));
  correctFlags[idx] = correct;
  if(correct) score++; else missed.push(idx);
  save();
  renderQuestion();
}}

function renderSummary(){{
  const pct = Math.round(score / QUESTIONS.length * 100);
  const passed = pct >= 72;
  let html = '<div class="card summary">';
  html += '<div class="eyebrow">Results</div>';
  html += '<div class="score-big">' + score + ' / ' + QUESTIONS.length + '</div>';
  html += '<div class="score-pct ' + (passed?'pass':'fail') + '">' + pct + '% — ' + (passed ? "Solid, above the ~72% pass bar" : "Below the ~72% pass bar — revisit the notes") + '</div>';
  const missedList = answered.map((_,i)=>i).filter(i => !correctFlags[i]);
  if(missedList.length){{
    html += '<div class="miss-list"><h3>Review these questions</h3>';
    missedList.forEach(i=>{{
      html += '<div class="miss-item"><b>Q' + (i+1) + '.</b> ' + escapeHtml(QUESTIONS[i].q) + '</div>';
    }});
    html += '</div>';
  }}
  html += '<div class="actions" style="justify-content:center; margin-top:22px;">';
  html += '<button class="btn btn-primary" id="restartBtn">Restart quiz</button>';
  html += '<button class="btn btn-ghost" id="resetBtn2">Reset progress</button>';
  html += '</div></div>';
  quizArea.innerHTML = html;
  document.getElementById("restartBtn").addEventListener("click", resetAll);
  document.getElementById("resetBtn2").addEventListener("click", resetAll);
}}

function resetAll(){{
  idx = 0; score = 0; missed = [];
  answered = new Array(QUESTIONS.length).fill(false);
  correctFlags = new Array(QUESTIONS.length).fill(false);
  QUESTIONS.forEach(q => {{ delete q.picked; }});
  try{{ localStorage.removeItem(STORAGE_KEY); }}catch(e){{}}
  renderQuestion();
}}

document.addEventListener("keydown", (e)=>{{
  const map = {{"1":0,"2":1,"3":2,"4":3,"5":4,"a":0,"b":1,"c":2,"d":3,"e":4,"A":0,"B":1,"C":2,"D":3,"E":4}};
  if(e.key in map){{
    const opts = quizArea.querySelectorAll(".opt:not(:disabled)");
    const i = map[e.key];
    if(opts[i]) opts[i].click();
  }} else if(e.key === "Enter"){{
    const nb = document.getElementById("nextBtn") || document.getElementById("finishBtn") || document.getElementById("submitBtn");
    if(nb && !nb.disabled) nb.click();
  }}
}});

if(load()){{
  if(answered.every(Boolean)) renderSummary(); else renderQuestion();
}} else {{
  renderQuestion();
}}
</script>
"""
    return html_content

if __name__ == "__main__":
    if len(sys.argv) < 5:
        print("Usage: build_quiz.py <module_dir> <title> <eyebrow> <storage_key>")
        sys.exit(1)
    
    module_dir = sys.argv[1]
    title = sys.argv[2]
    eyebrow = sys.argv[3]
    storage_key = sys.argv[4]

    md_path = os.path.join(module_dir, "questions.md")
    out_html = os.path.join(module_dir, "quiz.html")

    q_items = parse_questions_md(md_path)
    html = generate_quiz_html(title, eyebrow, storage_key, q_items)

    with open(out_html, "w", encoding="utf-8") as f:
        f.write(html)

    print(f"Generated {out_html} with {len(q_items)} questions.")
