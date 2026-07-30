# Adaptador Hermes Agent e modelos locais

Pesquisa verificada em **2026-07-30**.

Rótulos:

- **Documentado:** consta no repositório ou documentação oficial do Hermes.
- **Observado:** fornecido pelo usuário ou identificado no ambiente.
- **Inferência:** conclusão provável, não garantia.
- **Recomendação:** escolha de projeto da Metaprompter.

## Sumário

1. Perfil e limites
2. Gate de complexidade
3. Formato base
4. Modos obrigatórios
5. Ferramentas e alterações
6. Validação, parada e handoff
7. Modelos OpenAI-compatible
8. Fontes oficiais

## 1. Perfil e limites

**Documentado:** Hermes aceita endpoints customizados compatíveis com OpenAI, incluindo servidores locais; oferece toolsets, skills, persistência, limites de iteração, guardas de loop, verificação opcional e delegação configurável.

**Observado no uso do usuário:** o executor é Gemma 4 12B fine-tuned via LM Studio e perde confiabilidade com contexto longo, ambiguidade e muitas etapas.

**Recomendação obrigatória:** tratar Hermes como worker subordinado, não como orquestrador principal. Não ativar delegação, memória persistente, cron ou efeitos externos no prompt sem necessidade e confirmação.

## 2. Gate de complexidade

Antes de gerar, classificar a unidade.

Usar `microtask` quando:

- houver um objetivo e um entregável;
- entradas e caminhos estiverem definidos;
- validação puder ser concluída na mesma execução;
- não houver decisão arquitetural aberta.

Usar `bounded_worker` quando:

- houver poucas ações sequenciais dentro do mesmo objetivo;
- escopo de arquivos e ferramentas estiver fechado;
- cada ação tiver verificação objetiva.

Decompor ou emitir `escalation_request` quando houver:

- múltiplos entregáveis independentes;
- mudança transversal sem mapa de arquivos;
- requisitos conflitantes ou decisão de alto impacto;
- necessidade de pesquisa ampla, coordenação ou julgamento forte;
- validação indisponível;
- contexto necessário excessivo;
- falhas repetidas.

Não deixar o Hermes decompor autonomamente um projeto inteiro se o orquestrador puder fornecer a próxima microtarefa.

## 3. Formato base

Preferir Markdown compacto com um campo por linha. Usar JSON somente se houver parser/validador externo.

```markdown
task_id: [id]
mode: microtask | bounded_worker | verification
objective: [um resultado]
files_or_data: allow=[lista fechada]; forbid=[restante]
io: input=[contexto mínimo]; output=[arquivo, patch ou resposta]
tools: allow=[lista confirmada]; forbid=[capacidades excluídas]
scope_limit: [uma unidade]
validate: [comando/check determinístico]
success: [condições objetivas]
block_if: [condições]
stop: [sucesso ou primeira falha; não continuar]
return: [status + evidência mínima]
```

Manter o prompt `microtask` normalmente em até 12 linhas e, quando possível, até 650 caracteres sem contar dados fornecidos. Não acrescentar explicações antes ou depois. Combinar permitidos/proibidos e entrada/saída na mesma linha; omitir somente o que não se aplicar. Não transformar campos em listas narrativas quando uma linha inequívoca bastar.

Usar seções multilinha apenas em `bounded_worker` ou quando caminhos, validações ou bloqueios não couberem com clareza no contrato compacto.

## 4. Modos obrigatórios

### `microtask`

Executar uma alteração ou análise pequena. Não expandir escopo. Validar e parar. Gerar primeiro o contrato compacto acima.

### `bounded_worker`

Executar uma unidade delimitada com no máximo as fases necessárias para o mesmo entregável: inspecionar, alterar, validar. Não iniciar outro ticket.

### `verification`

Não modificar por padrão. Executar somente checks autorizados, comparar com critérios e retornar evidência. Se uma correção for necessária, emitir `blocked_result` ou `escalation_request`, salvo autorização explícita para corrigir.

### `handoff`

```markdown
task_id:
status: SUCCESS | BLOCKED | FAILED_VALIDATION | ESCALATE
completed:
outputs_or_files:
validation_run:
validation_result:
remaining:
blockers:
next_action:
```

### `blocked_result`

Usar quando faltar entrada, arquivo, ferramenta ou permissão.

```markdown
task_id:
status: BLOCKED
blocked_by:
evidence:
needed_to_resume:
no_changes_after_block: true
```

### `escalation_request`

```markdown
task_id:
status: ESCALATE
reason:
attempted:
evidence:
risk_if_continued:
recommended_split_or_route:
```

## 5. Ferramentas e alterações

Declarar nomes de tools somente após confirmar os toolsets efetivos. Caso contrário, descrever capacidades necessárias e exigir mapeamento pelo orquestrador.

Sempre definir:

- arquivos/diretórios permitidos;
- arquivos/diretórios proibidos;
- comandos de validação autorizados;
- ações externas proibidas;
- política de criação, edição e exclusão;
- política de Git.

Por padrão:

- não alterar arquivo fora da lista;
- não instalar dependência;
- não usar rede;
- não criar commit/push/PR;
- não apagar ou sobrescrever dados;
- não executar delegação;
- não persistir memória;
- não continuar após falha.

O orquestrador pode liberar exceções explícitas por tarefa.

## 6. Validação, parada e handoff

Após qualquer mudança:

1. executar exatamente a validação contratada;
2. capturar resultado e exit code quando disponível;
3. se falhar, parar como `FAILED_VALIDATION`;
4. não tentar correções fora do escopo;
5. devolver handoff mínimo.

Não confiar apenas em resumo de subagente ou mensagem de sucesso. Exigir arquivo, diff, comando, ID ou saída verificável.

Mesmo que `verify_on_stop` esteja habilitado, manter a validação no prompt: configuração de runtime não substitui o contrato da tarefa.

## 7. Modelos OpenAI-compatible

Compatibilidade de API é compatibilidade de transporte, não de capacidade.

Confirmar por modelo/servidor:

- mensagens/roles aceitos;
- tool calling e schema de tools;
- JSON/Structured Outputs;
- tamanho de contexto configurado e atenção efetiva;
- streaming;
- limites de tokens;
- retries/timeouts;
- suporte a imagens;
- comportamento de stop.

Se não confirmado:

- usar prompt portátil em texto;
- evitar dependência de tool calling;
- validar JSON externamente;
- limitar a uma unidade;
- usar contexto mínimo;
- devolver estado e parada explícitos.

## 8. Fontes oficiais

- [Nous Research — Hermes Agent](https://github.com/NousResearch/hermes-agent)
- [Hermes Agent — Providers and custom endpoints](https://github.com/NousResearch/hermes-agent/blob/main/website/docs/integrations/providers.md)
- [Hermes Agent — Toolsets reference](https://github.com/NousResearch/hermes-agent/blob/main/website/docs/reference/toolsets-reference.md)
- [Hermes Agent — Tools](https://github.com/NousResearch/hermes-agent/blob/main/website/docs/user-guide/features/tools.md)
- [Hermes Agent — Delegation](https://github.com/NousResearch/hermes-agent/blob/main/website/docs/user-guide/features/delegation.md)
- [Hermes Agent — Configuration](https://github.com/NousResearch/hermes-agent/blob/main/website/docs/user-guide/configuration.md)
- [Hermes Agent — LM Studio detection code](https://github.com/NousResearch/hermes-agent/blob/main/agent/model_metadata.py)

Limitação: o repositório evolui rapidamente. Revalidar nomes de configuração e toolsets antes de gerar arquivos executáveis para uma versão específica.
