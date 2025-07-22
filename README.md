## 🔸 Tabela: `games`

Representa os jogos eletrônicos disponíveis na plataforma RAWG.

**Atributos:**

- `name`: Nome do jogo  
- `released`: Data de lançamento  
- `rating`: Nota média dos usuários  
- `ratings_count`: Quantidade de avaliações recebidas  
- `image_background`: URL da imagem de fundo do jogo  
- `platforms`: Plataformas em que o jogo está disponível (ex: PC, PS5)  
- `genres`: Lista de gêneros do jogo (ex: Action, RPG)  
- `tags`: Lista de tags associadas (ex: Multiplayer, Indie)

---

## 🔸 Tabela: `creators`

Representa criadores envolvidos na produção de jogos (desenvolvedores, diretores, artistas, etc).

**Atributos:**

- `name`: Nome do criador  
- `slug`: Nome formatado para URL  
- `image`: URL da foto do criador (se disponível)  
- `games_count`: Número de jogos relacionados ao criador  
- `rating`: Avaliação média do criador com base na opinião dos usuários da plataforma
- `positions`: Lista de funções exercidas (ex: Designer, Developer)  
- `description`: Biografia ou descrição do criador  
- `games`: Lista de jogos mais populares feitos por ele

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
- `description`: Descrição da plataforma  
- `games`: Lista de jogos mais populares da plataforma

---

## 🔸 Tabela: `stores`

Representa as lojas digitais onde os jogos podem ser comprados.

**Atributos:**

- `name`: Nome da loja  
- `domain`: Domínio da loja (ex: store.steampowered.com)  
- `games_count`: Quantidade de jogos disponíveis na loja  
- `image_background`: Imagem de fundo da loja  
- `foundation_data`: Data de fundação da loja
- `location`: País em que a loja foi fundada
- `latitude`: latitude da sede da loja
- `longitude`: longitude da sede da loja
---

## 🔸 Tabela: `developers`

Representa as desenvolvedoras de jogos eletrônicos presentes na plataforma RAWG.

**Atributos:**

- `name`: Nome da desenvolvedora  
- `slug`: Nome formatado para URL  
- `games_count`: Quantidade de jogos desenvolvidos  
- `image_background`: Imagem de fundo associada  
- `description`: Descrição detalhada da desenvolvedora (via detalhes da API)  
- `website`: Site oficial da desenvolvedora  
- `country`: País de origem da desenvolvedora  
- `foundation_date`: Data de fundação da desenvolvedora