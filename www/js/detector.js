/**
 * GSSO Text Annotation / Detector Tool
 * Replaces https://gsso.research.cchmc.org/#!/detector
 * Scans raw clinical, research, or sociological text, detects GSSO concepts,
 * and highlights them with interactive tooltips and links.
 */

class GSSODetector {
  constructor(app) {
    this.app = app;
    this.dictionary = []; // Array of { phrase, id, len, lbl } sorted by length descending
    this.isReady = false;

    this.inputEl = document.getElementById('detector-input');
    this.outputEl = document.getElementById('detector-output');
    this.summaryEl = document.getElementById('detector-summary');
    this.annotateBtn = document.getElementById('btn-run-detector');

    this.init();
  }

  async init() {
    if (!this.inputEl || !this.annotateBtn) return;
    this.bindEvents();
  }

  buildDictionary() {
    if (this.isReady || !this.app.terms) return;

    const phrases = new Map();

    // Index all labels and synonyms with at least 3 characters
    for (const [id, term] of Object.entries(this.app.terms)) {
      if (term.lbl && term.lbl.length >= 3) {
        phrases.set(term.lbl.toLowerCase(), { id, lbl: term.lbl });
      }
      if (term.syn && term.syn.all) {
        for (const s of term.syn.all) {
          if (s && s.length >= 3 && !phrases.has(s.toLowerCase())) {
            phrases.set(s.toLowerCase(), { id, lbl: term.lbl });
          }
        }
      }
    }

    // Sort by phrase length descending for greedy longest-first matching
    this.dictionary = Array.from(phrases.entries())
      .map(([phrase, info]) => ({
        phrase,
        id: info.id,
        lbl: info.lbl,
        len: phrase.length
      }))
      .sort((a, b) => b.len - a.len);

    this.isReady = true;
  }

  bindEvents() {
    this.annotateBtn.addEventListener('click', () => {
      this.runDetection();
    });

    // Sample buttons
    document.querySelectorAll('.sample-btn').forEach(btn => {
      btn.addEventListener('click', (e) => {
        const type = e.target.getAttribute('data-sample');
        this.loadSample(type);
      });
    });

    // Delegated click on detected mentions in output box
    this.outputEl.addEventListener('click', (e) => {
      const mention = e.target.closest('.gsso-mention');
      if (mention) {
        const id = mention.getAttribute('data-id');
        if (id) {
          window.location.hash = `#!/entry/${id}`;
        }
      }
    });
  }

  loadSample(type) {
    if (type === 'clinical') {
      this.inputEl.value = `Patient is a 24-year-old transgender woman who presents to the clinic for gender-affirming hormone therapy evaluation (prescribed estradiol and spironolactone). She uses she/her pronouns, reports history of gender dysphoria since adolescence, and has legally updated her name and gender marker. She is accompanied and supported by her cisgender partner.`;
    } else if (type === 'sociological') {
      this.inputEl.value = `This qualitative study interviewed nonbinary, genderqueer, agender, and asexual young adults across diverse regional settings. Participants highlighted evolving terminology within queer communities, reclaiming historical descriptors such as butch and femme, alongside indigenous concepts such as two-spirit, while navigating societal barriers around sexual orientation and gender expression.`;
    } else if (type === 'biomedical') {
      this.inputEl.value = `Analysis of endocrine pathways during pubertal development and antiandrogen administration. Biological sex characteristics, including karyotype, gonadal morphology, and secondary sex characteristics, were monitored longitudinally alongside patient-reported psychological wellness.`;
    }
    this.runDetection();
  }

