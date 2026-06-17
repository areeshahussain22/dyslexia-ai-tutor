"""
Diagram Service implementation.
Generates Mermaid diagram definition strings for visual representation.
Does not render images directly; returns text definitions for frontend consumption.
"""
from typing import Optional
from src.services.llm_service import LLMService
from src.config.prompts import DIAGRAM_GENERATION_PROMPT

class DiagramService:
    def __init__(self, llm_service: Optional[LLMService] = None):
        """
        Initializes the Diagram Service.
        
        Args:
            llm_service (Optional[LLMService]): LLM engine wrapper.
        """
        self.llm_service = llm_service or LLMService()
        
    def _generate_mermaid(self, diagram_type: str, topic: str, context: str) -> str:
        """
        Helper method to generate diagrams using the LLM.
        """
        system_prompt = DIAGRAM_GENERATION_PROMPT.format(
            diagram_type=diagram_type,
            topic=topic,
            context=context
        )
        user_prompt = f"Topic: {topic}\nContext: {context}"
        
        raw_output = self.llm_service.generate_text(system_prompt, user_prompt)
        
        # Clean up any potential markdown backticks that the model might output
        cleaned = raw_output.replace("```mermaid", "").replace("```", "").strip()
        return cleaned

    def generate_flowchart(self, topic: str, context: str) -> str:
        """
        Generates a flowchart diagram (graph TD or graph LR).
        """
        return self._generate_mermaid("flowchart TD", topic, context)

    def generate_mindmap(self, topic: str, context: str) -> str:
        """
        Generates a mindmap diagram (mindmap).
        """
        return self._generate_mermaid("mindmap", topic, context)

    def generate_timeline(self, topic: str, context: str) -> str:
        """
        Generates a timeline diagram (timeline).
        """
        return self._generate_mermaid("timeline", topic, context)

    def generate_concept_map(self, topic: str, context: str) -> str:
        """
        Generates a conceptual schema map (graph TD).
        """
        return self._generate_mermaid("graph TD", topic, context)
