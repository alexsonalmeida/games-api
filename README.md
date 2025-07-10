## 🔸 Tabela: `games`

Representa os jogos eletrônicos disponíveis na plataforma RAWG.

**Atributos:**

- `name`: Nome do jogo  
- `released`: Data de lançamento  
- `rating`: Nota média dos usuários  
- `ratings_count`: Quantidade de avaliações recebidas  
- `background_image`: URL da imagem de fundo do jogo  
- `platforms`: Plataformas em que o jogo está disponível (ex: PC, PS5)  
- `genres`: Lista de gêneros do jogo (ex: Action, RPG)  
- `tags`: Lista de tags associadas (ex: Multiplayer, Indie)

---

## 🔸 Tabela: `genres`

Representa os gêneros dos jogos eletrônicos.

**Atributos:**

- `name`: Nome do gênero  
- `slug`: Nome formatado para URL  
- `games_count`: Número de jogos associados ao gênero  
- `image_background`: Imagem ilustrativa  
- `description`: Descrição do gênero (obtida por chamada detalhada)  
- `language`: Idioma padrão do gênero  
- `games`: Lista de jogos populares desse gênero  
- `updated`: Data da última atualização do gênero

---

## 🔸 Tabela: `platforms`

Representa as plataformas (consoles, PCs, etc) onde os jogos são lançados.

**Atributos:**

- `name`: Nome da plataforma  
- `slug`: Nome formatado para URL  
- `games_count`: Quantidade de jogos disponíveis para a plataforma  
- `image_background`: Imagem de fundo ilustrativa  
- `year_start`: Ano de início da plataforma  
- `year_end`: Ano de término (se aplicável)  
- `platform_type`: Tipo de plataforma (ex: console, PC, mobile)  
- `games`: Lista de jogos mais populares da plataforma

---

## 🔸 Tabela: `stores`

Representa as lojas digitais onde os jogos podem ser comprados.

**Atributos:**

- `name`: Nome da loja  
- `slug`: Nome formatado para URL  
- `domain`: Domínio da loja (ex: store.steampowered.com)  
- `games_count`: Quantidade de jogos disponíveis na loja  
- `image_background`: Imagem de fundo da loja  
- `description`: Breve descrição da loja (via detalhes)  
- `games`: Lista de jogos populares na loja  
- `updated`: Data da última atualização da loja

---

## 🔸 Tabela: `tags`

Representa as tags associadas aos jogos (ex: "multiplayer", "horror").

**Atributos:**

- `name`: Nome da tag  
- `slug`: Nome formatado para URL  
- `language`: Idioma padrão da tag  
- `games_count`: Quantidade de jogos com essa tag  
- `image_background`: Imagem associada à tag  
- `description`: Descrição detalhada da tag  
- `games`: Lista de jogos com essa tag  
- `updated`: Data da última atualização da tag