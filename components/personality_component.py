from typing import Dict, Any

from components.base import ContextComponent


class BuyerPersonalityComponent(ContextComponent):
    def __init__(self, cfg: Dict[str, Any]):
        super().__init__()
        self.cfg = dict(cfg)

    def make_pre_act_value(self) -> str:
        return f"{self.cfg['archetype']} personality: {', '.join(self.cfg['traits'])}"

    def get_state(self) -> Dict[str, Any]:
        return {"cfg": self.cfg}

    def set_state(self, state: Dict[str, Any]) -> None:
        self.cfg = state.get("cfg", self.cfg)
