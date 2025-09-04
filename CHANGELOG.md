# Changelog

Todas as alterações notáveis deste projeto serão documentadas aqui.

O formato é baseado em [Keep a Changelog](https://keepachangelog.com/pt-BR/1.0.0/),
e este projeto adota [Versionamento Semântico](https://semver.org/lang/pt-BR/).

---

## \[0.1.1] - 2025-09-03

### Adicionado

* Publicação bem-sucedida no **TestPyPI**.
* Instruções detalhadas de uso no README.md (uso em Python e via CLI, rotas persistentes e não persistentes, alteração de gateway, desinstalação).

### Alterado

* Ajuste no `pyproject.toml` para corrigir warnings de `license-file` e compatibilidade com `setuptools`.

### Corrigido

* Compatibilidade de build em ambientes Windows com Anaconda.

---

## \[0.1.0] - 2025-09-02

### Adicionado

* Primeira versão do pacote `mmpg-rout`.
* Função principal `ensure_host_route(hostname, nexthop, persist=False)` para criação de rotas.
* Suporte a execução via **CLI** (`mmpg-rout --host ... --nexthop ... [--persist]`).
* Licença MIT e estrutura inicial do projeto (README, .gitignore, LICENSE, pyproject.toml).
