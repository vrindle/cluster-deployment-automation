from k8sClient import K8sClient
from logger import logger
from concurrent.futures import Future
from typing import Dict

class ExtraConfigRT:
    def __init__(self, cc):
        self._cc = cc

    def run(self, cfg, futures: Dict[str, Future]) -> None:
        [f.result() for (_, f) in futures.items()]

        is_sno = self._cc.is_sno()

        logger.info("Running post config command to install rt kernel on worker nodes")
        client = K8sClient(self._cc["kubeconfig"])

        resource = "sno-realtime.yaml" if is_sno else "worker-realtime.yaml"
        client.oc(f"create -f manifests/rt/{resource}")

        logger.info("Waiting for mcp to update")
        name = "master" if is_sno else "worker"
        client.wait_for_mcp(name, resource)


def main():
    pass


if __name__ == "__main__":
    main()