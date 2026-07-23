/**
 * Supabase Client & Offline Mock Data Store
 * Pokémon Price Tracker - Mega Evolution Block
 */

// Supabase configuration parameters (env or public fallback config)
window.SUPABASE_URL = window.SUPABASE_URL || 'https://omheivhvuhpmgvttcmtb.supabase.co';
window.SUPABASE_KEY = window.SUPABASE_KEY || 'sb_publishable_uLbWQZSNPiGzZcTr_KwNGQ_af9BedT0';

/**
 * 8 Target Mega Evolution Block Expansions Metadata
 */
const MOCK_EXPANSIONS = [
  { id: 1, code: 'PBL', name: 'Coleção Poderes de Batalha', release_date: '2016-01-01' },
  { id: 2, code: 'ASC', name: 'Coleção Ascensão', release_date: '2016-01-01' },
  { id: 3, code: 'POR', name: 'Coleção Portais', release_date: '2016-01-01' },
  { id: 4, code: 'CRI', name: 'Coleção Criadores', release_date: '2016-01-01' },
  { id: 5, code: 'MEG', name: 'Coleção Mega Evolução', release_date: '2016-01-01' },
  { id: 6, code: 'MEP', name: 'Coleção Mega Poderes', release_date: '2016-01-01' },
  { id: 7, code: 'PFL', name: 'Coleção Poderes de Fogo e Luz', release_date: '2016-01-01' }
];

/**
 * Mock Catalog Cards across all 8 Mega Evolution block sets
 */
