from .Component import Component
import logging
from ..UploadPayload import UploadPayload

logger = logging.getLogger(__name__)


class NpmComponent(Component):

    def get_upload_payload(self) -> UploadPayload:
        payload = super().get_upload_payload()
        logger.info(f"Creating upload payload for npm component: {self.name}@{self.version}")

        # Add npm specific metadata
        if not self.name:
            raise Exception("NpmComponent name is required")
        if not self.version:
            raise Exception("NpmComponent version is required")

        payload.data["npm.name"] = self.name
        payload.data["npm.version"] = self.version

        # Add package.json content if available
        package_json = None
        tgz_file = None

        for asset in self.assets:
            if asset.path.suffix == ".tgz":
                if not asset.localPath:
                    raise Exception(
                        f"Asset {asset.path.name} was not downloaded")
                tgz_file = asset.localPath
            elif asset.path.name == "package.json":
                if not asset.localPath:
                    raise Exception(
                        f"Asset {asset.path.name} was not downloaded")
                with open(asset.localPath, 'r') as f:
                    package_json = f.read()

        if not package_json:
            raise Exception("No package.json found in component assets")
        payload.data["npm.package_json"] = package_json

        if tgz_file:
            payload.files["npm.asset"] = open(tgz_file, "rb")
            logger.info(f"Added TGZ file to payload: {tgz_file}")
            logger.info(f"Payload data: {payload.data}")
        else:
            raise Exception("No TGZ file found in component")

        return payload