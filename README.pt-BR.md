# AI Research Agents — laboratório aberto de pesquisa em IA, com evidências

> **Convite à comunidade — 2 revisores voluntários:** precisamos de duas avaliações humanas independentes de **15 respostas reais do Qwen**, verificando se **a citação original do modelo** sustenta cada resposta. Sem programação, pagamento ou chave de API; é necessário ler os trechos originais em inglês. **[Participe na issue #52](https://github.com/AMMARICA1791/ai-research-agents/issues/52)**. A precisão semântica do modelo ainda não foi validada.


**Nossa missão:** desenvolver ferramentas de pesquisa de código que verifiquem, de forma reproduzível, alterações propostas por modelos de IA de pesos abertos, usando recursos gratuitos sempre que viável.

**Estado atual:** protótipo experimental; não é um serviço comercial nem um agente capaz de corrigir qualquer programa sozinho. O sistema possui sete etapas de trabalho, mas elas **não são sete modelos de IA independentes**.

## O que já foi demonstrado
- Análise estática limitada de código Python e de algumas dependências.
- Resumos de pesquisa anonimizados entre execuções do GitHub.
- Uso real de modelos Qwen com Ollama, sem chave de API paga.
- Uma correção de código real proposta pelo Qwen2.5-Coder 1.5B: o tratamento de URLs falsas do GitHub. Ela passou nos testes e foi integrada pelo proprietário após revisão no [PR #17](https://github.com/AMMARICA1791/ai-research-agents/pull/17).
- Um pequeno benchmark **sintético** reproduzível, que não comprova desempenho em projetos desconhecidos.

## Como experimentar
No GitHub, abra **Actions → Research Lab - Persistent Missions → Run workflow**. Use somente objetivos públicos, sem senhas ou informações privadas. Para testar um modelo local, abra **Zero-Key Local Qwen Research**. Instruções: [QUICKSTART.md](QUICKSTART.md).

## Participar da comunidade
Veja [CONTRIBUTING](CONTRIBUTING.md), [ROADMAP](ROADMAP.md), [SECURITY](SECURITY.md), [GOVERNANCE](GOVERNANCE.md) e [escopo e limitações](docs/PROJECT_SCOPE.md). Proponha experimentos reproduzíveis e relate problemas, inclusive falhas.

## Licença e direitos
O código do projeto é disponibilizado sob a [Apache License 2.0](LICENSE), aprovada pelo proprietário em outubro de 2026. Ela permite modificações, distribuição e uso comercial segundo as condições da licença; **não garante exclusividade comercial sobre o código aberto**. Os autores mantêm os direitos autorais sobre suas contribuições. Consulte [NOTICE](NOTICE), [marcas](TRADEMARKS.md) e [direitos e condições](docs/LICENSING_DECISION.md). Bibliotecas externas seguem suas próprias licenças.

**Compromisso:** nenhum resultado de IA será apresentado como comprovado sem testes e evidências verificáveis.

Idiomas: [English](README.md) · [العربية](README.ar.md) · [Español](README.es.md) · [中文](README.zh-CN.md).

## Estado atual harmonizado — outubro de 2026

- Laboratório experimental, não um SaaS pronto nem um desenvolvedor autônomo. As sete etapas são fases de orquestração, não sete agentes independentes.
- [Demonstração em três comandos](DEMO.md): Python 3.11+, sem chave de API ou modelo local; oito casos sintéticos, reparo determinístico sintético e repetição do teste histórico do [PR #17](https://github.com/AMMARICA1791/ai-research-agents/pull/17). **Não executa Qwen novamente**.
- [Auditoria de repositórios públicos Python](docs/PUBLIC_REPO_AUDIT.md): análise estática limitada sem executar código externo; indícios para revisão humana, não certificação de segurança.
- [Descoberta bibliográfica](docs/SCHOLARLY_DISCOVERY.md): metadados reais do Crossref com fonte, data de coleta e incertezas; não lê artigos completos, não avalia qualidade científica nem usa LLM.
- [Evidências da versão](VERIFIED_RELEASE.md) distinguem histórico de testes novos; [contribuições](CONTRIBUTING.md) têm escopo limitado. Sem garantia de produção.
