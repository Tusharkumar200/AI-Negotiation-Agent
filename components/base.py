# components/base.py
"""
Compatibility layer for Concordia ContextComponent.
We try to import Concordia's ContextComponent; if not available we provide a small fallback class.
"""

try:
    # Concordia's components may expose ContextComponent in different locations depending on version
    from gdm_concordia.components.agent import ContextComponent  # type: ignore
except Exception:
    try:
        from gdm_concordia.components import agent as agent_components  # type: ignore
        ContextComponent = getattr(agent_components, "ContextComponent", object)
    except Exception:
        class ContextComponent:
            def make_pre_act_value(self) -> str:
                return ""
            def get_state(self):
                return {}
            def set_state(self, state):
                pass
