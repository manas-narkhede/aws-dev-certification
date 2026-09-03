#!/usr/bin/env python3
"""Generates unified study.html pages (Notes + Quiz tabs) for every module,
by reusing each module's existing notes.md and the QUESTIONS array already
embedded and validated in its quiz.html. Run once from the repo root, then delete.
"""
import re, os

ROOT = os.path.dirname(os.path.abspath(__file__))

MODULES = [
    ("00", "00-Exam-Overview-and-AWS-Fundamentals", "Exam Overview & Fundamentals", None),
    ("01", "01-EC2-and-Compute-Basics", "EC2 & Compute Basics", "1"),
    ("02", "02-S3-and-Storage", "S3 & Storage", "1"),
    ("03", "03-DynamoDB", "DynamoDB", "1"),
    ("04", "04-App-Design-Patterns-and-Lambda", "App Design Patterns & AWS Lambda", "1"),
    ("05", "05-API-Gateway-and-AppSync", "API Gateway & AppSync", "1"),
    ("06", "06-Messaging-Streaming-and-Analytics", "Messaging, Streaming & Analytics", "1"),
    ("07", "07-Step-Functions-and-Orchestration", "Step Functions & Orchestration", "1"),
    ("08", "08-Relational-and-InMemory-Databases", "Relational & In-Memory Databases", "1"),
    ("09", "09-Caching-Strategies-and-Performance", "Caching Strategies & Performance", "1"),
    ("10", "10-CICD-and-Developer-Tooling", "CI/CD & Developer Tooling", "3"),
    ("11", "11-Elastic-Beanstalk-Amplify-Copilot", "Elastic Beanstalk, Amplify & Copilot", "3"),
    ("12", "12-Containers-ECS-ECR-Fargate-EKS", "Containers (ECS, ECR, Fargate, EKS)", "3"),
    ("13", "13-IaC-CloudFormation-SAM-CDK", "IaC (CloudFormation, SAM, CDK)", "3"),
    ("14", "14-Security-Deep-Dive", "Security Deep Dive", "2"),
    ("15", "15-Networking-for-Developers", "Networking for Developers", "1"),
    ("16", "16-Monitoring-Logging-and-Observability", "Monitoring, Logging & Observability", "4"),
    ("17", "17-Well-Architected-and-Exam-Strategy", "Well-Architected & Exam Strategy", None),
]

DOMAIN_LABEL = {"1": "Domain 1 · Development (32%)", "2": "Domain 2 · Security (26%)",
                "3": "Domain 3 · Deployment (24%)", "4": "Domain 4 · Troubleshooting (18%)"}

TEMPLATE = r"""<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{page_title}</title>
<link rel="stylesheet" href="../assets/theme.css">
<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Public+Sans:wght@400;500;600;700;800&family=IBM+Plex+Mono:wght@500;600&display=swap">
<script src="https://cdnjs.cloudflare.com/ajax/libs/marked/12.0.2/marked.min.js"></script>
</head>
<body>
<header class="topbar">
  <a class="crumb" href="../index.html">&#8962; Hub</a>
  <span class="divider">/</span>
  <span class="page-title">Module {num} &mdash; {title}</span>
  {domain_chip}
  <span class="spacer"></span>
  <div class="tabbar">
    <button class="tabbtn active" data-tab="notes">Notes</button>
    <button class="tabbtn" data-tab="quiz">Practice Questions ({count})</button>
  </div>
</header>

<main>
  <section id="tab-notes" class="tabpanel active">
    <div class="notes-wrap">
      <nav id="notesToc" class="notes-toc"></nav>
      <article id="notesBody" class="notes-body"></article>
    </div>
  </section>

  <section id="tab-quiz" class="tabpanel">
    <div class="quiz-wrap">
      <div class="quiz-topline">
        <div class="stat"><span class="num" id="posNum">1 / {count}</span><span class="lbl">Question</span></div>
        <div class="stat"><span class="num" id="scoreNum">0</span><span class="lbl">Correct</span></div>
      </div>
      <div class="progress-track"><div class="progress-fill" id="progressFill" style="width:0%"></div></div>
      <div id="quizArea"></div>
      <div class="footer-note">Progress is saved automatically in this browser. Use 1&ndash;5 or A&ndash;E on your keyboard to answer.</div>
    </div>
  </section>
</main>

<script src="../assets/quiz-engine.js"></script>
<script src="../assets/notes-render.js"></script>
<script>
const NOTES_MD = `{notes_js}`;
{questions_block}
const STORAGE_KEY = "aws-dva-quiz-{num}";

document.querySelectorAll(".tabbtn").forEach(function(btn){{
  btn.addEventListener("click", function(){{
    document.querySelectorAll(".tabbtn").forEach(function(b){{ b.classList.remove("active"); }});
    document.querySelectorAll(".tabpanel").forEach(function(p){{ p.classList.remove("active"); }});
    btn.classList.add("active");
    document.getElementById("tab-" + btn.dataset.tab).classList.add("active");
  }});
}});

renderNotes(NOTES_MD);
initQuiz(QUESTIONS, STORAGE_KEY);

if(location.hash === "#quiz"){{ document.querySelector('[data-tab="quiz"]').click(); }}
</script>
</body>
</html>
"""