  async runDetection() {
    const rawText = this.inputEl.value.trim();
    if (!rawText) {
      this.outputEl.innerHTML = '<span style="color: var(--text-muted); font-style: italic;">Please enter or paste text above, or click one of the preset sample buttons.</span>';
      this.summaryEl.innerHTML = '';
      return;
    }

    // Ensure terms are loaded
    if (!this.app.terms) {
      this.outputEl.innerHTML = '<div style="color: var(--text-secondary); text-align: center; padding: 2rem;">Loading ontology terms...</div>';
      await this.app.loadFullTerms();
    }

    this.buildDictionary();

    this.outputEl.innerHTML = '<div style="color: var(--text-secondary); text-align: center; padding: 2rem;">Annotating text with GSSO concepts...</div>';

    // Greedy phrase matching
    const lowerText = rawText.toLowerCase();
    const matchedSpans = []; // { start, end, id, lbl, phrase }

    for (let i = 0; i < this.dictionary.length; i++) {
      const item = this.dictionary[i];
      let searchPos = 0;

      while (searchPos < lowerText.length) {
        const foundPos = lowerText.indexOf(item.phrase, searchPos);
        if (foundPos === -1) break;

        const endPos = foundPos + item.len;

        // Check word boundaries
        const charBefore = foundPos > 0 ? lowerText[foundPos - 1] : ' ';
        const charAfter = endPos < lowerText.length ? lowerText[endPos] : ' ';

        const isBoundaryBefore = /[\s\.,;:!?\(\)\[\]"'\/\-]/.test(charBefore);
        const isBoundaryAfter = /[\s\.,;:!?\(\)\[\]"'\/\-]/.test(charAfter);

        if (isBoundaryBefore && isBoundaryAfter) {
          // Check for overlap with already accepted longer phrases
          const overlaps = matchedSpans.some(span => 
            (foundPos >= span.start && foundPos < span.end) ||
            (endPos > span.start && endPos <= span.end)
          );

          if (!overlaps) {
            matchedSpans.push({
              start: foundPos,
              end: endPos,
              id: item.id,
              lbl: item.lbl,
              phrase: item.phrase
            });
          }
        }

        searchPos = foundPos + 1;
      }
    }

    // Sort matches by position
    matchedSpans.sort((a, b) => a.start - b.start);

    // Build highlighted HTML string
    let htmlResult = '';
    let lastIdx = 0;
    const termCounts = new Map();

    matchedSpans.forEach(match => {
      // Append preceding unannotated text
      htmlResult += this.escapeHtml(rawText.substring(lastIdx, match.start));

      // Append highlighted mention
      const matchedText = rawText.substring(match.start, match.end);
      const term = this.app.terms[match.id] || {};
      const def = term.def || 'GSSO ontology concept';

      htmlResult += `<span class="gsso-mention" data-id="${match.id}" title="${this.escapeHtml(term.lbl || match.lbl)} (${match.id}): ${this.escapeHtml(def)}">${this.escapeHtml(matchedText)}</span>`;

      lastIdx = match.end;

      // Track counts
      const cur = termCounts.get(match.id) || { id: match.id, lbl: term.lbl || match.lbl, count: 0, def };
      cur.count += 1;
      termCounts.set(match.id, cur);
    });

    htmlResult += this.escapeHtml(rawText.substring(lastIdx));
    this.outputEl.innerHTML = htmlResult;

    // Render detected terms summary
    this.renderSummary(termCounts);
  }

  renderSummary(termCounts) {
    if (termCounts.size === 0) {
      this.summaryEl.innerHTML = `
        <div style="color: var(--text-muted); font-size: 0.9rem;">
          No GSSO terms detected in this text.
        </div>
      `;
      return;
    }

    const sortedTerms = Array.from(termCounts.values()).sort((a, b) => b.count - a.count);

    let html = `
      <div style="display: flex; align-items: center; justify-content: space-between; margin-bottom: 0.75rem;">
        <h4 style="font-family: var(--font-heading); font-size: 1.1rem; color: var(--text-primary);">
          Detected Concepts (${termCounts.size} unique terms)
        </h4>
        <button id="btn-copy-detected" class="btn btn-secondary" style="font-size: 0.75rem; padding: 0.25rem 0.6rem;">
          Copy Term List
        </button>
      </div>
      <div style="display: flex; flex-wrap: wrap; gap: 0.5rem;">
    `;

    sortedTerms.forEach(t => {
      html += `
        <a href="#!/entry/${t.id}" class="mapping-tag" title="${this.escapeHtml(t.def)}">
          <strong>${this.escapeHtml(t.lbl)}</strong>
          <span style="font-family: var(--font-mono); font-size: 0.75rem; color: var(--accent-purple);">${t.id}</span>
          ${t.count > 1 ? `<span style="font-size: 0.7rem; background: var(--border-medium); padding: 0.1rem 0.35rem; border-radius: var(--radius-full);">${t.count}x</span>` : ''}
        </a>
      `;
    });

    html += `</div>`;
    this.summaryEl.innerHTML = html;

    const copyBtn = document.getElementById('btn-copy-detected');
    if (copyBtn) {
      copyBtn.addEventListener('click', () => {
        const textList = sortedTerms.map(t => `- ${t.lbl} (${t.id}): ${t.def}`).join('\n');
        navigator.clipboard.writeText(textList).then(() => {
          this.app.showToast('Copied detected term list to clipboard!');
        });
      });
    }
  }

  escapeHtml(str) {
    return String(str || '')
      .replace(/&/g, '&amp;')
      .replace(/</g, '&lt;')
      .replace(/>/g, '&gt;')
      .replace(/"/g, '&quot;');
  }
}

window.GSSODetector = GSSODetector;
