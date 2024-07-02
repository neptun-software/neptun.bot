from .spiders.dockerhub import DockerhubDockerRegistrySpider
from .spiders.quay import QuayDockerRegistrySpider

__all__ = ["DockerhubDockerRegistrySpider", "QuayDockerRegistrySpider"]
