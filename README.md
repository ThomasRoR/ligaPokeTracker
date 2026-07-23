# Pokémon Price Tracker 🔴⚪

Bem-vindo ao **Pokémon Price Tracker**, um projeto de rastreamento de preços de cartas de Pokémon TCG (especificamente as expansões da série *Mega Evolução XY* da Copag). O objetivo original deste projeto era atuar como um *Web Scraper* automatizado para extrair preços diários do maior marketplace brasileiro (LigaPokémon) e exibi-los em um painel interativo.

> [!WARNING]
> **Status do Projeto: Missão Parcialmente Abortada (O Triunfo do Cloudflare)** 🛡️
> Este projeto foi um sucesso absoluto em sua arquitetura de software (Front-end, Back-end, Banco de Dados e CI/CD). No entanto, a coleta de dados *ao vivo* foi um "fracasso" técnico e um excelente estudo de caso sobre segurança Web moderna. Leia a seção **"O Desafio Cloudflare"** abaixo para entender o porquê.

---

## 🏗️ Arquitetura do Sistema (O que deu certo)

O projeto foi construído como uma aplicação *Full-Stack* robusta:

- **Web Scraper (Python):** Script construído com `Playwright` e `BeautifulSoup4`, arquitetado para rodar diariamente via *GitHub Actions* (Cron Jobs).
- **Banco de Dados (Supabase/PostgreSQL):** Modelagem relacional (`expansions`, `cards`, `price_history`) acessada via API REST.
- **Front-end:** Interface rica construída com tecnologias Web modernas para consumo da API do Supabase e renderização reativa dos preços e cartas.
- **Tolerância a Falhas (Fallback):** O sistema foi programado para injetar dados *mockados* (fictícios) de alta fidelidade caso o alvo bloqueie a conexão, garantindo que o Front-end nunca fique fora do ar.

---

## 🛡️ O Desafio Cloudflare (Por que "falhou")

A LigaPokémon utiliza uma proteção Web Application Firewall (WAF) de nível *Enterprise* provida pelo **Cloudflare Turnstile**. Durante o desenvolvimento, esbarramos no limite do que é possível fazer com automação gratuita em 2024.

O que tentamos para burlar o firewall:
1. **Requests básico:** Bloqueado instantaneamente na camada TLS/IP.
2. **Cloudscraper:** Falha em resolver o desafio JavaScript moderno.
3. **Playwright Headless + Stealth:** O Cloudflare detectou a ausência de interface gráfica e bloqueou.
4. **Playwright Headful + Stealth:** Mesmo abrindo a interface gráfica na máquina local e aguardando 20 segundos para resolução manual, a assinatura da engine Chromium padrão do Playwright foi pega na malha fina.
5. **Chrome DevTools Protocol (CDP) Hijacking:** Tentamos conectar o script diretamente na instância ativa do navegador Google Chrome do próprio usuário (que já tinha os *cookies* e a confiança do Cloudflare). Imediatamente após anexar o protocolo de depuração, a flag interna `navigator.webdriver=true` foi ativada e o Cloudflare ativou o *loop infinito* de verificação ("Verificando se você é humano...").

### A Lição Aprendida 🎓

Burlar WAFs corporativos como o Cloudflare Turnstile localmente, sem gastar dinheiro, tornou-se praticamente impossível. Em um cenário corporativo real, a solução padrão para esse bloqueio seria a contratação de redes de **Proxies Residenciais Rotativos** e **Scraping APIs** (como BrightData ou ScraperAPI), que custam milhares de dólares por mês. 

Como este é um projeto de portfólio, optamos por **não** prosseguir com custos de infraestrutura e aceitar o bloqueio da LigaPokémon. 

Em vez de uma tela vazia, o sistema agora detecta o erro `HTTP 403 Forbidden` do Cloudflare e popula o banco de dados com nossos preciosos Mocks de *Mega Charizard* e *Mega Mewtwo*, provando que a arquitetura de manipulação e exibição de dados está **100% funcional**.

---

## 🚀 Como Rodar o Projeto Localmente

Mesmo com o bloqueio, você pode rodar o sistema no modo de simulação (Fallback Mode):

1. Configure suas chaves do Supabase no arquivo `.env`.
2. Rode o arquivo `run_scraper.bat`.
3. O script tentará acessar o site ao vivo, tomará um "tapa na cara" elegante do Cloudflare, e então populará o seu banco de dados com sucesso usando os dados embutidos.
4. Acesse seu painel Front-end e veja a mágica (simulada) acontecer!
