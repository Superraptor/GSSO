/**
 * GSSO Web Portal Application Controller
 * Handles SPA hash routing, theme switching, ontology term rendering, and external mappings.
 */

class GSSOApp {
  constructor() {
    this.meta = null;
    this.terms = null;
    this.searchEngine = null;
    this.detector = null;
    this.hierarchyTree = null;
    this.currentTermId = null;

    this.init();
  }

  async init() {
    this.initTheme();
    await this.loadMeta();

    // Initialize search engine
    this.searchEngine = new window.GSSOSearchEngine();

    // Initialize detector & tree
    this.detector = new window.GSSODetector(this);
    this.hierarchyTree = new window.GSSOHierarchyTree(this);

    // Bind navigation & hash changes
    this.bindEvents();
    this.handleRoute();

    // Preload terms in background after initial render
    setTimeout(() => {
      this.loadFullTerms();
    }, 200);
  }

  initTheme() {
    const savedTheme = localStorage.getItem('gsso-theme') || 'dark';
    document.documentElement.setAttribute('data-theme', savedTheme);
    this.updateThemeIcon(savedTheme);

    const toggleBtn = document.getElementById('theme-toggle');
    if (toggleBtn) {
      toggleBtn.addEventListener('click', () => {
        const current = document.documentElement.getAttribute('data-theme') || 'dark';
        const next = current === 'dark' ? 'light' : 'dark';
        document.documentElement.setAttribute('data-theme', next);
        localStorage.setItem('gsso-theme', next);
        this.updateThemeIcon(next);
      });
    }
  }

  updateThemeIcon(theme) {
    const iconEl = document.getElementById('theme-icon');
    if (iconEl) {
      iconEl.textContent = theme === 'dark' ? '🌙' : '☀️';
    }
  }

  async loadMeta() {
    try {
      const res = await fetch('data/meta.json');
      if (res.ok) {
        this.meta = await res.json();
        this.renderStats();
        this.renderFeaturedCategories();
      }
    } catch (err) {
      console.error('Failed to load meta.json', err);
    }
  }

  async loadFullTerms() {
    if (this.terms) return this.terms;
    try {
      const res = await fetch('data/gsso_terms.json');
      if (res.ok) {
        this.terms = await res.json();
        console.log(`Loaded ${Object.keys(this.terms).length} GSSO terms into memory.`);
      }
    } catch (err) {
      console.error('Failed to load gsso_terms.json', err);
    }
    return this.terms;
  }

  renderStats() {
    if (!this.meta) return;
    const termCountEl = document.getElementById('stat-terms-count');
    const edgeCountEl = document.getElementById('stat-edges-count');
    const versionEl = document.getElementById('stat-version');

    if (termCountEl) termCountEl.textContent = this.meta.total_terms.toLocaleString();
    if (edgeCountEl) edgeCountEl.textContent = this.meta.total_edges.toLocaleString();
    if (versionEl) versionEl.textContent = `v${this.meta.version}`;
  }

  renderFeaturedCategories() {
    if (!this.meta || !this.meta.featured_categories) return;
    const gridEl = document.getElementById('featured-categories-grid');
    if (!gridEl) return;

    let html = '';
    this.meta.featured_categories.forEach(cat => {
      html += `
        <div class="category-card" data-id="${cat.id}">
          <div class="category-card-top">
            <div class="category-icon-box">
              <span style="font-size: 1.35rem;">★</span>
            </div>
            <div>
              <h3 class="category-title">${this.escapeHtml(cat.name)}</h3>
              <p class="category-description">${this.escapeHtml(cat.description)}</p>
            </div>
          </div>
          <div class="category-footer">
            <span>Root: <strong style="font-family: var(--font-mono); color: var(--accent-purple);">${cat.id}</strong></span>
            <span class="category-link">Explore branch &rarr;</span>
          </div>
        </div>
      `;
    });

    gridEl.innerHTML = html;

    gridEl.querySelectorAll('.category-card').forEach(card => {
      card.addEventListener('click', () => {
        const id = card.getAttribute('data-id');
        window.location.hash = `#!/entry/${id}`;
      });
    });
  }

