# Original User Request

## Initial Request — 2026-07-22T21:05:34-03:00

# Teamwork Project Prompt — Draft

> Status: Launched
> Goal: Craft prompt → get user approval → delegate to teamwork_preview

Um sistema automatizado que realiza web scraping de preços de cartas Pokémon do bloco de mega evolução (últimas 8 coleções) no site ligapokemon.com.br, armazenando o histórico no Supabase e exibindo-os em um front-end no GitHub Pages.

Working directory: C:\Users\rault\.gemini\antigravity\scratch\teamwork_projects\pokemon_price_tracker
Integrity mode: development

## Requirements

### R1. Coleta de Preços (Scraping)
O sistema deve extrair preços das cartas do bloco alvo (mega evolução) do site ligapokemon.com.br. A implementação deve lidar adequadamente com a estrutura da página do site para extrair os valores corretos.

### R2. Armazenamento e Automação
O scraper deve armazenar o histórico de preços em um banco de dados no Supabase. O projeto deve incluir a configuração necessária de CI/CD (GitHub Actions) para executar o scraper automaticamente a cada 6 horas.

### R3. Visualização (Front-end)
Deve ser desenvolvida uma interface web construída apenas com tecnologias compatíveis com hospedagem estática (para posterior deploy no GitHub Pages). O front-end deve consumir os dados do Supabase e exibir o histórico de preços.

## Acceptance Criteria

### Extração de Dados
- [ ] Um teste rodado localmente deve provar que o script de scraping acessa ligapokemon.com.br, extrai com sucesso o nome e preço de pelo menos uma carta do bloco de mega evolução e exibe os resultados.

### Conectividade e Automação
- [ ] O script deve conseguir inserir um preço mock/fictício com sucesso no Supabase e realizar a leitura para comprovar a conectividade.
- [ ] O projeto deve conter um workflow válido (`.github/workflows/`) configurado com um gatilho de agendamento (cron) para rodar a cada 6 horas.

### Front-end
- [ ] A aplicação web, ao ser servida localmente, deve buscar os dados no Supabase e renderizar corretamente na tela, sem usar servidores de back-end dedicados além do próprio banco.
