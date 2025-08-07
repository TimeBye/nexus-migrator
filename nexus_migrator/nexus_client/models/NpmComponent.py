from .Component import Component
from ..UploadPayload import UploadPayload


class NpmComponent(Component):

    def get_upload_payload(self) -> UploadPayload:
        payload = super().get_upload_payload()

        tgz_file = None

        for asset in self.assets:
            if asset.path.suffix == ".tgz":
                if not asset.localPath:
                    raise Exception(
                        f"Asset {asset.path.name} was not downloaded")

                tgz_file = asset.localPath

        if tgz_file:
            payload.files["npm.asset"] = open(tgz_file, "rb")
        else:
            raise Exception("No TGZ file found in component")

        return payload