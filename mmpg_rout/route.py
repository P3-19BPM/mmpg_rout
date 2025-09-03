import subprocess, socket

def ensure_host_route(hostname: str, nexthop: str, persist: bool = False) -> str:
    """
    Garante rota de host (Windows) para `hostname` via `nexthop` (gateway).
    - persist=True cria rota persistente (requer console com privilégios de Administrador)
    Retorna o último IP resolvido.
    """
    infos = socket.getaddrinfo(hostname, None, family=socket.AF_INET, type=socket.SOCK_STREAM)
    ips = sorted({info[4][0] for info in infos})
    if not ips:
        raise RuntimeError(f"Não foi possível resolver {hostname}")

    last_ip = None
    for ip in ips:
        last_ip = ip
        chk = subprocess.run(["route", "print", ip], capture_output=True, text=True)
        if nexthop not in chk.stdout:
            cmd = ["route"]
            if persist:
                cmd += ["-p"]
            cmd += ["add", ip, "mask", "255.255.255.255", nexthop]
            subprocess.run(cmd, check=True)
            print(f"[OK] rota adicionada: {ip} -> {nexthop} (persistente={persist})")
        else:
            print(f"[INFO] rota já existe para {ip} via {nexthop}")
    return last_ip

# CLI: mmpg-rout --host H --nexthop G [--persist]
def main():
    import argparse
    p = argparse.ArgumentParser(description="Garantir rota de host (Windows) via gateway específico")
    p.add_argument("--host", required=True, help="Hostname de destino (ex.: dlmg.prodemge.gov.br)")
    p.add_argument("--nexthop", required=True, help="Gateway (ex.: 10.14.56.1)")
    p.add_argument("--persist", action="store_true", help="Criar rota persistente (requer Admin)")
    a = p.parse_args()
    ensure_host_route(a.host, a.nexthop, persist=a.persist)
