# mmpg-rout

Utilitário simples para **Windows** que cria **rota de host**: força o tráfego destinado a um **host/IP específico** a sair por um **gateway** determinado (ex.: acessar Impala/BISP por uma rede e manter a navegação comum em outra).

- Instalação: `pip install mmpg-rout`
- Import em Python: `from mmpg_rout import ensure_host_route`
- CLI opcional: `mmpg-rout --host HOST --nexthop GATEWAY [--persist]`

## Quando usar?
- Você tem **duas redes** e precisa que **apenas** um destino (ex.: `dlmg.prodemge.gov.br` – Impala/BISP) saia por um **gateway** diferente.
- Evita trocar gateway padrão manualmente: tudo continua saindo pela rede padrão, **exceto** o host roteado.

---

## 📦 Instalação

Você pode instalar a partir do TestPyPI (ou futuramente PyPI oficial):

```powershell
pip install --index-url https://test.pypi.org/simple/ --extra-index-url https://pypi.org/simple mmpg-rout
```

Se estiver desenvolvendo localmente (na pasta do projeto):

```powershell
pip install -e .
```

Isso instalará o pacote no ambiente atual (conda/venv/etc.).

---

## 🚀 Uso no código Python

### Exemplo simples:

```python
from mmpg_rout import ensure_host_route

# Cria rota temporária (só até reiniciar)
ensure_host_route("dlmg.prodemge.gov.br", "10.14.56.1")

# Cria rota persistente (fica gravada no Windows)
ensure_host_route("dlmg.prodemge.gov.br", "10.14.56.1", persist=True)
```

* `hostname` → domínio ou IP do destino.
* `nexthop` → gateway da sua rede local.
* `persist=True` → mantém a rota mesmo após reiniciar.

### Integração em projetos que usam ODBC

Basta garantir a rota antes de conectar:

```python
from mmpg_rout import ensure_host_route
import pyodbc

# Garante a rota
ensure_host_route("dlmg.prodemge.gov.br", "10.14.56.1")

# Agora conecta normalmente
conn = pyodbc.connect("Driver={Cloudera ODBC Driver for Impala};...etc...")
```

Assim, qualquer código que rodar dentro desse ambiente já terá a rota configurada.

---

## 💻 Uso via CLI (linha de comando)

Após instalar o pacote, o comando `mmpg-rout` ficará disponível no terminal.

```powershell
# Rota temporária (só até reiniciar)
mmpg-rout --host dlmg.prodemge.gov.br --nexthop 10.14.56.1

# Rota persistente (precisa rodar PowerShell como administrador)
mmpg-rout --host dlmg.prodemge.gov.br --nexthop 10.14.56.1 --persist
```

### Funcionamento do modo persistente

Se você usar `--persist`, o Windows salva a rota de forma definitiva. Isso significa que **qualquer programa** (Python, navegador, ODBC, etc.) que tentar acessar o host especificado **sempre usará o gateway configurado**, sem precisar alterar o código.

### Verificando as rotas atuais:

```powershell
route print
```

### Removendo uma rota manualmente:

```powershell
route delete 10.100.62.20
```

*(substitua pelo IP real do host que foi resolvido)*

---

## 🔧 Alterando gateway ou máscara

Se precisar mudar o gateway, basta recriar a rota:

```python
ensure_host_route("dlmg.prodemge.gov.br", "NOVO_GATEWAY", persist=True)
```

Ou pela CLI:

```powershell
mmpg-rout --host dlmg.prodemge.gov.br --nexthop NOVO_GATEWAY --persist
```

A máscara usada é sempre `/32` (`255.255.255.255`) porque a rota é criada para **um único host**.

---

## ❌ Desinstalação

Para remover a biblioteca do ambiente Python:

```powershell
pip uninstall mmpg-rout
```

Para remover a rota persistente do Windows:

```powershell
route delete 10.100.62.20
```

---

## 📌 Resumo das opções

* **No código**: garante a rota a cada execução.
* **Via CLI (temporário)**: funciona até reiniciar o PC.
* **Via CLI (persistente)**: fica registrado no Windows e vale para todos os programas.

---

## 📖 Observações importantes

* Requer execução em Windows.
* Para rotas persistentes, o PowerShell precisa estar aberto como **Administrador**.
* Expor o host `10.100.62.20` ou o gateway **não representa risco de segurança**, pois são endereços de rede interna (não roteáveis na internet).

---

## 👨‍💻 Autor

* **Valfrido Novais**
  PMMG · MMPG NOVAIS

Repositório: [github.com/ValfridoNovais/mmpg-rout](https://github.com/ValfridoNovais/mmpg-rout)
