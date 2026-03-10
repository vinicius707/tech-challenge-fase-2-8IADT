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

    def generate_report_summary(self, metrics_text: str) -> str:
        """
        Generate an executive summary of logistics metrics, including efficiency,
        time/resource economy, and suggestions for improvement.
        """
        if self.provider == "openai" and self.api_key:
            try:
                import openai
                openai.api_key = self.api_key
                system = (
                    "Você é um assistente que produz resumos executivos de relatórios logísticos hospitalares. "
                    "Sua resposta deve incluir: (1) resumo das métricas e eficiência operacional; "
                    "(2) análise de economia de tempo e recursos; "
                    "(3) sugestões de melhoria baseadas nos padrões identificados (ex.: rotas longas, "
                    "subutilização de veículos, picos de demanda). Seja conciso e acionável."
                )
                user_prompt = (
                    "Analise as métricas abaixo e produza um resumo executivo em 3-4 parágrafos, "
                    "incluindo eficiência, economia de tempo/recursos e sugestões de melhoria:\n\n"
                ) + metrics_text
                resp = openai.ChatCompletion.create(
                    model="gpt-4o-mini" if getattr(openai, "ChatCompletion", None) else "gpt-4o",
                    messages=[
                        {"role": "system", "content": system},
                        {"role": "user", "content": user_prompt}
                    ],
                    max_tokens=500,
                    temperature=0.3,
                )
                if "choices" in resp and resp["choices"]:
                    return resp["choices"][0]["message"]["content"]
            except Exception:
                pass
        return self._fallback_report_summary(metrics_text)

    def _fallback_report_summary(self, metrics_text: str) -> str:
        return (
            f"Relatório logístico (modo fallback):\n\n{metrics_text}\n\n"
            "Resumo: Revise as métricas acima. Sugestões: (1) analise rotas longas e considere "
            "rebalancear entregas entre veículos; (2) avalie picos de demanda para melhor planejamento; "
            "(3) monitore utilização de capacidade para otimizar recursos."
        )

    def answer_question(self, question: str, context: str) -> str:
        """
        Answer natural language questions about routes and deliveries using the provided context.
        """
        if self.provider == "openai" and self.api_key:
            try:
                import openai
                openai.api_key = self.api_key
                system = (
                    "Você é um assistente que responde perguntas sobre rotas de distribuição "
                    "hospitalar, entregas e planejamento logístico. Use apenas o contexto fornecido. "
                    "Se a pergunta não puder ser respondida com o contexto, indique isso."
                )
                user_prompt = f"Contexto (rotas e entregas):\n{context}\n\nPergunta: {question}"
                resp = openai.ChatCompletion.create(
                    model="gpt-4o-mini" if getattr(openai, "ChatCompletion", None) else "gpt-4o",
                    messages=[
                        {"role": "system", "content": system},
                        {"role": "user", "content": user_prompt}
                    ],
                    max_tokens=400,
                    temperature=0.2,
                )
                if "choices" in resp and resp["choices"]:
                    return resp["choices"][0]["message"]["content"]
            except Exception as e:
                return f"Erro ao consultar: {e}"
        return self._fallback_answer(question, context)

    def _fallback_answer(self, question: str, context: str) -> str:
        return (
            f"Modo fallback (sem API LLM). Pergunta: {question}\n\n"
            f"Contexto disponível:\n{context[:500]}...\n\n"
            "Configure OPENAI_API_KEY para respostas em linguagem natural."
        )