const MOCK_CARDS = [
  {
    price_id: 101,
    card_id: 1,
    card_name: 'Primal Kyogre-EX',
    card_number: '55/160',
    rarity: 'Ultra Rare',
    image_url: 'https://repositorio.ligapokemon.com.br/images/cartas/PRC/55.jpg',
    expansion_id: 1,
    expansion_name: 'XY - Primal Clash',
    expansion_code: 'PRC',
    price_min: 85.00,
    price_avg: 120.50,
    currency: 'BRL',
    price_timestamp: '2026-07-22T18:00:00Z'
  },
  {
    price_id: 102,
    card_id: 2,
    card_name: 'Primal Groudon-EX',
    card_number: '86/160',
    rarity: 'Ultra Rare',
    image_url: 'https://repositorio.ligapokemon.com.br/images/cartas/PRC/86.jpg',
    expansion_id: 1,
    expansion_name: 'XY - Primal Clash',
    expansion_code: 'PRC',
    price_min: 90.00,
    price_avg: 135.00,
    currency: 'BRL',
    price_timestamp: '2026-07-22T18:00:00Z'
  },
  {
    price_id: 103,
    card_id: 3,
    card_name: 'M Rayquaza-EX',
    card_number: '61/108',
    rarity: 'Ultra Rare',
    image_url: 'https://repositorio.ligapokemon.com.br/images/cartas/ROS/61.jpg',
    expansion_id: 2,
    expansion_name: 'XY - Roaring Skies',
    expansion_code: 'ROS',
    price_min: 145.00,
    price_avg: 195.00,
    currency: 'BRL',
    price_timestamp: '2026-07-22T18:30:00Z'
  },
  {
    price_id: 104,
    card_id: 4,
    card_name: 'Shaymin-EX',
    card_number: '77/108',
    rarity: 'Ultra Rare',
    image_url: 'https://repositorio.ligapokemon.com.br/images/cartas/ROS/77.jpg',
    expansion_id: 2,
    expansion_name: 'XY - Roaring Skies',
    expansion_code: 'ROS',
    price_min: 75.00,
    price_avg: 110.00,
    currency: 'BRL',
    price_timestamp: '2026-07-22T18:30:00Z'
  },
  {
    price_id: 105,
    card_id: 5,
    card_name: 'M Tyranitar-EX',
    card_number: '43/98',
    rarity: 'Ultra Rare',
    image_url: 'https://repositorio.ligapokemon.com.br/images/cartas/AOR/43.jpg',
    expansion_id: 3,
    expansion_name: 'XY - Ancient Origins',
    expansion_code: 'AOR',
    price_min: 68.50,
    price_avg: 92.00,
    currency: 'BRL',
    price_timestamp: '2026-07-22T19:00:00Z'
  },
  {
    price_id: 106,
    card_id: 6,
    card_name: 'M Ampharos-EX',
    card_number: '28/98',
    rarity: 'Ultra Rare',
    image_url: 'https://repositorio.ligapokemon.com.br/images/cartas/AOR/28.jpg',
    expansion_id: 3,
    expansion_name: 'XY - Ancient Origins',
    expansion_code: 'AOR',
    price_min: 52.00,
    price_avg: 74.00,
    currency: 'BRL',
    price_timestamp: '2026-07-22T19:00:00Z'
  },
  {
    price_id: 107,
    card_id: 7,
    card_name: 'M Mewtwo-EX',
    card_number: '64/162',
    rarity: 'Ultra Rare',
    image_url: 'https://repositorio.ligapokemon.com.br/images/cartas/BKT/64.jpg',
    expansion_id: 4,
    expansion_name: 'XY - BREAKthrough',
    expansion_code: 'BKT',
    price_min: 110.00,
    price_avg: 155.00,
    currency: 'BRL',
    price_timestamp: '2026-07-22T19:15:00Z'
  },
  {
    price_id: 108,
    card_id: 8,
    card_name: 'Zoroark BREAK',
    card_number: '92/162',
    rarity: 'Rare BREAK',
    image_url: 'https://repositorio.ligapokemon.com.br/images/cartas/BKT/92.jpg',
    expansion_id: 4,
    expansion_name: 'XY - BREAKthrough',
    expansion_code: 'BKT',
    price_min: 35.00,
    price_avg: 48.00,
    currency: 'BRL',
    price_timestamp: '2026-07-22T19:15:00Z'
  },
  {
    price_id: 109,
    card_id: 9,
    card_name: 'M Gyarados-EX',
    card_number: '27/122',
    rarity: 'Ultra Rare',
    image_url: 'https://repositorio.ligapokemon.com.br/images/cartas/BKP/27.jpg',
    expansion_id: 5,
    expansion_name: 'XY - BREAKpoint',
    expansion_code: 'BKP',
    price_min: 95.00,
    price_avg: 130.00,
    currency: 'BRL',
    price_timestamp: '2026-07-22T19:30:00Z'
  },
  {
    price_id: 110,
    card_id: 10,
    card_name: 'Greninja',
    card_number: '40/122',
    rarity: 'Rare Holo',
    image_url: 'https://repositorio.ligapokemon.com.br/images/cartas/BKP/40.jpg',
    expansion_id: 5,
    expansion_name: 'XY - BREAKpoint',
    expansion_code: 'BKP',
    price_min: 40.00,
    price_avg: 58.00,
    currency: 'BRL',
    price_timestamp: '2026-07-22T19:30:00Z'
  },
  {
    price_id: 111,
    card_id: 11,
    card_name: 'M Alakazam-EX',
    card_number: '26/124',
    rarity: 'Ultra Rare',
    image_url: 'https://repositorio.ligapokemon.com.br/images/cartas/FCO/26.jpg',
    expansion_id: 6,
    expansion_name: 'XY - Fates Collide',
    expansion_code: 'FCO',
    price_min: 88.00,
    price_avg: 118.00,
    currency: 'BRL',
    price_timestamp: '2026-07-22T19:45:00Z'
  },
  {
    price_id: 112,
    card_id: 12,
    card_name: 'Lugia BREAK',
    card_number: '79/124',
    rarity: 'Rare BREAK',
    image_url: 'https://repositorio.ligapokemon.com.br/images/cartas/FCO/79.jpg',
    expansion_id: 6,
    expansion_name: 'XY - Fates Collide',
    expansion_code: 'FCO',
    price_min: 45.00,
    price_avg: 62.00,
    currency: 'BRL',
    price_timestamp: '2026-07-22T19:45:00Z'
  },
  {
    price_id: 113,
    card_id: 13,
    card_name: 'M Gardevoir-EX',
    card_number: '79/114',
    rarity: 'Ultra Rare',
    image_url: 'https://repositorio.ligapokemon.com.br/images/cartas/STS/79.jpg',
    expansion_id: 7,
    expansion_name: 'XY - Steam Siege',
    expansion_code: 'STS',
    price_min: 78.00,
    price_avg: 105.00,
    currency: 'BRL',
    price_timestamp: '2026-07-22T20:00:00Z'
  },
  {
    price_id: 114,
    card_id: 14,
    card_name: 'Volcanion-EX',
    card_number: '26/114',
    rarity: 'Ultra Rare',
    image_url: 'https://repositorio.ligapokemon.com.br/images/cartas/STS/26.jpg',
    expansion_id: 7,
    expansion_name: 'XY - Steam Siege',
    expansion_code: 'STS',
    price_min: 32.00,
    price_avg: 45.00,
    currency: 'BRL',
    price_timestamp: '2026-07-22T20:00:00Z'
  },
  {
    price_id: 115,
    card_id: 15,
    card_name: 'M Charizard-EX',
    card_number: '13/108',
    rarity: 'Ultra Rare',
    image_url: 'https://repositorio.ligapokemon.com.br/images/cartas/EVO/13.jpg',
    expansion_id: 8,
    expansion_name: 'XY - Evolutions',
    expansion_code: 'EVO',
    price_min: 180.00,
    price_avg: 240.00,
    currency: 'BRL',
    price_timestamp: '2026-07-22T20:15:00Z'
  },
  {
    price_id: 116,
    card_id: 16,
    card_name: 'Charizard',
    card_number: '11/108',
    rarity: 'Rare Holo',
    image_url: 'https://repositorio.ligapokemon.com.br/images/cartas/EVO/11.jpg',
    expansion_id: 8,
    expansion_name: 'XY - Evolutions',
    expansion_code: 'EVO',
    price_min: 210.00,
    price_avg: 290.00,
    currency: 'BRL',
    price_timestamp: '2026-07-22T20:15:00Z'
  }
];

