# mmpg-rout

Utilitário simples para **Windows** que cria **rota de host**: força o tráfego destinado a um **host/IP específico** a sair por um **gateway** determinado (ex.: acessar Impala/BISP por uma rede e manter a navegação comum em outra).

- Instalação: `pip install mmpg-rout`
- Import em Python: `from mmpg_rout import ensure_host_route`
- CLI opcional: `mmpg-rout --host HOST --nexthop GATEWAY [--persist]`

> ⚠️ **Permissões**: criar/alterar rotas requer console **Executar como Administrador** (a não ser que a rota já exista).

---

## Quando usar?
- Você tem **duas redes** e precisa que **apenas** um destino (ex.: `dlmg.prodemge.gov.br` – Impala/BISP) saia por um **gateway** diferente.
- Evita trocar gateway padrão manualmente: tudo continua saindo pela rede padrão, **exceto** o host roteado.

---

## Instalação
```bash
pip install mmpg-rout
```

Instalar direto do GitHub (opcional):
```bash
pip install "git+https://github.com/ValfridoNovais/mmpg-rout.git@v0.1.0"
```

---

## Uso em Python
```python
from mmpg_rout import ensure_host_route

# Cria rota de host para o hostname resolvido (todos os A-records IPv4)
# via gateway informado. Se persist=True, grava rota persistente no SO.
ensure_host_route("dlmg.prodemge.gov.br", "10.14.56.1", persist=True)

# Depois faça sua conexão normalmente (ODBC, requests, etc.)
```

Parâmetros:
- `hostname` (str): ex. `"dlmg.prodemge.gov.br"`
- `nexthop` (str): gateway de saída, ex. `"10.14.56.1"`
- `persist` (bool): `True` cria rota **persistente** (permanece após reboot).

---

## Uso via CLI
```bash
# criar rota temporária
mmpg-rout --host dlmg.prodemge.gov.br --nexthop 10.14.56.1

# criar rota persistente (requer Admin)
mmpg-rout --host dlmg.prodemge.gov.br --nexthop 10.14.56.1 --persist
```

---

## Testes rápidos (PowerShell)
```powershell
# ver rota registrada
route print 10.100.62.20

# testar porta (ex.: Impala em 21051)
Test-NetConnection dlmg.prodemge.gov.br -Port 21051
```

---

## Como funciona
1. Resolve o `hostname` para **todos** os **IPv4** (caso haja balanceamento).
2. Para cada IP resolvido:
   - Checa se já existe rota passando por `nexthop`.
   - Se não existir, executa `route add <IP> mask 255.255.255.255 <nexthop>`  
     (`-p` quando `persist=True`).

Apenas o tráfego para o **destino** roteado usa o gateway alternativo; todo o restante continua usando o **gateway padrão** do Windows.

---

## Segurança / Boas práticas
- **Evite expor IPs internos** (ex.: `10.100.62.20`) em docs públicos. Prefira mostrar **hostname** nos exemplos.  
- Em repositório público, use exemplos genéricos (ex.: `example.internal`, `10.14.56.1`).
- No uso real, passe o **hostname** e deixe o pacote resolver o(s) IP(s).

---

## Dicas
- Se existir mais de um gateway **padrão**, ajuste a **métrica** da interface para que sua “rede 2” continue sendo o padrão.
- Para remover uma rota: `route delete <IP>`
- Para criar rota por **bloco** (se a TI informar):  
  `route -p add 10.100.62.0 mask 255.255.255.0 10.14.56.1`

---

## Solução de problemas
- **“A operação solicitada requer elevação.”**  
  Abra o **Prompt/PowerShell como Administrador**.

- **“Unexpected response from server” no ODBC**  
  Geralmente significa que o tráfego foi pela rede errada. Verifique se a rota para o IP do host foi criada com o `nexthop` correto.

- **Hostname com múltiplos IPs (balanceamento)**  
  O pacote cria rotas para **todos** os A-records IPv4 resolvidos no momento da chamada.

---

## Desenvolvimento / Publicação
Gerar artefatos e publicar no PyPI:
```bash
pip install build twine
python -m build
python -m twine upload dist/*
```

Instalar a versão publicada:
```bash
pip install mmpg-rout
```

---

## Licença
MIT.

---

## Links
- Repositório: https://github.com/ValfridoNovais/mmpg-rout
- Issues: https://github.com/ValfridoNovais/mmpg-rout/issues