def extract_questions_block(quiz_html_path):
    text = open(quiz_html_path, encoding="utf-8").read()
    start = text.index("const QUESTIONS = [")
    end = text.index("\nlet idx = 0", start)
    block = text[start:end].rstrip()
    if not block.endswith(";"):
        block += ";"
    return block

def js_escape_template(md_text):
    return md_text.replace("\\", "\\\\").replace("`", "\\`").replace("${", "\\${")

SCHEDULE = [
    ("Day 1 &middot; Mon Aug 31", ["00", "01"], False),
    ("Day 2 &middot; Tue Sep 01", ["02", "03"], False),
    ("Day 3 &middot; Wed Sep 02", ["04", "05"], False),
    ("Day 4 &middot; Thu Sep 03", ["06", "07"], False),
    ("Day 5 &middot; Fri Sep 04", ["08", "09"], False),
    ("Day 6 &middot; Sat Sep 05 &mdash; heavy", ["10", "11", "12"], True),
    ("Day 7 &middot; Sun Sep 06 &mdash; heavy", ["13", "14", "15"], True),
    ("Day 8 &middot; Mon Sep 07", ["16", "17"], False),
]

HUB_TEMPLATE = r"""<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>AWS DVA-C02 Study Hub</title>
<link rel="stylesheet" href="assets/theme.css">
<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Public+Sans:wght@400;500;600;700;800&family=IBM+Plex+Mono:wght@500;600&display=swap">
<style>
.hero{{max-width:1040px; margin:0 auto; padding:44px 20px 8px;}}
.hero .eyebrow{{font-family:"IBM Plex Mono",monospace; font-size:12px; letter-spacing:.08em; text-transform:uppercase; color:var(--accent); font-weight:600;}}
.hero h1{{font-size:30px; font-weight:800; letter-spacing:-.01em; margin:6px 0 10px; text-wrap:balance;}}
.hero p.lede{{font-size:15px; color:var(--muted); max-width:62ch; line-height:1.6; margin:0 0 26px;}}
.factstrip{{display:grid; grid-template-columns:repeat(auto-fit,minmax(120px,1fr)); gap:1px; background:var(--border); border:1px solid var(--border); border-radius:var(--radius); overflow:hidden; margin-bottom:10px;}}
.factstrip .fact{{background:var(--surface); padding:14px 16px;}}
.factstrip .fact .v{{font-family:"IBM Plex Mono",monospace; font-size:19px; font-weight:600;}}
.factstrip .fact .k{{font-size:11px; color:var(--muted); text-transform:uppercase; letter-spacing:.06em; margin-top:2px;}}
.note{{font-size:12.5px; color:var(--muted); max-width:70ch; margin:14px 0 0; line-height:1.6;}}
main.hub{{max-width:1040px; margin:0 auto; padding:20px 20px 90px;}}
.daygroup{{margin-bottom:30px;}}
.daygroup h2{{font-size:13px; font-weight:700; text-transform:uppercase; letter-spacing:.05em; color:var(--muted); margin:0 0 12px; display:flex; align-items:center; gap:10px;}}
.daygroup h2 .heavy{{background:var(--accent-soft); color:var(--accent); font-family:"IBM Plex Mono",monospace; font-size:10.5px; padding:2px 8px; border-radius:999px; text-transform:none; letter-spacing:0;}}
.cardgrid{{display:grid; grid-template-columns:repeat(auto-fill,minmax(260px,1fr)); gap:12px;}}
.modcard{{background:var(--surface); border:1px solid var(--border); border-radius:var(--radius); padding:16px 18px; display:flex; flex-direction:column; gap:10px;}}
.modcard .mtop{{display:flex; align-items:flex-start; justify-content:space-between; gap:8px;}}
.modcard .mnum{{font-family:"IBM Plex Mono",monospace; font-size:11px; color:var(--muted); font-weight:600;}}
.modcard h3{{font-size:14.5px; font-weight:700; margin:2px 0 0; line-height:1.35;}}
.modcard .mmeta{{display:flex; align-items:center; gap:8px; flex-wrap:wrap;}}
.modcard .qcount{{font-family:"IBM Plex Mono",monospace; font-size:11px; color:var(--muted);}}
.modcard .mactions{{display:flex; gap:8px; margin-top:2px;}}
.mockrow{{display:grid; grid-template-columns:repeat(auto-fill,minmax(280px,1fr)); gap:12px;}}
.mockcard{{background:var(--surface); border:1px solid var(--border); border-radius:var(--radius); padding:18px; display:flex; flex-direction:column; gap:10px;}}
.mockcard h3{{font-size:15px; font-weight:700; margin:0;}}
.mockcard p{{font-size:13px; color:var(--muted); margin:0; line-height:1.5;}}
footer.hubfoot{{max-width:1040px; margin:0 auto; padding:0 20px 50px; font-size:12px; color:var(--muted); text-align:center;}}
</style>
</head>
<body>
<div class="hero">
  <div class="eyebrow">AWS Certified Developer &ndash; Associate &middot; DVA-C02</div>
  <h1>Study Hub</h1>
  <p class="lede">18 modules, ~2,300 practice questions, and 2 full timed mock exams &mdash; grounded in AWS's official exam guide. Click any module to read its notes and take its quiz in one place.</p>
  <div class="factstrip">
    <div class="fact"><div class="v">65</div><div class="k">Questions</div></div>
    <div class="fact"><div class="v">130</div><div class="k">Minutes</div></div>
    <div class="fact"><div class="v">720</div><div class="k">Pass score /1000</div></div>
    <div class="fact"><div class="v">32/26/24/18</div><div class="k">Domain weight %</div></div>
  </div>
  <p class="note">Progress (score, current question) is saved per-page in your browser's local storage. If you open these files directly (double-click), each file is a separate local origin, so progress doesn't sync between pages &mdash; that's a browser limitation, not a bug. Tick off modules in <code>README.md</code> as you finish them.</p>
</div>

<main class="hub">
{day_groups}
  <div class="daygroup">
    <h2>Day 9&ndash;10 &middot; Review &amp; Mock Exams</h2>
    <div class="mockrow">
      <div class="mockcard">
        <h3>Mock Exam 1</h3>
        <p>65 questions, 130-minute countdown timer, domain-by-domain score breakdown.</p>
        <div class="mactions"><a class="btn btn-primary btn-sm" href="18-Mock-Exams/mock-exam-1.html">Start exam &rarr;</a></div>
      </div>
      <div class="mockcard">
        <h3>Mock Exam 2</h3>
        <p>A second full-length simulation with different questions, same weighting.</p>
        <div class="mactions"><a class="btn btn-primary btn-sm" href="18-Mock-Exams/mock-exam-2.html">Start exam &rarr;</a></div>
      </div>
    </div>
  </div>
</main>

<footer class="hubfoot">Built from AWS's official DVA-C02 exam guide and sample questions. See <code>HANDOVER.md</code> for the full research/build brief.</footer>
</body>
</html>
"""

