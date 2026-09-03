/* Renders a NOTES_MD markdown string into #notesBody and builds a TOC in #notesToc.
   Requires marked.js (window.marked) to already be loaded. */
(function(){
  function slugify(text){
    return String(text).toLowerCase().trim()
      .replace(/[`*_~]/g,"")
      .replace(/[^a-z0-9\s-]/g,"")
      .replace(/\s+/g,"-")
      .replace(/-+/g,"-");
  }

  function renderNotes(NOTES_MD){
    const body = document.getElementById("notesBody");
    const tocEl = document.getElementById("notesToc");
    if(!body) return;

    const renderer = new marked.Renderer();
    const used = {};
    renderer.heading = function(text, level){
      let slug = slugify(text);
      if(used[slug]){ used[slug]++; slug = slug + "-" + used[slug]; } else { used[slug] = 1; }
      return '<h' + level + ' id="' + slug + '">' + text + '</h' + level + '>';
    };
    renderer.table = function(header, body2){
      return '<div class="table-wrap"><table><thead>' + header + '</thead><tbody>' + body2 + '</tbody></table></div>';
    };

    marked.setOptions({ renderer: renderer, gfm: true, breaks: false });
    body.innerHTML = marked.parse(NOTES_MD);

    // Remove the first H1 from the body (module title is already in the page header) and skip it in TOC
    const firstH1 = body.querySelector("h1");
    if(firstH1) firstH1.remove();

    if(tocEl){
      const headings = Array.from(body.querySelectorAll("h2"));
      if(headings.length){
        let toc = "<h4>On this page</h4>";
        headings.forEach(h=>{
          toc += '<a href="#' + h.id + '">' + h.textContent + '</a>';
        });
        tocEl.innerHTML = toc;
      }
    }
  }
  window.renderNotes = renderNotes;
})();
