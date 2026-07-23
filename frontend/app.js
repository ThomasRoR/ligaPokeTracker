/**
 * Pokémon Price Tracker - Main Application Logic (`app.js`)
 * Connects UI elements to `supabaseClient.js`
 */

let allCards = [];
let currentExpansions = [];

/**
 * Formats price number into Brazilian Real (R$) currency format
 */
function formatCurrency(val) {
  if (val === null || val === undefined || isNaN(val)) return 'N/A';
  return `R$ ${Number(val).toFixed(2).replace('.', ',')}`;
}

/**
 * Formats ISO date timestamp to readable locale date string
 */
function formatDate(isoStr) {
  if (!isoStr) return 'N/A';
  try {
    const d = new Date(isoStr);
    return d.toLocaleDateString('pt-BR', {
      day: '2-digit',
      month: '2-digit',
      year: 'numeric'
    });
  } catch (e) {
    return isoStr;
  }
}

/**
 * Populates expansion dropdown selector
 */
async function loadExpansions() {
  const select = document.getElementById('expansion-filter');
  if (!select) return;

  try {
    const expansions = await window.supabaseTrackerClient.fetchExpansions();
    currentExpansions = expansions || [];

    // Preserving default options while dynamically enriching codes if needed
    const existingValues = Array.from(select.options).map(o => o.value);
    
    currentExpansions.forEach(exp => {
      const expName = exp.name || exp.code;
      if (!existingValues.includes(expName) && !existingValues.includes(exp.code)) {
        const opt = document.createElement('option');
        opt.value = expName;
        opt.textContent = expName;
        select.appendChild(opt);
      }
    });
  } catch (err) {
    console.error('[App] Error in loadExpansions:', err);
  }
}

/**
 * Fetches and renders latest card prices from Supabase API / mock client
 */
async function loadCards() {
  const grid = document.getElementById('cards-grid');
  const countSpan = document.getElementById('results-count');
  const modeBadge = document.getElementById('datasource-badge');

  if (grid) {
    grid.innerHTML = '<div class="no-cards-msg">Loading cards data...</div>';
  }

  // Update Data Source Status Badge
  if (modeBadge) {
    if (window.supabaseTrackerClient && window.supabaseTrackerClient.isOfflineMockMode()) {
      modeBadge.textContent = 'Offline Mock Mode';
      modeBadge.style.backgroundColor = '#2b3147';
    } else {
      modeBadge.textContent = 'Live Supabase DB';
      modeBadge.style.backgroundColor = '#10b981';
      modeBadge.style.color = '#ffffff';
    }
  }

  try {
    allCards = await window.supabaseTrackerClient.fetchLatestCardPrices();
    if (countSpan) {
      countSpan.textContent = `Showing ${allCards.length} cards`;
    }
    filterCards();
  } catch (err) {
    console.error('[App] Error loading cards:', err);
    if (grid) {
      grid.innerHTML = '<div class="no-cards-msg">Failed to load card prices. Please try again.</div>';
    }
  }
}

/**
 * Filters loaded cards by name search input and expansion dropdown filter
 */
function filterCards() {
  const searchInput = document.getElementById('card-search');
  const expansionFilter = document.getElementById('expansion-filter');
  const grid = document.getElementById('cards-grid');
  const countSpan = document.getElementById('results-count');

  if (!grid) return;

  const query = searchInput ? searchInput.value.toLowerCase().trim() : '';
  const selectedExp = expansionFilter ? expansionFilter.value : '';

  const filtered = allCards.filter(card => {
    // Search query match
    const nameMatch = !query || card.card_name.toLowerCase().includes(query) || 
                      (card.card_number && card.card_number.toLowerCase().includes(query));

    // Expansion filter match
    let expMatch = true;
    if (selectedExp && selectedExp !== 'All' && selectedExp !== '') {
      expMatch = (card.expansion_name === selectedExp) || 
                 (card.expansion_code === selectedExp) ||
                 (selectedExp.includes(card.expansion_name) || card.expansion_name.includes(selectedExp));
    }

    return nameMatch && expMatch;
  });

  if (countSpan) {
    countSpan.textContent = `Showing ${filtered.length} of ${allCards.length} cards`;
  }

  renderCards(filtered);
}

/**
 * Renders card items in cards grid container
 */
