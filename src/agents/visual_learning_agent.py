"""
Visual Learning Agent.
Handles visual adaptations, generating study flowcharts or comic stories
using DiagramService and ComicService.
"""
from typing import Optional
from src.services.diagram_service import DiagramService
from src.services.comic_service import ComicService
from src.config.settings import GENERATED_CONTENT_DIR

class VisualLearningAgent:
    def __init__(self, diagram_service: DiagramService, comic_service: ComicService):
        """
        Initializes the VisualLearningAgent.
        
        Args:
            diagram_service (DiagramService): Compiles mindmaps/flowcharts.
            comic_service (ComicService): Generates comic panels.
        """
        self.diagram_service = diagram_service
        self.comic_service = comic_service
        
    def generate_diagram(self, topic: str, context: str, lesson_id: str, diagram_type: str = "flowchart") -> str:
        """
        Generates flowchart or mindmap diagram code from text, saving it locally.
        
        Args:
            topic (str): The subject area.
            context (str): Background information.
            lesson_id (str): Unique lesson ID.
            diagram_type (str): Format ('flowchart', 'mindmap', 'timeline', 'concept_map').
            
        Returns:
            str: Filepath where the diagram text is saved.
        """
        # Choose diagram style
        if diagram_type == "mindmap":
            mermaid_code = self.diagram_service.generate_mindmap(topic, context)
        elif diagram_type == "timeline":
            mermaid_code = self.diagram_service.generate_timeline(topic, context)
        elif diagram_type == "concept_map":
            mermaid_code = self.diagram_service.generate_concept_map(topic, context)
        else:
            mermaid_code = self.diagram_service.generate_flowchart(topic, context)
            
        output_path = f"{GENERATED_CONTENT_DIR}/visuals/{lesson_id}_diagram.mermaid"
        
        with open(output_path, "w", encoding="utf-8") as f:
            f.write(mermaid_code)
            
        return output_path

    def generate_comic(self, topic: str, context: str, lesson_id: str) -> str:
        """
        Generates SVG-formatted cartoon comics from explanation details.
        
        Args:
            topic (str): The subject area.
            context (str): Core lesson text.
            lesson_id (str): Unique lesson ID.
            
        Returns:
            str: Filepath where the SVG comic is saved.
        """
        svg_content = self.comic_service.generate_comic_svg(topic, context)
        output_path = f"{GENERATED_CONTENT_DIR}/comics/{lesson_id}_comic.svg"
        
        with open(output_path, "w", encoding="utf-8") as f:
            f.write(svg_content)
            
        return output_path
