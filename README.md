# JOGO DA MEMÓRIA — Parquinho Colorido

Versão infantil do jogo da memória feita com **HTML, CSS e JavaScript puro**. O visual Arcade Neon foi substituído por uma interface clara e divertida, com cenário de parquinho, painéis arredondados e botões coloridos. Acesse pelo link: https://wxsleyb.github.io/jogo-memoria-infantil/

## Abrir o jogo

1. Extraia o ZIP inteiro.
2. Mantenha `index.html`, `styles.css`, `scripts.js`, `biblioteca-local.js`, `biblioteca-pixabay.js` e a pasta `img/` juntos.
3. Abra `index.html` em um navegador moderno.

O jogo funciona sem internet usando as **96 ilustrações locais de demonstração**: 32 bichinhos, 32 frutinhas e 32 veículos. As fontes do Google são opcionais; se estiver offline, fontes alternativas locais serão usadas.

## Verso escolhido

- **Opção 2: Ponto de interrogação divertido** — um ponto de interrogação amarelo e sorridente sobre fundo colorido com estrelinhas e confetes.
- Novo arquivo: `img/card-back.png`, usado tanto nas cartas fechadas quanto na prévia do tabuleiro.
- Original preservado para comparação em `img/card-back-original.png`.

A nova imagem de verso foi extraída da arte gerada durante a escolha das propostas visuais. A interface foi implementada em CSS e HTML, não é apenas uma imagem estática.

## Recursos preservados

- **Temas:** Bichinhos, Frutinhas, Veículos e Todos.
- **Dificuldades:** Casual (6 pares), Intermediário (12 pares), Insano (16 pares) e Personalizado (2–32 pares).
- Formação e embaralhamento de pares, tentativas, cronômetro, progresso, zoom, pausa, efeitos sonoros opcionais, reinício, vitória e recordes locais por tema/dificuldade.
- Layout adaptado ao computador e ao celular e suporte a teclado.
- Não faz pesquisas abertas durante a partida. Não inclui anúncios nem ferramentas de acompanhamento.

## Imagens Pixabay (opcional)

**Importante:** as 96 ilustrações que já vêm no ZIP são desenhos locais originais de demonstração, **não são da Pixabay**. O catálogo `biblioteca-pixabay.js` começa vazio. Para incorporar ilustrações Pixabay aprovadas manualmente, a ferramenta de curadoria foi mantida.

1. Obtenha uma chave na [documentação da Pixabay API](https://pixabay.com/api/docs/).
2. Instale a dependência: `python -m pip install Pillow`.
3. Informe a chave por variável de ambiente (`PIXABAY_API_KEY`). **Não coloque a chave no JavaScript.**
4. Na pasta do projeto, busque candidatos:

```bash
python tools/importar_pixabay.py buscar --tema animais --consulta "cute cartoon animal isolated" --limite 40
python tools/importar_pixabay.py buscar --tema frutas --consulta "cute cartoon fruit isolated" --limite 40
python tools/importar_pixabay.py buscar --tema transportes --consulta "cute cartoon vehicle isolated" --limite 40
```

5. Revise os resultados e preencha `curadoria/selecionadas.json` com IDs e nomes aprovados.
6. Importe: `python tools/importar_pixabay.py importar`.

A ferramenta baixa arquivos selecionados para o projeto e atualiza `biblioteca-pixabay.js`; imagens de demonstração completam automaticamente o conjunto quando necessário. A chave é usada só na etapa de curadoria, nunca durante o jogo. Verifique as condições de licenciamento e os direitos sobre os materiais antes de distribuir.

## Arquivos principais

| Arquivo | Finalidade |
|---|---|
| `index.html` | Interface Parquinho Colorido |
| `styles.css` | Cores, cenário, cartões e responsividade |
| `scripts.js` | Lógica do jogo e recursos interativos |
| `biblioteca-local.js` | Catálogo de 96 ilustrações locais |
| `biblioteca-pixabay.js` | Catálogo opcional de imagens importadas e aprovadas |
| `img/card-back.png` | Novo verso das cartas: opção 2 |
| `img/card-back-original.png` | Verso antigo preservado |
| `img/ilustracoes/` | Imagens infantis locais |
| `tools/importar_pixabay.py` | Busca e importação de candidatos Pixabay |

## Configuração padrão ao abrir

O site inicia com o tema **Bichinhos** (`animais`) e a dificuldade **Casual** (**6 pares / 12 cartas**) selecionados. O jogador pode trocar tema e dificuldade antes de começar uma partida.


## Revisão das imagens de transportes (novembro de 2026)

**Alterações limitadas à categoria Veículos.** Os SVGs das categorias Bichinhos e Frutinhas foram preservados sem nenhuma alteração.

- **7 transportes redesenhados** com silhuetas reconhecíveis: helicóptero (`09-helicopter.svg`), avião (`08-plane.svg`), moto (`05-moto.svg`), trator (`11-tractor.svg`), caminhão de bombeiros (`13-firetruck.svg`), van (`23-van.svg`) e jipe (`27-jeep.svg`).
- **Legendas recuperadas** nos seis SVGs substituídos na revisão anterior: `06-train.svg`, `22-icecreamtruck.svg`, `28-racecar.svg`, `29-bullettrain.svg`, `30-dumptruck.svg` e `31-pickup.svg`.
- **Legenda padronizada:** fundo branco arredondado na parte inferior de cada ilustração (como na coleção original), com o nome do transporte.
- O catálogo passa a identificar `13-firetruck.svg` como **Caminhão de bombeiros** em vez de apenas **Bombeiros**. As renomeações anteriores de carro de sorvete, carro de corrida e caminhão basculante foram mantidas.
- Quantidades inalteradas: **32 transportes, 32 animais, 32 frutas**. Assim, qualquer tema continua permitindo até 32 pares no modo Personalizado.
- Configuração inicial preservada: **Casual (6 pares) e Bichinhos**.

Prévia dos 13 SVGs revistos: `preview-transportes.png`. Todos os desenhos continuam em **SVG vetorial**, na mesma proporção e estrutura de arquivos que o jogo já utiliza.
