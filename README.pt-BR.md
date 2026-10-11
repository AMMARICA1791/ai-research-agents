# AI Research Agents — laboratório aberto de pesquisa em IA, com evidências

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