/**
 * Historical time-series price snapshots for mock cards
 */
const MOCK_PRICE_HISTORY = {
  1: [
    { id: 501, card_id: 1, price_min: 85.00, price_avg: 120.50, currency: 'BRL', timestamp: '2026-07-22T18:00:00Z' },
    { id: 401, card_id: 1, price_min: 82.00, price_avg: 118.00, currency: 'BRL', timestamp: '2026-07-21T18:00:00Z' },
    { id: 301, card_id: 1, price_min: 80.00, price_avg: 115.00, currency: 'BRL', timestamp: '2026-07-20T18:00:00Z' }
  ],
  2: [
    { id: 502, card_id: 2, price_min: 90.00, price_avg: 135.00, currency: 'BRL', timestamp: '2026-07-22T18:00:00Z' },
    { id: 402, card_id: 2, price_min: 88.00, price_avg: 130.00, currency: 'BRL', timestamp: '2026-07-21T18:00:00Z' },
    { id: 302, card_id: 2, price_min: 85.00, price_avg: 128.00, currency: 'BRL', timestamp: '2026-07-20T18:00:00Z' }
  ],
  3: [
    { id: 503, card_id: 3, price_min: 145.00, price_avg: 195.00, currency: 'BRL', timestamp: '2026-07-22T18:30:00Z' },
    { id: 403, card_id: 3, price_min: 140.00, price_avg: 190.00, currency: 'BRL', timestamp: '2026-07-21T18:30:00Z' },
    { id: 303, card_id: 3, price_min: 138.00, price_avg: 185.00, currency: 'BRL', timestamp: '2026-07-20T18:30:00Z' }
  ],
  4: [
    { id: 504, card_id: 4, price_min: 75.00, price_avg: 110.00, currency: 'BRL', timestamp: '2026-07-22T18:30:00Z' },
    { id: 404, card_id: 4, price_min: 72.00, price_avg: 108.00, currency: 'BRL', timestamp: '2026-07-21T18:30:00Z' }
  ],
  5: [
    { id: 505, card_id: 5, price_min: 68.50, price_avg: 92.00, currency: 'BRL', timestamp: '2026-07-22T19:00:00Z' },
    { id: 405, card_id: 5, price_min: 65.00, price_avg: 90.00, currency: 'BRL', timestamp: '2026-07-21T19:00:00Z' }
  ],
  6: [
    { id: 506, card_id: 6, price_min: 52.00, price_avg: 74.00, currency: 'BRL', timestamp: '2026-07-22T19:00:00Z' }
  ],
  7: [
    { id: 507, card_id: 7, price_min: 110.00, price_avg: 155.00, currency: 'BRL', timestamp: '2026-07-22T19:15:00Z' },
    { id: 407, card_id: 7, price_min: 105.00, price_avg: 150.00, currency: 'BRL', timestamp: '2026-07-21T19:15:00Z' }
  ],
  8: [
    { id: 508, card_id: 8, price_min: 35.00, price_avg: 48.00, currency: 'BRL', timestamp: '2026-07-22T19:15:00Z' }
  ],
  9: [
    { id: 509, card_id: 9, price_min: 95.00, price_avg: 130.00, currency: 'BRL', timestamp: '2026-07-22T19:30:00Z' }
  ],
  10: [
    { id: 510, card_id: 10, price_min: 40.00, price_avg: 58.00, currency: 'BRL', timestamp: '2026-07-22T19:30:00Z' }
  ],
  11: [
    { id: 511, card_id: 11, price_min: 88.00, price_avg: 118.00, currency: 'BRL', timestamp: '2026-07-22T19:45:00Z' }
  ],
  12: [
    { id: 512, card_id: 12, price_min: 45.00, price_avg: 62.00, currency: 'BRL', timestamp: '2026-07-22T19:45:00Z' }
  ],
  13: [
    { id: 513, card_id: 13, price_min: 78.00, price_avg: 105.00, currency: 'BRL', timestamp: '2026-07-22T20:00:00Z' }
  ],
  14: [
    { id: 514, card_id: 14, price_min: 32.00, price_avg: 45.00, currency: 'BRL', timestamp: '2026-07-22T20:00:00Z' }
  ],
  15: [
    { id: 515, card_id: 15, price_min: 180.00, price_avg: 240.00, currency: 'BRL', timestamp: '2026-07-22T20:15:00Z' },
    { id: 415, card_id: 15, price_min: 175.00, price_avg: 235.00, currency: 'BRL', timestamp: '2026-07-21T20:15:00Z' }
  ],
  16: [
    { id: 516, card_id: 16, price_min: 210.00, price_avg: 290.00, currency: 'BRL', timestamp: '2026-07-22T20:15:00Z' },
    { id: 416, card_id: 16, price_min: 205.00, price_avg: 280.00, currency: 'BRL', timestamp: '2026-07-21T20:15:00Z' }
  ]
};

