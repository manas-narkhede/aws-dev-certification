/* Shared quiz engine. Expects a global QUESTIONS array ({q,o,a,multi,e}) and STORAGE_KEY string
   to already be defined on the page, and these elements to exist: #quizArea, #posNum, #scoreNum, #progressFill */
(function(){
  function initQuiz(QUESTIONS, STORAGE_KEY, opts){
    opts = opts || {};
    let idx = 0, score = 0, answered = new Array(QUESTIONS.length).fill(false), correctFlags = new Array(QUESTIONS.length).fill(false);

    function save(){
      try{ localStorage.setItem(STORAGE_KEY, JSON.stringify({idx, score, answered, correctFlags})); }catch(e){}
    }
    function load(){
      try{
        const raw = localStorage.getItem(STORAGE_KEY);
        if(!raw) return false;
        const d = JSON.parse(raw);
        if(d && Array.isArray(d.answered) && d.answered.length === QUESTIONS.length){
          idx = d.idx; score = d.score; answered = d.answered; correctFlags = d.correctFlags;
          return true;
        }
      }catch(e){}
      return false;
    }

    const quizArea = document.getElementById("quizArea");
    const posNum = document.getElementById("posNum");
    const scoreNum = document.getElementById("scoreNum");
    const progressFill = document.getElementById("progressFill");

    function escapeHtml(s){
      return String(s).replace(/&/g,"&amp;").replace(/</g,"&lt;").replace(/>/g,"&gt;");
    }

    function updateTop(){
      if(posNum) posNum.textContent = (idx+1) + " / " + QUESTIONS.length;
      if(scoreNum) scoreNum.textContent = score;
      const answeredCount = answered.filter(Boolean).length;
      if(progressFill) progressFill.style.width = (answeredCount / QUESTIONS.length * 100) + "%";
      if(opts.onProgress) opts.onProgress(answeredCount, QUESTIONS.length, score);
    }

    function renderQuestion(){
      const item = QUESTIONS[idx];
      const isMulti = !!item.multi;
      const done = answered[idx];
      let html = "";
      html += '<div class="card">';
      html += '<div class="qnum">Question ' + (idx+1) + '</div>';
      if(isMulti) html += '<div class="multi-hint">Select all that apply</div><br>';
      html += '<div class="qtext">' + escapeHtml(item.q) + '</div>';
      item.o.forEach((optText, i)=>{
        const letter = String.fromCharCode(65+i);
        let cls = "opt";
        if(done){
          if(item.a.includes(i)) cls += " correct";
          else if(item.picked && item.picked.includes(i)) cls += " incorrect";
        } else if(item.picked && item.picked.includes(i)){
          cls += " selected";
        }
        html += '<button class="' + cls + '" data-i="' + i + '" ' + (done?'disabled':'') + '>' +
          '<span class="mark">' + letter + '</span><span>' + escapeHtml(optText) + '</span></button>';
      });
      if(done){
        html += '<div class="explain"><b>' + (correctFlags[idx] ? "Correct. " : "Not quite. ") + '</b>' + escapeHtml(item.e) + '</div>';
      }
      html += '<div class="actions">';
      if(isMulti && !done){
        html += '<button class="btn btn-primary" id="submitBtn" disabled>Submit answer</button>';
      }
      if(done){
        if(idx < QUESTIONS.length - 1){
          html += '<button class="btn btn-primary" id="nextBtn">Next question</button>';
        } else {
          html += '<button class="btn btn-primary" id="finishBtn">See results</button>';
        }
      }
      html += '<button class="btn btn-ghost" id="resetBtn">Reset progress</button>';
      html += '</div></div>';
      quizArea.innerHTML = html;
      updateTop();
      wireOptions(item, isMulti, done);
    }

    function wireOptions(item, isMulti, done){
      const opts2 = quizArea.querySelectorAll(".opt");
      opts2.forEach(btn=>{
        btn.addEventListener("click", ()=>{
          if(done) return;
          const i = parseInt(btn.dataset.i, 10);
          if(isMulti){
            item.picked = item.picked || [];
            const pos = item.picked.indexOf(i);
            if(pos >= 0) item.picked.splice(pos,1); else item.picked.push(i);
            renderQuestion();
            const submitBtn = document.getElementById("submitBtn");
            if(submitBtn) submitBtn.disabled = !(item.picked && item.picked.length > 0);
          } else {
            item.picked = [i];
            commitAnswer(item);
          }
        });
      });
      const submitBtn = document.getElementById("submitBtn");
      if(submitBtn){
        submitBtn.disabled = !(item.picked && item.picked.length > 0);
        submitBtn.addEventListener("click", ()=> commitAnswer(item));
      }
      const nextBtn = document.getElementById("nextBtn");
      if(nextBtn) nextBtn.addEventListener("click", ()=>{ idx++; save(); renderQuestion(); });
      const finishBtn = document.getElementById("finishBtn");
      if(finishBtn) finishBtn.addEventListener("click", renderSummary);
      const resetBtn = document.getElementById("resetBtn");
      if(resetBtn) resetBtn.addEventListener("click", resetAll);
    }

    function commitAnswer(item){
      if(answered[idx]) return;
      answered[idx] = true;
      const correct = item.picked.length === item.a.length && item.picked.every(p => item.a.includes(p));
      correctFlags[idx] = correct;
      if(correct) score++;
      save();
      renderQuestion();
    }

    function renderSummary(){
      const pct = Math.round(score / QUESTIONS.length * 100);
      const passed = pct >= 72;
      let html = '<div class="card summary">';
      html += '<div class="eyebrow">Results</div>';
      html += '<div class="score-big">' + score + ' / ' + QUESTIONS.length + '</div>';
      html += '<div class="score-pct ' + (passed?'pass':'fail') + '">' + pct + '% — ' + (passed ? "Solid, above the ~72% pass bar" : "Below the ~72% pass bar — revisit the notes") + '</div>';
      const missedList = answered.map((_,i)=>i).filter(i => !correctFlags[i]);
      if(missedList.length){
        html += '<div class="miss-list"><h3>Review these questions</h3>';
        missedList.forEach(i=>{
          html += '<div class="miss-item"><b>Q' + (i+1) + '.</b> ' + escapeHtml(QUESTIONS[i].q) + '</div>';
        });
        html += '</div>';
      }
      html += '<div class="actions" style="justify-content:center; margin-top:22px;">';
      html += '<button class="btn btn-primary" id="restartBtn">Restart quiz</button>';
      html += '<button class="btn btn-ghost" id="resetBtn2">Reset progress</button>';
      html += '</div></div>';
      quizArea.innerHTML = html;
      if(opts.onFinish) opts.onFinish(score, QUESTIONS.length, pct);
      document.getElementById("restartBtn").addEventListener("click", resetAll);
      document.getElementById("resetBtn2").addEventListener("click", resetAll);
    }

    function resetAll(){
      idx = 0; score = 0;
      answered = new Array(QUESTIONS.length).fill(false);
      correctFlags = new Array(QUESTIONS.length).fill(false);
      QUESTIONS.forEach(q => { delete q.picked; });
      try{ localStorage.removeItem(STORAGE_KEY); }catch(e){}
      renderQuestion();
    }

    document.addEventListener("keydown", (e)=>{
      if(!quizArea || quizArea.offsetParent === null) return; // only respond when quiz tab is visible
      const map = {"1":0,"2":1,"3":2,"4":3,"5":4,"a":0,"b":1,"c":2,"d":3,"e":4,"A":0,"B":1,"C":2,"D":3,"E":4};
      if(e.key in map){
        const opts2 = quizArea.querySelectorAll(".opt:not(:disabled)");
        const i = map[e.key];
        if(opts2[i]) opts2[i].click();
      } else if(e.key === "Enter"){
        const nb = document.getElementById("nextBtn") || document.getElementById("finishBtn") || document.getElementById("submitBtn");
        if(nb && !nb.disabled) nb.click();
      }
    });

    if(load()){
      if(answered.every(Boolean)) renderSummary(); else renderQuestion();
    } else {
      renderQuestion();
    }

    return { resetAll: resetAll };
  }
  window.initQuiz = initQuiz;
})();
