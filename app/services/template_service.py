from app.models.schemas import PersonaType
from typing import Dict, Any

class TemplateService:
    def __init__(self):
        self.templates = self._load_templates()
    
    def _load_templates(self) -> Dict[PersonaType, Dict[str, Any]]:
        """Load UI templates for different personas"""
        return {
            PersonaType.HEALTH_CONSCIOUS: {
                "name": "senior_sue_template",
                "layout": "simple_overview",
                "components": {
                    "header": {
                        "type": "simple_header",
                        "show_icons": True,
                        "large_text": True
                    },
                    "results_view": {
                        "type": "simplified_cards",
                        "highlight_abnormal": True,
                        "use_plain_language": True,
                        "show_reference_ranges": False
                    },
                    "summary": {
                        "type": "text_summary",
                        "include_recommendations": True,
                        "medical_context": True
                    }
                },
                "styling": {
                    "font_size": "large",
                    "contrast": "high",
                    "colors": "medical_safe"
                },
                "prompts": {
                    "ai_instruction": "Use simple, clear language. Focus on what the patient needs to know for their diabetes management. Highlight any concerning values but reassure when appropriate.",
                    "tone": "caring, professional, reassuring",
                    "complexity": "low",
                    "focus": "health_management"
                }
            },
            PersonaType.DETAIL_ORIENTED: {
                "name": "analyst_template",
                "layout": "comprehensive_dashboard",
                "components": {
                    "header": {
                        "type": "detailed_header",
                        "show_metrics": True,
                        "show_trends": True
                    },
                    "results_view": {
                        "type": "detailed_table",
                        "show_all_data": True,
                        "include_charts": True,
                        "show_historical": True
                    },
                    "summary": {
                        "type": "analytical_summary",
                        "include_statistics": True,
                        "show_correlations": True
                    }
                },
                "styling": {
                    "font_size": "normal",
                    "contrast": "normal",
                    "colors": "professional"
                },
                "prompts": {
                    "ai_instruction": "Provide detailed analysis with specific numbers, ranges, and trends. Include technical context and explain correlations between different biomarkers.",
                    "tone": "analytical, detailed, precise",
                    "complexity": "high",
                    "focus": "comprehensive_analysis"
                }
            },
            PersonaType.QUICK_BOLD: {
                "name": "achiever_template",
                "layout": "action_focused",
                "components": {
                    "header": {
                        "type": "action_header",
                        "show_status": True,
                        "highlight_urgent": True
                    },
                    "results_view": {
                        "type": "summary_cards",
                        "show_only_abnormal": True,
                        "action_buttons": True
                    },
                    "summary": {
                        "type": "action_summary",
                        "bullet_points": True,
                        "next_steps": True
                    }
                },
                "styling": {
                    "font_size": "normal",
                    "contrast": "high",
                    "colors": "action_focused"
                },
                "prompts": {
                    "ai_instruction": "Be direct and action-oriented. Focus on what needs immediate attention and specific next steps. Keep explanations brief but actionable.",
                    "tone": "direct, motivating, action-oriented",
                    "complexity": "medium",
                    "focus": "immediate_actions"
                }
            },
            PersonaType.TECH_SAVVY: {
                "name": "innovator_template",
                "layout": "integrated_dashboard",
                "components": {
                    "header": {
                        "type": "tech_header",
                        "show_integrations": True,
                        "api_status": True
                    },
                    "results_view": {
                        "type": "interactive_charts",
                        "real_time_updates": True,
                        "export_options": True
                    },
                    "summary": {
                        "type": "data_driven_summary",
                        "include_apis": True,
                        "show_algorithms": True
                    }
                },
                "styling": {
                    "font_size": "normal",
                    "contrast": "normal",
                    "colors": "tech_modern"
                },
                "prompts": {
                    "ai_instruction": "Include technical details and data integration possibilities. Mention how values relate to wearable device data and suggest tech-enabled monitoring.",
                    "tone": "technical, innovative, data-driven",
                    "complexity": "high",
                    "focus": "technology_integration"
                }
            },
            PersonaType.BEGINNER: {
                "name": "learner_template",
                "layout": "educational_guided",
                "components": {
                    "header": {
                        "type": "educational_header",
                        "show_help": True,
                        "guided_tour": True
                    },
                    "results_view": {
                        "type": "educational_cards",
                        "explanations": True,
                        "tooltips": True
                    },
                    "summary": {
                        "type": "educational_summary",
                        "learn_more_links": True,
                        "step_by_step": True
                    }
                },
                "styling": {
                    "font_size": "large",
                    "contrast": "high",
                    "colors": "friendly"
                },
                "prompts": {
                    "ai_instruction": "Explain everything in simple terms. Include what each test measures and why it matters. Be encouraging and educational without being overwhelming.",
                    "tone": "educational, encouraging, simple",
                    "complexity": "very_low",
                    "focus": "learning_and_understanding"
                }
            }
        }
    
    async def get_template_for_persona(self, persona: PersonaType) -> Dict[str, Any]:
        """Get UI template configuration for a specific persona"""
        # Default to balanced template if persona not found
        return self.templates.get(persona, self.templates.get(PersonaType.HEALTH_CONSCIOUS, {}))
    
    async def get_ai_prompt_for_persona(self, persona: PersonaType, context: Dict[str, Any] = None) -> str:
        """Generate AI prompt based on persona and context"""
        template = await self.get_template_for_persona(persona)
        prompts = template.get("prompts", {})
        
        base_instruction = prompts.get("ai_instruction", "Provide a helpful summary of the lab results.")
        tone = prompts.get("tone", "professional")
        complexity = prompts.get("complexity", "medium")
        focus = prompts.get("focus", "general_health")
        
        # Build persona-specific prompt
        prompt = f"""
        You are a health AI assistant providing personalized lab result explanations.
        
        Persona Context:
        - Communication Style: {tone}
        - Complexity Level: {complexity}
        - Primary Focus: {focus}
        
        Instructions: {base_instruction}
        
        User Context: {context or {}}
        
        Please analyze the provided lab results and provide a response that matches this persona's preferences.
        """
        
        return prompt.strip()
    
    async def structure_ui_response(self, persona: PersonaType, content: str, lab_results: list) -> Dict[str, Any]:
        """Structure the AI response according to persona's UI template"""
        template = await self.get_template_for_persona(persona)
        components = template.get("components", {})
        
        # Structure response based on template
        ui_response = {
            "layout": template.get("layout", "default"),
            "components": {
                "header": {
                    "type": components.get("header", {}).get("type", "default"),
                    "title": "Your Health Results",
                    "subtitle": f"Personalized for {persona.value.replace('_', ' ').title()}"
                },
                "results_view": {
                    "type": components.get("results_view", {}).get("type", "default"),
                    "data": lab_results,
                    "config": components.get("results_view", {})
                },
                "summary": {
                    "type": components.get("summary", {}).get("type", "default"),
                    "content": content,
                    "config": components.get("summary", {})
                }
            },
            "styling": template.get("styling", {}),
            "persona": persona.value
        }
        
        return ui_response