function renderCards(cardsList) {
  const grid = document.getElementById('cards-grid');
  if (!grid) return;

  if (!cardsList || cardsList.length === 0) {
    grid.innerHTML = '<div class="no-cards-msg">No Pokémon cards found matching selected filters.</div>';
    return;
  }

  const html = cardsList.map(card => {
    const cardId = card.card_id;
    const name = card.card_name || 'Unknown Card';
    const number = card.card_number ? `#${card.card_number}` : '';
    const expCode = card.expansion_code || 'TCG';
    const expName = card.expansion_name || expCode;
    const rarity = card.rarity || 'Standard';
    const imgUrl = card.image_url || 'https://via.placeholder.com/200x280/181c2b/ffcb05?text=Pokemon+Card';
    const priceMinStr = formatCurrency(card.price_min);
    const priceAvgStr = formatCurrency(card.price_avg);
    const dateStr = formatDate(card.price_timestamp);

    return `
      <article class="card-item" data-card-id="${cardId}" onclick="showPriceHistoryModal(${cardId})">
        <div class="card-image-wrapper">
          <span class="expansion-tag">${expCode}</span>
          <img src="${imgUrl}" alt="${name}" loading="lazy" onerror="this.onerror=null; this.src='https://via.placeholder.com/200x280/181c2b/ffcb05?text=No+Image';">
        </div>
        <div class="card-details">
          <div class="card-title-row">
            <h3 class="card-name">${name}</h3>
            <span class="card-number">${number}</span>
          </div>
          <p class="card-rarity">${rarity} • ${expName}</p>
          <div class="card-prices">
            <div class="price-box">
              <span class="price-label">Min Price</span>
              <span class="price-min">${priceMinStr}</span>
            </div>
            <div class="price-box">
              <span class="price-label">Avg Price</span>
              <span class="price-avg">${priceAvgStr}</span>
            </div>
          </div>
          <div class="card-meta-footer">
            <span>Date: ${dateStr}</span>
            <button type="button" class="btn-history" onclick="event.stopPropagation(); showPriceHistoryModal(${cardId})">
              History
            </button>
          </div>
        </div>
      </article>
    `;
  }).join('');

  grid.innerHTML = html;
}

/**
 * Displays price history modal for selected card ID
 */
async function showPriceHistoryModal(cardId) {
  const modal = document.getElementById('price-history-modal');
  const modalTitle = document.getElementById('modal-card-title');
  const modalMeta = document.getElementById('modal-card-meta');
  const tableBody = document.getElementById('history-table-body');

  if (!modal || !tableBody) return;

  // Find card metadata
  const card = allCards.find(c => Number(c.card_id) === Number(cardId)) || {
    card_name: `Card #${cardId}`,
    card_number: '',
    expansion_name: ''
  };

  if (modalTitle) modalTitle.textContent = card.card_name;
  if (modalMeta) modalMeta.textContent = `${card.expansion_name || ''} ${card.card_number ? '#' + card.card_number : ''} (ID: ${cardId})`;

  tableBody.innerHTML = '<tr><td colspan="4" style="text-align: center;">Loading history...</td></tr>';
  modal.classList.remove('hidden');

  try {
    const history = await window.supabaseTrackerClient.fetchCardPriceHistory(cardId);
    if (!history || history.length === 0) {
      tableBody.innerHTML = '<tr><td colspan="4" style="text-align: center;">No price history snapshots found.</td></tr>';
      return;
    }

    tableBody.innerHTML = history.map(snap => `
      <tr>
        <td>${formatDate(snap.timestamp)}</td>
        <td style="color: var(--accent-green); font-weight: 600;">${formatCurrency(snap.price_min)}</td>
        <td style="color: var(--accent-yellow); font-weight: 600;">${formatCurrency(snap.price_avg)}</td>
        <td>${snap.currency || 'BRL'}</td>
      </tr>
    `).join('');
  } catch (err) {
    console.error('[App] Error fetching price history:', err);
    tableBody.innerHTML = '<tr><td colspan="4" style="text-align: center; color: var(--accent-red);">Failed to load price history.</td></tr>';
  }
}

/**
 * Closes price history modal
 */
function closeModal() {
  const modal = document.getElementById('price-history-modal');
  if (modal) {
    modal.classList.add('hidden');
  }
}

// Expose functions globally on window
window.loadExpansions = loadExpansions;
window.loadCards = loadCards;
window.filterCards = filterCards;
window.showPriceHistoryModal = showPriceHistoryModal;
window.closeModal = closeModal;

// Initialize app when DOM content is ready
document.addEventListener('DOMContentLoaded', () => {
  loadExpansions();
  loadCards();

  // Attach search & filter event listeners
  const searchInput = document.getElementById('card-search');
  if (searchInput) {
    searchInput.addEventListener('input', filterCards);
  }

  const expansionFilter = document.getElementById('expansion-filter');
  if (expansionFilter) {
    expansionFilter.addEventListener('change', filterCards);
  }

  // Modal close handlers
  const closeBtn = document.getElementById('close-modal');
  if (closeBtn) {
    closeBtn.addEventListener('click', closeModal);
  }

  const modal = document.getElementById('price-history-modal');
  if (modal) {
    modal.addEventListener('click', (e) => {
      if (e.target === modal) {
        closeModal();
      }
    });
  }

  document.addEventListener('keydown', (e) => {
    if (e.key === 'Escape') {
      closeModal();
    }
  });
});