  bindEvents() {
    window.addEventListener('hashchange', () => {
      this.handleRoute();
    });

    // Quick filter pills
    document.querySelectorAll('.quick-pill').forEach(pill => {
      pill.addEventListener('click', (e) => {
        const term = e.target.getAttribute('data-search');
        if (term) {
          const searchInput = document.getElementById('search-input');
          if (searchInput) {
            searchInput.value = term;
            this.searchEngine.handleSearch(term);
            searchInput.focus();
          }
        }
      });
    });

    // Delegated copy button for IRI
    document.addEventListener('click', (e) => {
      const copyBtn = e.target.closest('.btn-copy-iri');
      if (copyBtn) {
        const iri = copyBtn.getAttribute('data-iri');
        if (iri) {
          navigator.clipboard.writeText(iri).then(() => {
            this.showToast('Copied PURL IRI to clipboard!');
          });
        }
      }
    });
  }

  handleRoute() {
    const hash = window.location.hash || '#!/';
    const navLinks = document.querySelectorAll('.nav-link');

    // Update active nav link
    navLinks.forEach(link => {
      const href = link.getAttribute('href');
      if (href && (hash === href || (href !== '#!/' && hash.startsWith(href)))) {
        link.classList.add('active');
      } else {
        link.classList.remove('active');
      }
    });

    // 1. Check entry route with query param: #!/entry?iri=... (matches CCHMC / PURL format)
    if (hash.startsWith('#!/entry?iri=') || hash.startsWith('#/entry?iri=')) {
      const iriParam = decodeURIComponent(hash.split('?iri=')[1] || '').trim();
      this.showView('explorer');
      this.resolveAndRenderIri(iriParam);
      return;
    }

    // 2. Check entry route with ID: #!/entry/GSSO_000130
    if (hash.startsWith('#!/entry/') || hash.startsWith('#/entry/')) {
      const termId = hash.replace(/#\!?\/entry\//, '').trim();
      this.showView('explorer');
      this.renderTermDetail(termId);
      return;
    }

    // 3. Text Detector view: #!/detector
    if (hash.startsWith('#!/detector') || hash.startsWith('#/detector')) {
      this.showView('detector');
      return;
    }

    // 4. Hierarchy Tree view: #!/tree
    if (hash.startsWith('#!/tree') || hash.startsWith('#/tree')) {
      this.showView('tree');
      this.hierarchyTree.render();
      return;
    }

    // 5. Cross-Walk Mappings view: #!/mappings
    if (hash.startsWith('#!/mappings') || hash.startsWith('#/mappings')) {
      this.showView('mappings');
      this.renderMappingsView();
      return;
    }

    // 6. Downloads & Releases view: #!/downloads
    if (hash.startsWith('#!/downloads') || hash.startsWith('#/downloads')) {
      this.showView('downloads');
      return;
    }

    // 7. About view: #!/about
    if (hash.startsWith('#!/about') || hash.startsWith('#/about')) {
      this.showView('about');
      return;
    }

    // Default: Home Explorer
    this.showView('explorer');
    const detailContainer = document.getElementById('term-detail-container');
    if (detailContainer) {
      detailContainer.innerHTML = '';
      detailContainer.style.display = 'none';
    }
  }

  showView(viewName) {
    document.querySelectorAll('.view-section').forEach(sec => {
      sec.classList.remove('active');
    });

    const targetSec = document.getElementById(`view-${viewName}`);
    if (targetSec) {
      targetSec.classList.add('active');
    }

    // Scroll to top
    window.scrollTo({ top: 0, behavior: 'smooth' });
  }

  async resolveAndRenderIri(iri) {
    if (!iri) return;
    await this.loadFullTerms();

    // Check if IRI ends with a GSSO ID (e.g. http://purl.obolibrary.org/obo/GSSO_000130)
    const match = iri.match(/GSSO[_:](\d+)/i);
    if (match) {
      const termId = `GSSO_${match[1]}`;
      this.renderTermDetail(termId);
      return;
    }

    // Check if IRI is an external mapping (e.g. Homosaurus URI)
    if (this.terms) {
      for (const [id, term] of Object.entries(this.terms)) {
        if (term.maps) {
          for (const list of Object.values(term.maps)) {
            if (list.includes(iri)) {
              this.renderTermDetail(id);
              return;
            }
          }
        }
      }
    }

    this.renderNotFound(iri);
  }

  async renderTermDetail(termId) {
    const detailContainer = document.getElementById('term-detail-container');
    if (!detailContainer) return;

    detailContainer.style.display = 'block';
    detailContainer.innerHTML = `
      <div style="text-align: center; padding: 3rem; color: var(--text-secondary);">
        Loading details for <strong>${this.escapeHtml(termId)}</strong>...
      </div>
    `;

    await this.loadFullTerms();

    // Normalize termId
    let targetId = termId.replace(':', '_').toUpperCase();
    if (!targetId.startsWith('GSSO_') && /^\d+$/.test(targetId)) {
      targetId = `GSSO_${targetId.padStart(6, '0')}`;
    }

    const term = this.terms ? this.terms[targetId] : null;

    if (!term) {
      this.renderNotFound(termId);
      return;
    }

    this.currentTermId = targetId;

    // Build PURL link
    const purl = `http://purl.obolibrary.org/obo/${targetId}`;

    // Render term card
    let html = `
      <div class="term-detail-wrapper" id="term-${targetId}">
        <div class="term-header">
          <div class="term-title-block">
            <h2>${this.escapeHtml(term.lbl)}</h2>
            <div class="term-meta-badges">
              <span class="id-badge">${targetId}</span>
              <span style="font-family: var(--font-mono); font-size: 0.8rem; color: var(--text-muted);">${purl}</span>
            </div>
          </div>
          <div class="term-actions-bar">
            <button class="btn btn-secondary btn-copy-iri" data-iri="${purl}" title="Copy Canonical PURL IRI">
              📋 Copy PURL
            </button>
            <a href="http://www.ontobee.org/ontology/GSSO?iri=${encodeURIComponent(purl)}" target="_blank" rel="noopener" class="btn btn-secondary" title="View on Ontobee">
              Ontobee ↗
            </a>
            <a href="https://bioportal.bioontology.org/ontologies/GSSO/?p=classes&conceptid=${encodeURIComponent(purl)}" target="_blank" rel="noopener" class="btn btn-secondary" title="View on NCBO BioPortal">
              BioPortal ↗
            </a>
            <a href="https://lgbtdb.wikibase.cloud/" target="_blank" rel="noopener" class="btn btn-primary" title="Contribute on lgbtDB for GSSO 3.0.0">
              lgbtDB (v3.0.0) ↗
            </a>
          </div>
        </div>

        ${term.def ? `
          <div class="term-definition-box">
            <div style="font-size: 0.75rem; text-transform: uppercase; font-weight: 700; color: var(--accent-purple); margin-bottom: 0.35rem; letter-spacing: 0.05em;">Definition</div>
            <p>${this.escapeHtml(term.def)}</p>
          </div>
        ` : ''}

        ${term.comm && term.comm.length > 0 ? `
          <div class="detail-section">
            <div class="detail-section-title">Usage & Linguistic Notes</div>
            <ul class="term-comments-list">
              ${term.comm.map(c => `<li>${this.escapeHtml(c)}</li>`).join('')}
            </ul>
          </div>
        ` : ''}

        ${term.syn && term.syn.all && term.syn.all.length > 0 ? `
          <div class="detail-section">
            <div class="detail-section-title">Synonyms & Alternate Names (${term.syn.all.length})</div>
            <div class="pill-container">
              ${term.syn.exact.map(s => `<span class="synonym-pill exact" title="Exact Synonym">${this.escapeHtml(s)}</span>`).join('')}
              ${term.syn.related.map(s => `<span class="synonym-pill" title="Related Synonym">${this.escapeHtml(s)}</span>`).join('')}
              ${term.syn.narrow.map(s => `<span class="synonym-pill" title="Narrow Synonym">${this.escapeHtml(s)}</span>`).join('')}
              ${term.syn.broad.map(s => `<span class="synonym-pill" title="Broad Synonym">${this.escapeHtml(s)}</span>`).join('')}
            </div>
          </div>
        ` : ''}

        <!-- Parents / Superclasses -->
        <div class="detail-section">
          <div class="detail-section-title">Superclasses (Ancestors)</div>
          ${term.par && term.par.length > 0 ? `
            <div class="hierarchy-links-grid">
              ${term.par.map(p => `
                <a href="#!/entry/${p.id}" class="hierarchy-item-btn">
                  <span>${this.escapeHtml(p.lbl)}</span>
                  <span class="id">${p.id}</span>
                </a>
              `).join('')}
            </div>
          ` : `<div style="font-size: 0.85rem; color: var(--text-muted);">Root entity (no asserted parent classes)</div>`}
        </div>

        <!-- Children / Subclasses -->
        <div class="detail-section">
          <div class="detail-section-title">Subclasses (Direct Descendants) (${term.ch ? term.ch.length : 0})</div>
          ${term.ch && term.ch.length > 0 ? `
            <div class="hierarchy-links-grid">
              ${term.ch.map(c => `
                <a href="#!/entry/${c.id}" class="hierarchy-item-btn">
                  <span>${this.escapeHtml(c.lbl)}</span>
                  <span class="id">${c.id}</span>
                </a>
              `).join('')}
            </div>
          ` : `<div style="font-size: 0.85rem; color: var(--text-muted);">Leaf term (no child classes)</div>`}
        </div>

        <!-- External Mappings & Cross-References -->
        ${term.maps && Object.keys(term.maps).length > 0 ? `
          <div class="detail-section">
            <div class="detail-section-title">External Vocabulary Mappings & Cross-References</div>
            <div class="mappings-badge-grid">
              ${Object.entries(term.maps).flatMap(([source, links]) => 
                links.map(link => `
                  <a href="${this.escapeHtml(link)}" target="_blank" rel="noopener" class="mapping-tag">
                    <span style="color: var(--accent-indigo); font-weight: 700;">${this.escapeHtml(source)}:</span>
                    <span>${this.escapeHtml(link.split('/').pop())}</span>
                    <span style="font-size: 0.7rem;">↗</span>
                  </a>
                `)
              ).join('')}
            </div>
          </div>
        ` : ''}
      </div>
    `;

    detailContainer.innerHTML = html;
    detailContainer.scrollIntoView({ behavior: 'smooth', block: 'start' });
  }

  renderNotFound(query) {
    const detailContainer = document.getElementById('term-detail-container');
    if (!detailContainer) return;

    detailContainer.style.display = 'block';
    detailContainer.innerHTML = `
      <div class="term-detail-wrapper" style="text-align: center; padding: 3rem 1.5rem;">
        <h3 style="font-family: var(--font-heading); font-size: 1.5rem; color: var(--accent-rose); margin-bottom: 0.5rem;">
          Term Not Found
        </h3>
        <p style="color: var(--text-secondary); max-width: 500px; margin: 0 auto 1.5rem;">
          No GSSO concept or external mapping matched "<strong>${this.escapeHtml(query)}</strong>".
        </p>
        <a href="#!/" class="btn btn-primary">&larr; Return to Explorer</a>
      </div>
    `;
  }

  async renderMappingsView() {
    const tableBodyEl = document.getElementById('mappings-table-body');
    if (!tableBodyEl) return;

    tableBodyEl.innerHTML = `<tr><td colspan="4" style="text-align:center; padding: 2rem; color: var(--text-secondary);">Loading mapped vocabulary crosswalks...</td></tr>`;
    await this.loadFullTerms();

    const sampleRows = [];
    for (const [id, term] of Object.entries(this.terms)) {
      if (term.maps && Object.keys(term.maps).length > 0) {
        for (const [source, links] of Object.entries(term.maps)) {
          sampleRows.push({
            id,
            lbl: term.lbl,
            source,
            link: links[0]
          });
          if (sampleRows.length >= 100) break;
        }
      }
      if (sampleRows.length >= 100) break;
    }

    let html = '';
    sampleRows.forEach(row => {
      html += `
        <tr>
          <td><a href="#!/entry/${row.id}" style="font-family: var(--font-mono); font-weight:600;">${row.id}</a></td>
          <td>${this.escapeHtml(row.lbl)}</td>
          <td><span class="brand-badge">${this.escapeHtml(row.source)}</span></td>
          <td><a href="${this.escapeHtml(row.link)}" target="_blank" rel="noopener" style="font-family: var(--font-mono); font-size: 0.8rem;">${this.escapeHtml(row.link)} ↗</a></td>
        </tr>
      `;
    });

    tableBodyEl.innerHTML = html;
  }

  showToast(message) {
    let toastEl = document.getElementById('app-toast');
    if (!toastEl) {
      toastEl = document.createElement('div');
      toastEl.id = 'app-toast';
      toastEl.className = 'toast-notice';
      document.body.appendChild(toastEl);
    }

    toastEl.textContent = message;
    toastEl.classList.add('show');

    setTimeout(() => {
      toastEl.classList.remove('show');
    }, 2800);
  }

  escapeHtml(str) {
    return String(str || '')
      .replace(/&/g, '&amp;')
      .replace(/</g, '&lt;')
      .replace(/>/g, '&gt;')
      .replace(/"/g, '&quot;');
  }
}

// Instantiate on DOM ready
document.addEventListener('DOMContentLoaded', () => {
  window.app = new GSSOApp();
});
