/**
 * GSSO Interactive Hierarchy Tree Browser
 * Expandable ontology tree viewer with dynamic children loading.
 */

class GSSOHierarchyTree {
  constructor(app) {
    this.app = app;
    this.containerEl = document.getElementById('tree-view-container');
    this.isInitialized = false;

    // Key thematic root nodes to display initially
    this.rootIds = [
      'GSSO_005835', // LGBTQ persons
      'GSSO_011889', // persons organized in relationship to gender
      'GSSO_002024', // gendered person
      'GSSO_003283', // personal identity
      'GSSO_000484', // health condition
      'GSSO_006233', // medical process
      'GSSO_000029', // social process
      'GSSO_000492', // knowledge content entity
      'GSSO_000721'  // biological interaction
    ];
  }

  async render() {
    if (!this.containerEl) return;

    if (!this.app.terms) {
      this.containerEl.innerHTML = '<div style="color: var(--text-secondary); text-align: center; padding: 2rem;">Loading ontology hierarchy...</div>';
      await this.app.loadFullTerms();
    }

    this.containerEl.innerHTML = '';
    const rootListEl = document.createElement('div');
    rootListEl.className = 'tree-root-list';

    this.rootIds.forEach(id => {
      const term = this.app.terms[id];
      if (term) {
        rootListEl.appendChild(this.createTreeNode(term, 0));
      }
    });

    this.containerEl.appendChild(rootListEl);
  }

  createTreeNode(term, depth) {
    const nodeEl = document.createElement('div');
    nodeEl.className = 'tree-node';
    nodeEl.setAttribute('data-id', term.id);

    const hasChildren = term.ch && term.ch.length > 0;
    const childCount = hasChildren ? term.ch.length : 0;

    const contentEl = document.createElement('div');
    contentEl.className = 'tree-node-content';
    contentEl.innerHTML = `
      <span class="tree-expand-toggle">${hasChildren ? '▶' : '•'}</span>
      <span class="tree-node-label">${this.escapeHtml(term.lbl)}</span>
      <span class="tree-node-id">${term.id}</span>
      ${hasChildren ? `<span style="font-size: 0.75rem; color: var(--text-muted); background: var(--bg-surface-elevated); padding: 0.1rem 0.4rem; border-radius: var(--radius-full);">${childCount}</span>` : ''}
    `;

    const childrenContainer = document.createElement('div');
    childrenContainer.className = 'tree-children-container';
    childrenContainer.style.display = 'none';

    // Toggle expand/collapse
    contentEl.querySelector('.tree-expand-toggle').addEventListener('click', (e) => {
      e.stopPropagation();
      this.toggleNode(nodeEl, term, childrenContainer, depth);
    });

    // Click label to view in entry details
    contentEl.addEventListener('click', () => {
      window.location.hash = `#!/entry/${term.id}`;
    });

    nodeEl.appendChild(contentEl);
    nodeEl.appendChild(childrenContainer);

    return nodeEl;
  }

  toggleNode(nodeEl, term, childrenContainer, depth) {
    const toggleIcon = nodeEl.querySelector('.tree-expand-toggle');
    const isExpanded = childrenContainer.style.display === 'block';

    if (isExpanded) {
      childrenContainer.style.display = 'none';
      toggleIcon.textContent = '▶';
    } else {
      // Lazy render children if empty
      if (childrenContainer.children.length === 0 && term.ch && term.ch.length > 0) {
        term.ch.forEach(chRef => {
          const childTerm = this.app.terms[chRef.id];
          if (childTerm) {
            childrenContainer.appendChild(this.createTreeNode(childTerm, depth + 1));
          } else {
            // Render placeholder child with label
            const simpleNode = document.createElement('div');
            simpleNode.className = 'tree-node';
            simpleNode.innerHTML = `
              <div class="tree-node-content">
                <span class="tree-expand-toggle">•</span>
                <span class="tree-node-label">${this.escapeHtml(chRef.lbl)}</span>
                <span class="tree-node-id">${chRef.id}</span>
              </div>
            `;
            simpleNode.querySelector('.tree-node-content').addEventListener('click', () => {
              window.location.hash = `#!/entry/${chRef.id}`;
            });
            childrenContainer.appendChild(simpleNode);
          }
        });
      }

      childrenContainer.style.display = 'block';
      toggleIcon.textContent = '▼';
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

window.GSSOHierarchyTree = GSSOHierarchyTree;
