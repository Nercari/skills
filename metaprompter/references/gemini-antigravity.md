# Adaptador Gemini e Google Antigravity

Pesquisa verificada em **2026-07-30**.

Rótulos:

- **Documentado:** consta em fonte oficial do Google.
- **Observado:** identificado no ambiente ou artefato em análise.
- **Inferência:** conclusão provável, não garantia.
- **Recomendação:** escolha de projeto da Metaprompter.

## Sumário

1. Roteamento de superfície
2. Gemini em chat e Gems
3. Gemini API
4. Antigravity IDE e CLI
5. Ferramentas, permissões e subagentes
6. Handoff e validação
7. Fontes oficiais

## 1. Roteamento de superfície

Separar:

| Superfície | Artefato adequado |
|---|---|
| Gemini Apps/chat | prompt conversacional |
| Gem | instruções reutilizáveis salvas na interface do Gem |
| Gemini API | `system_instruction`, entrada e configuração no SDK/API |
| Antigravity IDE | tarefa + Rules, Workflows ou skills quando persistentes |
| Antigravity CLI | tarefa + `GEMINI.md`/`AGENTS.md`, skill ou configuração confirmada |

Não tratar Gem como chamada de API. Não tratar Antigravity como simples janela do Gemini.

## 2. Gemini em chat e Gems

**Documentado:** Gems são versões personalizadas do Gemini para tarefas repetidas e possuem instruções configuradas na interface web.

**Recomendação:**

- para chat, produzir prompt autocontido;
- para Gem, produzir instruções persistentes compactas e separar os dados de cada uso;
- não gerar arquivos de configuração que a interface do Gem não aceite;
- não presumir tools, extensões ou acesso a apps sem confirmação do usuário;
- evitar instruções longas que repitam conhecimento anexado.

Estrutura de Gem:

```markdown
Função:
Tarefas atendidas:
Regras:
Entrada esperada:
Saída:
Dados ausentes:
Limites:
```

## 3. Gemini API

**Documentado:** a API aceita `system_instruction`; function calling conecta funções registradas; Structured Outputs gera resposta aderente a schema nos modelos/superfícies compatíveis.

Separar:

1. `system_instruction` para comportamento estável;
2. conteúdo da chamada para tarefa e dados;
3. tools/schema/configuração no SDK.

Não presumir que toda versão do Gemini suporte a mesma combinação de tools e Structured Outputs. Verificar modelo e endpoint atuais.

Usar function calling para ação/intermediação com ferramenta. Usar Structured Outputs quando a resposta final precisar de schema. Definir fallback com validação externa quando o recurso não estiver confirmado.

## 4. Antigravity IDE e CLI

**Documentado em 2026-07-30:**

- Antigravity possui IDE, CLI e SDK;
- o Agent usa ferramentas, artifacts e knowledge;
- Rules são Markdown, globais ou de workspace, e têm limite documentado de 12.000 caracteres;
- Workflows são sequências Markdown invocadas por `/nome`, também limitadas a 12.000 caracteres;
- skills seguem o padrão `SKILL.md` e podem residir em `.agents/skills/<skill>/` no workspace;
- a CLI pode ler `GEMINI.md` ou `AGENTS.md` na raiz;
- a CLI solicita confiança/permissão para ler, editar e executar no workspace.

Escolher:

- `GEMINI.md`/`AGENTS.md`: convenções duráveis do código;
- Rule: restrição persistente, global, de workspace ou por glob;
- Workflow: sequência repetível;
- skill: conhecimento/procedimento reutilizável com progressive disclosure;
- prompt atual: objetivo e unidade de trabalho.

Não inventar caminho bruto de Workflow quando apenas a criação pela interface estiver confirmada. Não assumir que regras da IDE e arquivos da CLI sejam equivalentes em todas as versões.

Prompt operacional:

```markdown
Objetivo:
Workspace/arquivos permitidos:
Arquivos proibidos:
Instruções do projeto a consultar:
Ferramentas autorizadas:
Mudanças:
Validações:
Permissões que exigem pausa:
Concluído quando:
Handoff:
```

## 5. Ferramentas, permissões e subagentes

**Documentado:** Antigravity pode usar ferramentas, MCP e subagentes assíncronos; a disponibilidade efetiva depende da superfície e configuração.

Nomear somente tools visíveis/confirmadas. Para terminal, browser, MCP, implantação ou ação externa:

- restringir alvo e diretório;
- pedir autorização quando a superfície exigir;
- preservar evidência;
- parar se a permissão for negada;
- não usar `--dangerously-skip-permissions` por padrão.

Usar subagentes somente quando confirmados e úteis para tarefas independentes. Definir contrato de retorno e verificar efeitos compartilhados.

## 6. Handoff e validação

Preferir artifact ou Markdown:

```markdown
Estado:
Objetivo:
Alterações/artefatos:
Comandos ou verificações:
Evidências:
Permissões pendentes:
Bloqueios:
Próximo passo:
```

Se uma capacidade estiver sem documentação suficiente, declarar `não confirmado` e fornecer prompt portátil sem dependência nela.

## 7. Fontes oficiais

- [Gemini API — Prompt design strategies](https://ai.google.dev/gemini-api/docs/prompting-strategies)
- [Gemini API — Text generation and system instructions](https://ai.google.dev/gemini-api/docs/text-generation)
- [Gemini API — Function calling](https://ai.google.dev/gemini-api/docs/function-calling)
- [Gemini API — Structured outputs](https://ai.google.dev/gemini-api/docs/structured-output)
- [Gemini Apps Help — Create custom Gems](https://support.google.com/gemini/answer/15235603)
- [Google Antigravity — Agent](https://antigravity.google/docs/agent)
- [Google Antigravity — Skills](https://antigravity.google/docs/skills)
- [Google Antigravity — Rules and Workflows](https://antigravity.google/docs/rules-workflows)
- [Google Antigravity CLI — Best practices](https://antigravity.google/docs/cli/best-practices)
- [Google Antigravity — Asynchronous subagents](https://antigravity.google/docs/subagents)
- [Google Codelabs — Getting started with Antigravity](https://codelabs.developers.google.com/getting-started-google-antigravity)
- [Google Codelabs — Antigravity CLI](https://codelabs.developers.google.com/antigravity-cli-hands-on)