/**
 * Supabase Tracker Client Manager
 */
class SupabaseTrackerClient {
  constructor() {
    this.client = null;
    this.initClient();
  }

  /**
   * Initializes live Supabase JS SDK client if available and configured
   */
  initClient() {
    const url = window.SUPABASE_URL;
    const key = window.SUPABASE_KEY;

    if (window.supabase && typeof window.supabase.createClient === 'function' && url && key && !url.includes('example.com')) {
      try {
        this.client = window.supabase.createClient(url, key);
        console.log('[SupabaseClient] Initialized live Supabase client.');
      } catch (err) {
        console.warn('[SupabaseClient] Failed to initialize live client, using mock mode:', err);
        this.client = null;
      }
    } else {
      console.log('[SupabaseClient] Operating in Offline Mock Mode.');
    }
  }

  /**
   * Check if client is operating in fallback offline mock mode
   */
  isOfflineMockMode() {
    return !this.client;
  }

  /**
   * Fetches target expansions list from `expansions` table or mock data
   */
  async fetchExpansions() {
    if (this.client) {
      try {
        const { data, error } = await this.client
          .from('expansions')
          .select('*')
          .order('id', { ascending: true });
        if (!error && data && data.length > 0) {
          return data;
        }
      } catch (err) {
        console.warn('[SupabaseClient] Error fetching expansions from Supabase, falling back to mock:', err);
      }
    }
    return MOCK_EXPANSIONS;
  }

  /**
   * Fetches latest card prices from `latest_card_prices` view or fallback mock dataset
   * Can query `cards` and `price_history` if needed.
   */
  async fetchLatestCardPrices(expansionCode = '') {
    if (this.client) {
      try {
        let query = this.client.from('latest_card_prices').select('*');
        if (expansionCode) {
          query = query.eq('expansion_code', expansionCode.toUpperCase());
        }
        const { data, error } = await query;
        if (!error && data && data.length > 0) {
          return data;
        }
      } catch (err) {
        console.warn('[SupabaseClient] Error querying latest_card_prices view, falling back to mock:', err);
      }
    }

    // Mock Data Fallback
    if (expansionCode && expansionCode !== 'ALL') {
      const codeUpper = expansionCode.toUpperCase();
      return MOCK_CARDS.filter(c => 
        c.expansion_code.toUpperCase() === codeUpper ||
        c.expansion_name.toLowerCase().includes(expansionCode.toLowerCase())
      );
    }
    return MOCK_CARDS;
  }

  /**
   * Fetches time-series price history for a given card from `price_history` table or fallback mock dataset
   */
  async fetchCardPriceHistory(cardId) {
    const parsedId = Number(cardId);

    if (this.client) {
      try {
        const { data, error } = await this.client
          .from('price_history')
          .select('*')
          .eq('card_id', parsedId)
          .order('timestamp', { ascending: false });
        if (!error && data && data.length > 0) {
          return data;
        }
      } catch (err) {
        console.warn('[SupabaseClient] Error querying price_history table, falling back to mock:', err);
      }
    }

    // Return mock price history or default snapshot
    if (MOCK_PRICE_HISTORY[parsedId]) {
      return MOCK_PRICE_HISTORY[parsedId];
    }
    
    // Fallback if cardId not in mock map: find card and return single history record
    const card = MOCK_CARDS.find(c => c.card_id === parsedId);
    if (card) {
      return [{
        id: 999,
        card_id: card.card_id,
        price_min: card.price_min,
        price_avg: card.price_avg,
        currency: card.currency || 'BRL',
        timestamp: card.price_timestamp || new Date().toISOString()
      }];
    }

    return [];
  }
}

// Global instance export
window.supabaseTrackerClient = new SupabaseTrackerClient();
