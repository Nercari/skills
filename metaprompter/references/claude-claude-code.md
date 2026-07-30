# Adaptador Claude e Claude Code

Pesquisa verificada em **2026-07-30**.

Rótulos:

- **Documentado:** consta em fonte oficial da Anthropic.
- **Observado:** identificado no ambiente ou artefato em análise.
- **Inferência:** conclusão provável, não garantia.
- **Recomendação:** escolha de projeto da Metaprompter.

## Sumário

1. Roteamento de superfície
2. Claude em chat, Projects e Artifacts
3. Claude API
4. Claude Code
5. Skills, agentes, hooks e permissões
6. Validação e handoff
7. Fontes oficiais

## 1. Roteamento de superfície

Separar:

| Superfície | Artefato adequado |
|---|---|
| Claude chat | prompt conversacional |
| Claude Project | instruções do projeto + knowledge |
| Claude Artifact | especificação do conteúdo/app a produzir |
| Claude API | system prompt, mensagens, tools e schema/configuração |
| Claude Code | tarefa de repositório + `CLAUDE.md`/skill/hooks/configuração |

Não aplicar sintaxe de Claude Code em Claude chat. Não apresentar Artifact como execução no repositório.

## 2. Claude em chat, Projects e Artifacts

**Documentado:** Projects mantêm chats, knowledge e instruções próprias; Artifacts separam conteúdo substancial ou interativo da conversa.

**Recomendação:**

- usar Project instructions para comportamento recorrente;
- manter fontes extensas no knowledge;
- usar Artifact somente quando o usuário pedir ou quando um artefato independente for o produto;
- mencionar web, connectors, execução de código ou criação de arquivos somente se disponíveis;
- manter instruções e conteúdo delimitados.

## 3. Claude API

**Documentado:** tools são registradas pelo parâmetro `tools` com JSON Schema; a aplicação executa a ferramenta; Structured Outputs deve ser usado quando conformidade de schema for exigida e suportada.

Gerar:

```markdown
System prompt:
[regras estáveis]

User message:
[tarefa e dados]

Runtime:
- model: [placeholder ou confirmado]
- tools: [definições reais]
- output format/schema: [quando suportado]
- validação e erros: [responsabilidade da aplicação]
```

XML pode ajudar a delimitar partes complexas, mas não usar por padrão. Não pedir cadeia de pensamento. Solicitar conclusão, critérios ou justificativa observável quando necessário.

## 4. Claude Code

**Documentado:** `CLAUDE.md` é carregado no início de sessões como contexto; skills encapsulam procedimentos; hooks executam em eventos do ciclo; subagentes podem ter prompts e ferramentas restritos; settings controlam permissões.

Gerar prompt de desenvolvimento:

```markdown
Objetivo:
Repositório e contexto:
Instruções a consultar:
Escopo permitido:
Não alterar:
Plano de implementação:
Validações obrigatórias:
Permissões:
Política de commit:
Concluído quando:
Retorno/handoff:
```

Incluir quando aplicável:

- ler `CLAUDE.md` e arquivos mais específicos;
- verificar estado do repositório e preservar mudanças do usuário;
- inspecionar antes de editar;
- não tocar em arquivos não relacionados;
- executar testes/lint/build adequados;
- registrar comandos e resultados reais;
- não fazer commit, push ou PR sem pedido;
- parar em bloqueio de permissão, requisito ou validação.

## 5. Skills, agentes, hooks e permissões

Escolher mecanismo:

- `CLAUDE.md`: fatos e regras recorrentes;
- skill em `.claude/skills/<nome>/SKILL.md`: procedimento reutilizável;
- hook: restrição determinística ou automação em evento;
- subagente: subtarefa isolada com tools/permissões próprias;
- prompt atual: objetivo imediato.

**Documentado:** Claude trata `CLAUDE.md` como contexto, não como controle técnico. Para bloquear ação independentemente da decisão do modelo, usar mecanismo determinístico como `PreToolUse` hook.

Não gerar hook sem:

- evento e matcher confirmados;
- entrada/saída esperada;
- tratamento de erro;
- teste seguro;
- explicação de efeito e permissões.

Não presumir agentes, hooks ou MCP configurados. Quando o usuário pedir apenas um prompt, não criar infraestrutura desnecessária.

## 6. Validação e handoff

Para código:

```markdown
Estado: SUCCESS | BLOCKED | FAILED_VALIDATION | ESCALATE
Arquivos alterados:
Resumo da mudança:
Testes/comandos executados:
Resultados:
Validação não executada e motivo:
Riscos/bloqueios:
Próximo passo:
```

Tratar saída de subagente como relato a verificar quando houver efeito em arquivo, serviço ou repositório compartilhado.

## 7. Fontes oficiais

- [Anthropic — Prompting best practices](https://docs.anthropic.com/en/docs/build-with-claude/prompt-engineering/claude-4-best-practices)
- [Anthropic — Tool use](https://docs.anthropic.com/en/docs/agents-and-tools/tool-use/implement-tool-use)
- [Anthropic — Output consistency and Structured Outputs](https://docs.anthropic.com/en/docs/test-and-evaluate/strengthen-guardrails/increase-consistency)
- [Claude Help — Projects](https://support.anthropic.com/en/articles/9517075-what-are-projects)
- [Claude Help — Artifacts](https://support.anthropic.com/en/articles/9487310-what-are-artifacts-and-how-do-i-use-them)
- [Claude Code — Overview](https://docs.anthropic.com/en/docs/claude-code/overview)
- [Claude Code — Memory and CLAUDE.md](https://docs.anthropic.com/en/docs/claude-code/memory)
- [Claude Code — Skills](https://docs.anthropic.com/en/docs/claude-code/skills)
- [Claude Code — Subagents](https://docs.anthropic.com/en/docs/claude-code/sub-agents)
- [Claude Code — Hooks](https://docs.anthropic.com/en/docs/claude-code/hooks)
- [Claude Code — Settings](https://docs.anthropic.com/en/docs/claude-code/settings)