def build_hub(counts, titles, domains):
    groups_html = []
    for label, nums, heavy in SCHEDULE:
        cards = []
        for n in nums:
            title = titles[n]
            count = counts[n]
            domain = domains[n]
            chip = ""
            if domain:
                chip = '<span class="domain-chip" style="background:var(--d{d}-bg);color:var(--d{d});font-size:10px;padding:2px 7px;">D{d}</span>'.format(d=domain)
            folder = dict((m[0], m[1]) for m in MODULES)[n]
            cards.append(f'''      <div class="modcard">
        <div class="mtop"><span class="mnum">MODULE {n}</span>{chip}</div>
        <h3>{title}</h3>
        <div class="mmeta"><span class="qcount">{count} questions</span></div>
        <div class="mactions">
          <a class="btn btn-primary btn-sm" href="{folder}/study.html">Notes &amp; Quiz</a>
          <a class="btn btn-ghost btn-sm" href="{folder}/study.html#quiz">Quiz only</a>
        </div>
      </div>''')
        heavy_badge = '<span class="heavy">heavy day</span>' if heavy else ""
        groups_html.append(f'''  <div class="daygroup">
    <h2>{label} {heavy_badge}</h2>
    <div class="cardgrid">
{chr(10).join(cards)}
    </div>
  </div>''')
    html = HUB_TEMPLATE.format(day_groups="\n".join(groups_html))
    with open(os.path.join(ROOT, "index.html"), "w", encoding="utf-8") as f:
        f.write(html)
    print("Hub -> index.html")

def main():
    counts, titles, domains = {}, {}, {}
    for num, folder, title, domain in MODULES:
        folder_path = os.path.join(ROOT, folder)
        notes_path = os.path.join(folder_path, "notes.md")
        quiz_path = os.path.join(folder_path, "quiz.html")
        notes_md = open(notes_path, encoding="utf-8").read()
        questions_block = extract_questions_block(quiz_path)
        count_match = re.findall(r'"?q"?\s*:\s*"', questions_block)
        count = len(count_match)
        counts[num] = count; titles[num] = title; domains[num] = domain
        domain_chip = ""
        if domain:
            domain_chip = '<span class="domain-chip" style="background:var(--d{d}-bg);color:var(--d{d});">{label}</span>'.format(
                d=domain, label=DOMAIN_LABEL[domain])
        html = TEMPLATE.format(
            page_title=f"Module {num} — {title}",
            num=num, title=title, count=count,
            domain_chip=domain_chip,
            notes_js=js_escape_template(notes_md),
            questions_block=questions_block,
        )
        out_path = os.path.join(folder_path, "study.html")
        with open(out_path, "w", encoding="utf-8") as f:
            f.write(html)
        print(f"Module {num}: {count} questions -> {out_path}")
    build_hub(counts, titles, domains)

if __name__ == "__main__":
    main()
