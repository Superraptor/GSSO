/**
 * GSSO Instant Client-Side Search Engine
 * High-performance prefix and substring matching across GSSO labels, IDs, and synonyms.
 */

class GSSOSearchEngine {
  constructor() {
    this.index = [];
    this.isLoaded = false;
    this.selectedIndex = -1;
    this.currentResults = [];

    this.inputEl = document.getElementById('search-input');
    this.dropdownEl = document.getElementById('search-dropdown');
    this.containerEl = document.getElementById('search-container');

    this.init();
  }

  async init() {
    if (!this.inputEl || !this.dropdownEl) return;

    try {
      const res = await fetch('data/search_index.json');
      if (res.ok) {
        this.index = await res.json();
        this.isLoaded = true;
      }
    } catch (err) {
      console.warn('Search index deferred, loading from main dataset...', err);
    }

    this.bindEvents();
  }

  bindEvents() {
    let debounceTimer;

    this.inputEl.addEventListener('input', (e) => {
      clearTimeout(debounceTimer);
      debounceTimer = setTimeout(() => {
        this.handleSearch(e.target.value.trim());
      }, 100);
    });

    this.inputEl.addEventListener('keydown', (e) => {
      this.handleKeydown(e);
    });

    this.inputEl.addEventListener('focus', () => {
      if (this.inputEl.value.trim().length >= 2) {
        this.showDropdown();
      }
    });

    document.addEventListener('click', (e) => {
      if (!this.containerEl.contains(e.target)) {
        this.hideDropdown();
      }
    });

    // Global shortcut '/' to focus search
    document.addEventListener('keydown', (e) => {
      if (e.key === '/' && document.activeElement !== this.inputEl && !['INPUT', 'TEXTAREA'].includes(document.activeElement.tagName)) {
        e.preventDefault();
        this.inputEl.focus();
        this.inputEl.select();
      }
    });
  }

  handleSearch(query) {
    if (!query || query.length < 2) {
      this.hideDropdown();
      return;
    }

    const q = query.toLowerCase();
    const results = [];
    const maxResults = 12;

    // 1. Exact ID match check (e.g. "GSSO_000130" or "000130" or "GSSO:000130")
    const cleanId = q.replace(':', '_').toUpperCase();
    for (let i = 0; i < this.index.length; i++) {
      const item = this.index[i];
      if (item.id === cleanId || item.id.endsWith(cleanId)) {
        results.push({ item, score: 100, matchType: 'id' });
        break;
      }
    }

    // 2. Label prefix and substring match
    for (let i = 0; i < this.index.length; i++) {
      if (results.length >= maxResults) break;
      const item = this.index[i];
      if (results.some(r => r.item.id === item.id)) continue;

      const lbl = item.l.toLowerCase();
      if (lbl === q) {
        results.unshift({ item, score: 90, matchType: 'exact-label' });
      } else if (lbl.startsWith(q)) {
        results.push({ item, score: 80, matchType: 'prefix-label' });
      } else if (lbl.includes(q)) {
        results.push({ item, score: 60, matchType: 'sub-label' });
      } else if (item.s && item.s.some(s => s.toLowerCase().startsWith(q))) {
        results.push({ item, score: 50, matchType: 'synonym-prefix' });
      } else if (item.s && item.s.some(s => s.toLowerCase().includes(q))) {
        results.push({ item, score: 40, matchType: 'synonym-sub' });
      }
    }

    results.sort((a, b) => b.score - a.score);
    this.currentResults = results.slice(0, maxResults);
    this.selectedIndex = -1;
    this.renderDropdown(query);
  }

  renderDropdown(query) {
    if (this.currentResults.length === 0) {
      this.dropdownEl.innerHTML = `
        <div style="padding: 1rem; text-align: center; color: var(--text-muted); font-size: 0.9rem;">
          No matching GSSO terms found for "<strong>${this.escapeHtml(query)}</strong>"
        </div>
      `;
      this.showDropdown();
      return;
    }

    let html = '';
    this.currentResults.forEach((res, idx) => {
      const item = res.item;
      const synonymsText = item.s && item.s.length > 0 ? item.s.slice(0, 3).join(', ') : '';

      html += `
        <div class="search-result-item" data-index="${idx}" data-id="${item.id}" id="search-opt-${idx}">
          <div class="search-result-header">
            <span class="search-result-label">${this.highlightMatch(item.l, query)}</span>
            <span class="search-result-id">${item.id}</span>
          </div>
          ${synonymsText ? `<div class="search-result-synonyms">aka: ${this.highlightMatch(synonymsText, query)}</div>` : ''}
        </div>
      `;
    });

    this.dropdownEl.innerHTML = html;
    this.showDropdown();

    // Attach click events
    this.dropdownEl.querySelectorAll('.search-result-item').forEach(el => {
      el.addEventListener('click', () => {
        const termId = el.getAttribute('data-id');
        this.selectTerm(termId);
      });
    });
  }

  handleKeydown(e) {
    if (!this.dropdownEl.style.display || this.dropdownEl.style.display === 'none') {
      if (e.key === 'ArrowDown') {
        this.handleSearch(this.inputEl.value.trim());
      }
      return;
    }

    if (e.key === 'ArrowDown') {
      e.preventDefault();
      this.selectedIndex = Math.min(this.selectedIndex + 1, this.currentResults.length - 1);
      this.updateSelectionVisuals();
    } else if (e.key === 'ArrowUp') {
      e.preventDefault();
      this.selectedIndex = Math.max(this.selectedIndex - 1, 0);
      this.updateSelectionVisuals();
    } else if (e.key === 'Enter') {
      e.preventDefault();
      if (this.selectedIndex >= 0 && this.selectedIndex < this.currentResults.length) {
        this.selectTerm(this.currentResults[this.selectedIndex].item.id);
      } else if (this.currentResults.length > 0) {
        this.selectTerm(this.currentResults[0].item.id);
      }
    } else if (e.key === 'Escape') {
      this.hideDropdown();
    }
  }

  updateSelectionVisuals() {
    const items = this.dropdownEl.querySelectorAll('.search-result-item');
    items.forEach((item, idx) => {
      if (idx === this.selectedIndex) {
        item.classList.add('selected');
        item.scrollIntoView({ block: 'nearest' });
      } else {
        item.classList.remove('selected');
      }
    });
  }

  selectTerm(termId) {
    this.hideDropdown();
    window.location.hash = `#!/entry/${termId}`;
  }

  showDropdown() {
    this.dropdownEl.style.display = 'block';
  }

  hideDropdown() {
    this.dropdownEl.style.display = 'none';
    this.selectedIndex = -1;
  }

  highlightMatch(text, query) {
    if (!query) return this.escapeHtml(text);
    const regex = new RegExp(`(${query.replace(/[.*+?^${}()|[\]\\]/g, '\\$&')})`, 'gi');
    return this.escapeHtml(text).replace(regex, '<span style="color: var(--accent-pink); font-weight:700;">$1</span>');
  }

  escapeHtml(str) {
    return String(str || '')
      .replace(/&/g, '&amp;')
      .replace(/</g, '&lt;')
      .replace(/>/g, '&gt;')
      .replace(/"/g, '&quot;');
  }
}

window.GSSOSearchEngine = GSSOSearchEngine;
