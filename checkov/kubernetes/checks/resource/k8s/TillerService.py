from checkov.common.models.enums import CheckCategories, CheckResult
from checkov.kubernetes.checks.resource.base_spec_check import BaseK8Check


class TillerService(BaseK8Check):

    def __init__(self):
        name = "Ensure that the Tiller Service (Helm v2) is deleted"
        id = "CKV_K8S_44"
        # Location: container .image
        supported_kind = ['Service']
        categories = [CheckCategories.KUBERNETES]
        super().__init__(name=name, id=id, categories=categories, supported_entities=supported_kind)

    def scan_spec_conf(self, conf):

        metadata = conf.get('metadata')
        if metadata:
            if 'name' in metadata and 'tiller' in str(metadata['name']).lower():
                return CheckResult.FAILED
            labels = metadata.get('labels')
            if labels and isinstance(labels, dict):
                for v in labels.values():
                    if 'tiller' in str(v).lower():
                        return CheckResult.FAILED

        spec = conf.get('spec')
        if spec:
            selector = spec.get('selector')
            if selector and isinstance(selector, dict):
                for v in selector.values():
                    if 'tiller' in str(v).lower():
                        return CheckResult.FAILED

        return CheckResult.UNKNOWN

check = TillerService()
