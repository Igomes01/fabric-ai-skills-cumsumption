# 🧮 Calculadora Online

Uma calculadora web simples e elegante que funciona diretamente no seu navegador!

---

## 📝 Contador de Palavras & Tokens

Além da calculadora, este repositório agora inclui uma ferramenta estática (100% client-side) para analisar **lista de frases** e obter:

- Contagem de palavras
- Estimativa de tokens (heurística chars/4)
- Cálculo real de tokens se o script `tiktoken` JS carregar
- Médias por frase
- Download CSV e copiar tabela para clipboard

### Como usar (GitHub Pages)

1. Publique o repositório com GitHub Pages (ver instruções abaixo)
2. Acesse a URL do seu Pages (`https://SEU_USUARIO.github.io/NOME_DO_REPOSITORIO`)
3. A página `index.html` já abre a ferramenta
4. Cole suas frases (uma por linha ou separadas por `;` ou `|`)
5. Ajuste opções (remover vazias, minúsculas, separador, modo de tokens, encoding)
6. Clique em **Calcular métricas**
7. Baixe o CSV ou copie a tabela

### Técnicas usadas

- **HTML + CSS puro** com design responsivo
- **JavaScript vanilla** (nenhuma dependência obrigatória)
- **Progressive enhancement**: tenta carregar `js-tiktoken` via CDN; se falhar usa heurística
- **Segurança / Privacidade**: nenhum dado sai do navegador

### Estrutura visual

| Elemento | Função |
|----------|--------|
| Textarea | Inserção de frases |
| Configurações | Ajuste de separador e normalização |
| KPIs | Totais e médias |
| Tabela | Métricas linha a linha |
| Chips | Resumo do processamento |

---

## 🌐 [**ACESSE A CALCULADORA AQUI**](https://SEU_USUARIO.github.io/calculadora-online)

## ✨ Funcionalidades

- ✅ **Interface moderna e responsiva**
- ✅ **Soma instantânea** de dois números
- ✅ **Suporte a decimais** (ex: 10.5 + 7.3)
- ✅ **Números negativos** (ex: -5 + 10)
- ✅ **Histórico de cálculos** (salvo localmente)
- ✅ **Atalhos de teclado** (Enter para navegar/calcular)
- ✅ **Animações suaves** e feedback visual
- ✅ **Responsivo** - funciona em celular e desktop
- ✅ **Easter egg** 🎮 (tente o Konami Code!)

## 🎯 Como usar

1. **Acesse a calculadora** no link acima
2. **Digite o primeiro número** no campo superior
3. **Digite o segundo número** no campo inferior  
4. **Clique em "Calcular Soma"** ou pressione Enter
5. **Veja o resultado** instantaneamente!

## 🚀 Hospedagem no GitHub Pages

### Configuração automática:

1. **Faça push do código para o GitHub**
2. **Vá nas Configurações do repositório**
3. **Role até "Pages" na barra lateral**
4. **Selecione "Deploy from a branch"**
5. **Escolha "main" como branch**
6. **Clique em "Save"**

### Sua calculadora estará disponível em:
```
https://SEU_USUARIO.github.io/NOME_DO_REPOSITORIO
```

## 📁 Estrutura do projeto

```
├── index.html          # Interface web (calculadora + contador de tokens)
├── calculadora.py      # Versão Python da calculadora simples
├── README.md           # Esta documentação
└── .gitignore          # Arquivos ignorados pelo Git
```

## 🎨 Características do design

- **Gradiente moderno** azul/roxo
- **Cards com sombra** para profundidade
- **Animações suaves** nos botões e resultados
- **Feedback visual** para sucesso/erro
- **Tipografia limpa** com ícones emoji
- **Layout responsivo** para todos os dispositivos

## ⌨️ Atalhos de teclado

- **Tab** - Navegar entre campos
- **Enter** - Ir para próximo campo ou calcular
- **↑↑↓↓←→←→BA** - Easter egg especial! 🎮

## 💾 Persistência de dados

- **Histórico salvo** no navegador (LocalStorage)
- **Até 10 cálculos** mantidos automaticamente
- **Botão de limpar** histórico disponível
- **Dados persistem** entre sessões

## �️ Tecnologias

- **HTML5** - Estrutura semântica
- **CSS3** - Design moderno com gradientes e animações
- **JavaScript** - Lógica da calculadora e persistência
- **LocalStorage** - Salvamento do histórico
- **GitHub Pages** - Hospedagem gratuita

## 🧪 Testando localmente

Você também pode testar a versão Python:

```bash
# Teste direto com números
python calculadora.py 10 5

# Teste com texto (simulando issue)
python calculadora.py "Número 1: 10.5\nNúmero 2: 5.2"
```

## � Próximas melhorias

- [ ] Mais operações (-, *, /)
- [ ] Modo escuro/claro
- [ ] Calculadora científica
- [ ] Compartilhamento de resultados
- [ ] Temas personalizáveis
- [ ] PWA (Progressive Web App)

## 🤝 Contribuindo

1. Fork este repositório
2. Crie uma branch: `git checkout -b feature/nova-funcao`
3. Commit suas mudanças: `git commit -m 'Adiciona nova funcionalidade'`
4. Push para a branch: `git push origin feature/nova-funcao`
5. Abra um Pull Request

## 📄 Licença

Este projeto está sob a licença MIT. Veja o arquivo LICENSE para mais detalhes.

## 🌟 Mostre seu apoio

Se este projeto te ajudou, dê uma ⭐ no repositório!

---

**Feito com ❤️ e muito ☕** | [Ver no GitHub](https://github.com/SEU_USUARIO/calculadora-online)