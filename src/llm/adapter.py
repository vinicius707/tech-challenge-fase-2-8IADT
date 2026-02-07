from typing import Optional
import os
import json


class LLMAdapter:
    """
    Adapter for LLM providers. Supports OpenAI via OPENAI_API_KEY env var, otherwise falls back to a simple template generator.
    """
    def __init__(self, provider: str = "openai", api_key_env: str = "OPENAI_API_KEY"):
        self.provider = provider
        self.api_key = os.getenv(api_key_env)

    def generate_instructions(self, route_summary: str, prompt_template: Optional[str] = None) -> str:
        """
        Generate instructions given a route summary (string) and an optional prompt template content.
        If OpenAI API key is available and provider is 'openai', will attempt to call OpenAI.
        Otherwise returns a fallback templated instruction.
        """
        if self.provider == "openai" and self.api_key:
            try:
                import openai
                openai.api_key = self.api_key
                system = "You are an assistant that generates clear delivery instructions for hospital delivery teams."
                user_prompt = (prompt_template or "") + "\n\nRoute summary:\n" + route_summary
                resp = openai.ChatCompletion.create(
                    model="gpt-4o-mini" if getattr(openai, "ChatCompletion", None) else "gpt-4o",
                    messages=[
                        {"role": "system", "content": system},
                        {"role": "user", "content": user_prompt}
                    ],
                    max_tokens=600,
                    temperature=0.2,
                )
                # support different response shapes
                if "choices" in resp and resp["choices"]:
                    text = resp["choices"][0]["message"]["content"]
                else:
                    text = str(resp)
                return text
            except Exception as e:
                # fallback to template on error
                return self._fallback_instructions(route_summary, prompt_template, note=str(e))
        else:
            return self._fallback_instructions(route_summary, prompt_template)

    def _fallback_instructions(self, route_summary: str, prompt_template: Optional[str], note: Optional[str] = None) -> str:
        lines = []
        lines.append("INSTRUCTION (FALLBACK MODE)")
        if note:
            lines.append(f"Note: {note}")
        lines.append("")
        if prompt_template:
            lines.append("Prompt template used:")
            lines.append(prompt_template)
            lines.append("")
        lines.append("Route summary:")
        lines.append(route_summary)
        lines.append("")
        lines.append("Suggested step-by-step instructions:")
        lines.append("1) Seguir a ordem das paradas conforme listado.")
        lines.append("2) Priorizar entregas marcadas como 'high'.")
        lines.append("3) Confirmar assinatura e registrar observações.")
        lines.append("")
        lines.append("Fim das instruções.")
        return "\n".join(lines)

