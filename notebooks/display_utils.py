"""Display utilities for notebook visualizations with optimized styling and rendering.

This module provides professional, styled display functions for Jupyter notebooks.
Each display function includes responsive CSS styling, color-coded cards, and
comprehensive visual feedback for different types of content.

Available Display Categories:
-----------------------------
1. Librarian Tool Displays (Phase 2)
   - display_librarian_styles()
   - display_librarian_header()
   - display_librarian_results()
   - display_librarian_footer()

2. Analyst Tool Displays (Phase 2)
   - display_analyst_styles()
   - display_analyst_results()

3. Trend Analysis Displays (Phase 2)
   - display_trend_styles()
   - display_trend_results()

4. Tools Overview Displays (Phase 2)
   - display_tools_styles()
   - display_available_tools()

5. Gatekeeper Displays (Phase 3)
   - display_gatekeeper_styles()
   - display_gatekeeper_test()

6. Planner Displays (Phase 3)
   - display_planner_styles()
   - display_planner_test()

7. Executor Displays (Phase 3)
   - display_executor_styles()
   - display_executor_test()

8. Auditor Displays (Phase 3)
   - display_auditor_styles()
   - display_auditor_test()

9. Router Displays (Phase 3)
   - display_router_styles()
   - display_router_test()

10. Synthesizer/Strategist Displays (Phase 3)
    - display_synthesizer_styles()
    - display_synthesizer_test()

11. Red Team Displays (Phase 5) ⭐ NEW
    - display_red_team_styles()
    - display_red_team_header()
    - display_generated_prompts()
    - display_red_team_test_result()
    - display_red_team_summary()

12. Full Application Displays (Phase 4)
    - display_app_styles()
    - display_app_final_response()

Usage Example:
--------------
```python
from display_utils import display_red_team_summary

# Display comprehensive red team evaluation
display_red_team_summary(summary_df, all_evaluations)
```

All functions automatically handle:
- Responsive CSS styling
- Color-coded status indicators
- Professional card layouts
- Interactive hover effects
- Mobile-friendly displays
"""

import json
from typing import List, Dict, Any, Optional
from IPython.display import display, Markdown, HTML
import pandas as pd


# ============================================================================
# SHARED CSS STYLES
# ============================================================================

COMMON_CARD_STYLES = """
    max-width: 100%;
    overflow-wrap: break-word;
    word-wrap: break-word;
    border-radius: 8px;
    box-shadow: 0 2px 8px rgba(0,0,0,0.08);
    padding: 18px;
    margin: 15px 0;
"""

COMMON_HEADER_GRADIENT = """
    background: linear-gradient(135deg, {color1} 0%, {color2} 100%);
    padding: 20px;
    border-radius: 10px 10px 0 0;
    color: white;
    text-align: center;
    box-shadow: 0 4px 12px {shadow};
"""


def _get_common_styles():
    """Return common CSS styles used across multiple display functions."""
    return """
<style>
/* Base card styles */
.card-base {
    max-width: 100%;
    overflow-wrap: break-word;
    word-wrap: break-word;
    border-radius: 8px;
    padding: 18px;
    margin: 15px 0;
}

/* Badge styles */
.badge {
    padding: 3px 10px;
    border-radius: 12px;
    font-size: 0.85em;
    font-weight: bold;
    color: white;
}

/* Tag styles */
.tag {
    background: #f0f0f0;
    padding: 2px 8px;
    border-radius: 3px;
    font-family: monospace;
    font-size: 0.9em;
    overflow-wrap: break-word;
    word-break: break-all;
}

/* Code block styles */
.code-block {
    padding: 12px;
    border-radius: 6px;
    font-family: 'Courier New', 'Consolas', monospace;
    overflow-x: auto;
    max-width: 100%;
    white-space: pre-wrap;
}
</style>
"""


# ============================================================================
# LIBRARIAN TOOL DISPLAYS
# ============================================================================

def display_librarian_styles():
    """Display CSS styles for librarian tool output."""
    display(HTML(_get_common_styles() + """
<style>
.result-card {
    border-left: 4px solid #4A90E2;
    background: linear-gradient(to right, #f8f9fa, #ffffff);
    box-shadow: 0 2px 4px rgba(0,0,0,0.1);
}
.result-card:extend(.card-base) {}

.score-badge {
    background: #4A90E2;
}
.score-badge:extend(.badge) {}

.source-tag:extend(.tag) {}
</style>
"""))


def display_librarian_header(query: str):
    """Display header for librarian tool results."""
    gradient = COMMON_HEADER_GRADIENT.format(
        color1='#667eea', color2='#764ba2', 
        shadow='rgba(102, 126, 234, 0.3)'
    )
    display(HTML(f"""
<div style='{gradient}'>
    <h2 style='margin:0; font-size: 1.5em;'>🔍 Test du Librarian Tool</h2>
    <div style='margin-top: 15px; padding: 12px; background: rgba(255,255,255,0.1); border-radius: 6px;'>
        <div style='font-size: 0.9em; opacity: 0.9;'>📌 Requête</div>
        <div style='font-size: 1.1em; font-style: italic; margin-top: 5px;'>{query}</div>
    </div>
</div>
"""))


def display_librarian_results(results: List[Dict[str, Any]], top_k: int = 3):
    """Display librarian tool results in a formatted way.
    
    Args:
        results: List of result dictionaries with keys: source, rerank_score, summary, content
        top_k: Number of top results to display (default: 3)
    """
    if not results:
        display(Markdown("*Aucun résultat trouvé.*"))
        return
    
    display(Markdown(f"### ✨ Top {top_k} résultats les plus pertinents ({len(results)} trouvés au total)"))
    
    colors = ['#FF6B6B', '#4ECDC4', '#45B7D1']
    
    for i, result in enumerate(results[:top_k], 1):
        color = colors[i - 1] if i <= len(colors) else colors[0]
        source = result.get('source', 'Unknown')
        score = result.get('rerank_score', 0)
        summary = result.get('summary', 'No summary available')
        content = result.get('content', '')[:800]
        
        display(HTML(f"""
<div class='result-card' style='border-left-color: {color};'>
    <h4 style='color: {color}; margin-top: 0;'>📄 Résultat #{i}</h4>
    <p><strong>Source:</strong> <span class='source-tag'>{source}</span> 
       <span class='score-badge' style='background: {color};'>Score: {score:.4f}</span></p>
    <div style='margin-top: 12px; padding: 12px; background: #f8f9fa; border-left: 3px solid {color}; border-radius: 4px;'>
        <p style='margin: 0; color: #2c3e50;'><strong style='color: {color};'>💡 Résumé:</strong></p>
        <p style='margin: 8px 0 0 0; color: #34495e; line-height: 1.6;'>{summary}</p>
    </div>
</div>
<details style='margin: 10px 0;'>
    <summary><b>📖 Voir le contenu complet</b></summary>
    <pre style='background: #f8f9fa; padding: 10px; border-radius: 4px; overflow-x: auto;'>{content}...</pre>
</details>
{'<hr style="border: none; border-top: 2px dashed #e0e0e0; margin: 20px 0;">' if i < top_k else ''}
"""))


def display_librarian_footer():
    """Display footer for librarian tool results."""
    display(Markdown("---\n### ✅ Test complété avec succès!"))


# ============================================================================
# ANALYST TOOL DISPLAYS
# ============================================================================

def display_analyst_styles():
    """Display CSS styles for analyst tool output."""
    display(HTML(_get_common_styles() + """
<style>
.analyst-result-card {
    background: linear-gradient(90deg, #f8fafc 0%, #e3e8ee 100%);
    border-left: 6px solid #2b6cb0;
    color: #22223b;
    font-size: 1.08em;
}
.analyst-result-card:extend(.card-base) {}

.analyst-output {
    background: #22223b;
    color: #f2e9e4;
}
.analyst-output:extend(.code-block) {}

.analyst-sql {
    background: #f8f9fa;
    color: #1a202c;
    border: 1px solid #cbd5e0;
    margin-bottom: 10px;
}
.analyst-sql:extend(.code-block) {}
</style>
"""))


def _extract_sql_query(sql_steps: Any) -> Optional[str]:
    """Extract SQL query from intermediate steps.
    
    Args:
        sql_steps: Can be a list of tuples, a string, or None
        
    Returns:
        Extracted SQL query string or None
    """
    if not sql_steps:
        return None
        
    if isinstance(sql_steps, str):
        return sql_steps
        
    if isinstance(sql_steps, list):
        for step in sql_steps:
            if isinstance(step, tuple) and len(step) >= 2:
                action = step[0]
                if hasattr(action, 'tool_input') and isinstance(action.tool_input, dict):
                    sql_query = action.tool_input.get('query')
                    if sql_query:
                        return sql_query
    return None


def display_analyst_results(query: str, sql_steps: Any, result: str):
    """Display analyst SQL tool results.
    
    Args:
        query: The original query
        sql_steps: SQL steps from intermediate execution (can be list, tuple, or string)
        result: Final result string
    """
    display(HTML(f"""
<div class='analyst-result-card'>
    <h3 style='margin: 0 0 10px 0;'>🧑‍💼 Test du Analyst Tool</h3>
    <b>Requête :</b> <span style='color:#2b6cb0;font-weight:bold'>{query}</span>
</div>
"""))
    
    # Display final result
    display(HTML(f"""
<p style='margin: 15px 0 8px 0; color: #2c3e50; font-weight: bold; font-size: 1.05em;'>✅ Résultat final :</p>
<pre class='analyst-output code-block'>{result}</pre>
<hr style='margin: 20px 0; border: none; border-top: 1px solid #e0e0e0;'>
"""))



# ============================================================================
# TREND ANALYSIS DISPLAYS
# ============================================================================

def display_trend_styles():
    """Display CSS styles for trend analysis output."""
    display(HTML(_get_common_styles() + """
<style>
.trend-result-card {
    background: linear-gradient(90deg, #fef3e8 0%, #fff9f0 100%);
    border-left: 6px solid #f59e0b;
    box-shadow: 0 2px 8px rgba(245,158,11,0.1);
    color: #22223b;
    font-size: 1.08em;
}
.trend-result-card:extend(.card-base) {}

.trend-output {
    background: #f8f9fa;
    color: #1a202c;
    padding: 15px;
    border-radius: 6px;
    line-height: 1.6;
    border-left: 4px solid #f59e0b;
}

.trend-metric {
    background: #fef3e8;
    padding: 8px 12px;
    border-radius: 4px;
    margin: 8px 0;
    border-left: 3px solid #f59e0b;
}
</style>
"""))


def display_trend_results(query: str, result: str):
    """Display trend analysis results.
    
    Args:
        query: The original query
        result: Analysis result string
    """
    formatted_result = result.replace('\n', '<br>').replace('  ', '&nbsp;&nbsp;')
    
    display(HTML(f"""
<div class='trend-result-card'>
    <h3 style='margin: 0 0 10px 0;'>📈 Test du Advanced Analyst Tool</h3>
    <b>Requête :</b> <span style='color:#f59e0b;font-weight:bold'>{query}</span>
</div>
<p style='margin: 15px 0 8px 0; color: #2c3e50; font-weight: bold; font-size: 1.05em;'>📊 Analyse des tendances :</p>
<div class='trend-output'>{formatted_result}</div>
<hr style='margin: 20px 0; border: none; border-top: 1px solid #e0e0e0;'>
"""))



# ============================================================================
# TOOLS OVERVIEW DISPLAYS
# ============================================================================

def display_tools_styles():
    """Display CSS styles for tools overview."""
    display(HTML(_get_common_styles() + """
<style>
.tools-container {
    background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
    padding: 24px;
    border-radius: 12px;
    margin: 20px 0;
    box-shadow: 0 4px 12px rgba(102, 126, 234, 0.3);
}

.tools-title {
    color: white;
    margin: 0 0 20px 0;
    font-size: 1.5em;
    font-weight: bold;
    text-align: center;
    text-shadow: 0 2px 4px rgba(0,0,0,0.2);
}

.tool-card {
    background: white;
    border-radius: 8px;
    padding: 20px;
    margin: 15px 0;
    box-shadow: 0 2px 8px rgba(0,0,0,0.1);
    transition: transform 0.2s, box-shadow 0.2s;
}

.tool-card:hover {
    transform: translateY(-2px);
    box-shadow: 0 4px 16px rgba(0,0,0,0.15);
}

.tool-header {
    display: flex;
    align-items: center;
    margin-bottom: 12px;
    gap: 12px;
}

.tool-icon {
    font-size: 2em;
    min-width: 40px;
}

.tool-name {
    color: #2c3e50;
    font-size: 1.2em;
    font-weight: bold;
    margin: 0;
    font-family: 'Courier New', monospace;
}

.tool-description {
    color: #34495e;
    line-height: 1.6;
    margin: 0;
    padding: 12px;
    background: #f8f9fa;
    border-left: 4px solid #667eea;
    border-radius: 4px;
}

.tool-count {
    background: rgba(255,255,255,0.2);
    color: white;
    padding: 8px 16px;
    border-radius: 20px;
    display: inline-block;
    margin-bottom: 15px;
    font-weight: bold;
}
</style>
"""))


def display_available_tools(tools: List[Any], tool_map: Optional[Dict[str, Any]] = None):
    """Display available tools in a formatted card layout.
    
    Args:
        tools: List of tool objects with 'name' and 'description' attributes
        tool_map: Optional dictionary mapping tool names to tool objects (unused but kept for compatibility)
    """
    display_tools_styles()
    
    # Tool icons mapping
    TOOL_ICONS = {
        'librarian_rag_tool': '📚',
        'analyst_sql_tool': '🗃️',
        'analyst_trend_tool': '📈',
    }
    
    # Build tools HTML
    tools_html = ''.join([
        f"""
    <div class='tool-card'>
        <div class='tool-header'>
            <div class='tool-icon'>{TOOL_ICONS.get(tool.name, '🔧')}</div>
            <h3 class='tool-name'>{tool.name}</h3>
        </div>
        <p class='tool-description'>{tool.description.strip()}</p>
    </div>"""
        for tool in tools
    ])
    
    display(HTML(f"""
<div class='tools-container'>
    <h2 class='tools-title'>🛠️ Outils Disponibles</h2>
    <div class='tool-count'>📊 {len(tools)} outil(s) chargé(s)</div>
    {tools_html}
</div>
<div style='background: #d4edda; border-left: 5px solid #28a745; padding: 15px; margin: 20px 0; border-radius: 5px;'>
    <strong style='color: #155724;'>✅ Tous les outils ont été chargés avec succès!</strong>
</div>
"""))



# ============================================================================
# GATEKEEPER DISPLAYS
# ============================================================================

def display_gatekeeper_styles():
    """Display CSS styles for gatekeeper test output."""
    display(HTML(_get_common_styles() + """
<style>
.gatekeeper-container { margin: 20px 0; }

.gatekeeper-header {
    background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
    padding: 20px;
    border-radius: 10px 10px 0 0;
    color: white;
    text-align: center;
    box-shadow: 0 4px 12px rgba(102, 126, 234, 0.3);
}

.gatekeeper-title {
    margin: 0;
    font-size: 1.5em;
    font-weight: bold;
    text-shadow: 0 2px 4px rgba(0,0,0,0.2);
}

.test-case-card {
    background: white;
    border: 2px solid #e0e0e0;
    border-radius: 8px;
    margin: 15px 0;
    overflow: hidden;
    box-shadow: 0 2px 8px rgba(0,0,0,0.08);
    transition: transform 0.2s, box-shadow 0.2s;
}

.test-case-card:hover {
    transform: translateY(-2px);
    box-shadow: 0 4px 16px rgba(0,0,0,0.12);
}

.test-case-header {
    padding: 15px 20px;
    font-weight: bold;
    font-size: 1.1em;
    display: flex;
    align-items: center;
    gap: 10px;
}

.test-case-ambiguous {
    background: linear-gradient(90deg, #fff3cd 0%, #fff9e6 100%);
    border-bottom: 3px solid #ffc107;
    color: #856404;
}

.test-case-specific {
    background: linear-gradient(90deg, #d4edda 0%, #e8f5e9 100%);
    border-bottom: 3px solid #28a745;
    color: #155724;
}

.test-case-content { padding: 20px; }

.query-box {
    background: #f8f9fa;
    border-left: 4px solid #667eea;
    padding: 12px 15px;
    margin: 10px 0;
    border-radius: 4px;
    font-style: italic;
    color: #2c3e50;
}

.result-box {
    background: #f8f9fa;
    border-radius: 6px;
    padding: 15px;
    margin: 15px 0;
}

.result-label {
    font-weight: bold;
    color: #495057;
    margin-bottom: 8px;
    font-size: 0.95em;
}

.clarification-needed {
    background: #fff3cd;
    border-left: 4px solid #ffc107;
    padding: 12px 15px;
    border-radius: 4px;
    color: #856404;
}

.status-approved {
    background: #d4edda;
    border-left: 4px solid #28a745;
    padding: 12px 15px;
    border-radius: 4px;
    color: #155724;
}

.status-icon {
    font-size: 1.5em;
    margin-right: 8px;
}
</style>
"""))


def display_gatekeeper_test(ambiguous_query: str, ambiguous_result: Dict[str, Any], 
                            specific_query: str, specific_result: Dict[str, Any]):
    """Display gatekeeper test results in a formatted way.
    
    Args:
        ambiguous_query: The ambiguous test query
        ambiguous_result: Result from ambiguous query test (dict with 'clarification_question' key)
        specific_query: The specific test query
        specific_result: Result from specific query test
    """
    display_gatekeeper_styles()
    
    clarification = ambiguous_result.get('clarification_question', 'Aucune')
    
    display(HTML(f"""
<div class='gatekeeper-container'>
    <div class='gatekeeper-header'>
        <h2 class='gatekeeper-title'>🚪 Test du Gatekeeper Node</h2>
        <p style='margin: 10px 0 0 0; font-size: 0.95em; opacity: 0.95;'>
            Détection d'ambiguïté et vérification de spécificité
        </p>
    </div>
</div>

<div class='test-case-card'>
    <div class='test-case-header test-case-ambiguous'>
        <span class='status-icon'>⚠️</span>
        <span>Cas de Test 1 : Requête Ambiguë</span>
    </div>
    <div class='test-case-content'>
        <div class='result-label'>📝 Requête :</div>
        <div class='query-box'>"{ambiguous_query}"</div>
        
        <div class='result-label' style='margin-top: 15px;'>🔍 Analyse du Gatekeeper :</div>
        <div class='clarification-needed'>
            <strong>⚠️ Ambiguïté détectée</strong><br>
            <div style='margin-top: 10px; padding-top: 10px; border-top: 1px solid #ffc107;'>
                <strong>Question de clarification :</strong><br>
                <em style='color: #856404; margin-top: 5px; display: block;'>{clarification}</em>
            </div>
        </div>
    </div>
</div>

<div class='test-case-card'>
    <div class='test-case-header test-case-specific'>
        <span class='status-icon'>✅</span>
        <span>Cas de Test 2 : Requête Spécifique</span>
    </div>
    <div class='test-case-content'>
        <div class='result-label'>📝 Requête :</div>
        <div class='query-box'>"{specific_query}"</div>
        
        <div class='result-label' style='margin-top: 15px;'>🔍 Analyse du Gatekeeper :</div>
        <div class='status-approved'>
            <strong>✅ Requête approuvée</strong><br>
            <div style='margin-top: 8px; color: #155724;'>
                La requête est suffisamment spécifique. Passage au planificateur.
            </div>
        </div>
    </div>
</div>
"""))
    
    display(Markdown("""
---
### 📊 Résumé des Tests

Le **Gatekeeper** a correctement :
- 🔴 **Identifié** la requête ambiguë et généré une question de clarification appropriée
- 🟢 **Validé** la requête spécifique et autorisé la poursuite du processus

Ce mécanisme de filtrage garantit que l'agent ne travaille que sur des requêtes bien définies et à haute valeur ajoutée.
"""))



# ============================================================================
# PLANNER DISPLAYS
# ============================================================================

def display_planner_styles():
    """Display CSS styles for planner test output."""
    display(HTML(_get_common_styles() + """
<style>
.planner-container { margin: 20px 0; }

.planner-header {
    background: linear-gradient(135deg, #4A90E2 0%, #357ABD 100%);
    padding: 20px;
    border-radius: 10px 10px 0 0;
    color: white;
    text-align: center;
    box-shadow: 0 4px 12px rgba(74, 144, 226, 0.3);
}

.planner-title {
    margin: 0;
    font-size: 1.5em;
    font-weight: bold;
    text-shadow: 0 2px 4px rgba(0,0,0,0.2);
}

.planner-content {
    background: white;
    border: 2px solid #e0e0e0;
    border-top: none;
    border-radius: 0 0 10px 10px;
    padding: 25px;
    box-shadow: 0 4px 12px rgba(0,0,0,0.08);
}

.request-box {
    background: linear-gradient(90deg, #f0f7ff 0%, #e3f2fd 100%);
    border-left: 5px solid #4A90E2;
    padding: 15px 20px;
    margin: 15px 0;
    border-radius: 6px;
    font-size: 1.05em;
}

.request-label {
    font-weight: bold;
    color: #1976d2;
    margin-bottom: 8px;
    font-size: 0.95em;
    display: flex;
    align-items: center;
    gap: 8px;
}

.request-text {
    color: #2c3e50;
    font-style: italic;
    line-height: 1.6;
}

.plan-section { margin: 25px 0; }

.plan-title {
    font-weight: bold;
    color: #2c3e50;
    margin-bottom: 15px;
    font-size: 1.1em;
    display: flex;
    align-items: center;
    gap: 8px;
}

.plan-steps {
    background: #f8f9fa;
    border-radius: 8px;
    padding: 0;
    overflow: hidden;
}

.plan-step {
    padding: 15px 20px;
    border-left: 4px solid #4A90E2;
    margin: 0;
    background: white;
    border-bottom: 2px solid #e9ecef;
    transition: all 0.2s;
}

.plan-step:hover {
    background: #f8f9fa;
    border-left-width: 6px;
    padding-left: 18px;
}

.plan-step:last-child { border-bottom: none; }

.step-number {
    display: inline-block;
    background: #4A90E2;
    color: white;
    width: 28px;
    height: 28px;
    border-radius: 50%;
    text-align: center;
    line-height: 28px;
    font-weight: bold;
    margin-right: 12px;
    font-size: 0.9em;
}

.step-finish { border-left-color: #28a745 !important; }
.step-finish .step-number { background: #28a745; }

.step-content {
    display: inline-block;
    vertical-align: middle;
    color: #2c3e50;
    font-family: 'Courier New', monospace;
    font-size: 0.95em;
}

.plan-summary {
    background: linear-gradient(90deg, #d4edda 0%, #e8f5e9 100%);
    border-left: 5px solid #28a745;
    padding: 15px 20px;
    margin: 20px 0;
    border-radius: 6px;
    color: #155724;
}

.plan-summary strong { color: #0d4521; }
</style>
"""))


def display_planner_test(request: str, plan: List[str]):
    """Display planner test results in a formatted way.
    
    Args:
        request: The original user request
        plan: List of planned steps
    """
    display_planner_styles()
    
    # Build step HTML
    steps_html = ''.join([
        f"""<div class='plan-step {'step-finish' if 'FINISH' in step.upper() else ''}'>
                <span class='step-number'>{i}</span>
                <span class='step-content'>{step}</span>
            </div>"""
        for i, step in enumerate(plan, 1)
    ])
    
    tool_count = len([s for s in plan if "FINISH" not in s.upper()])
    
    display(HTML(f"""
<div class='planner-container'>
    <div class='planner-header'>
        <h2 class='planner-title'>🧠 Test du Planner Node</h2>
        <p style='margin: 10px 0 0 0; font-size: 0.95em; opacity: 0.95;'>
            Génération intelligente de plans d'action
        </p>
    </div>
    <div class='planner-content'>
        <div class='request-box'>
            <div class='request-label'>
                <span>📋</span>
                <span>Requête de l'utilisateur :</span>
            </div>
            <div class='request-text'>{request}</div>
        </div>
        
        <div class='plan-section'>
            <div class='plan-title'>
                <span>🗺️</span>
                <span>Plan d'action généré :</span>
            </div>
            <div class='plan-steps'>
                {steps_html}
            </div>
        </div>
        
        <div class='plan-summary'>
            <strong>✅ Plan généré avec succès !</strong><br>
            <div style='margin-top: 8px;'>
                📊 <strong>{tool_count}</strong> outil(s) seront utilisés pour répondre à cette requête.<br>
                🎯 Le planificateur a correctement sélectionné les outils spécialisés adaptés à la tâche.
            </div>
        </div>
    </div>
</div>
"""))
    
    display(Markdown(f"""
---
### 🔍 Analyse du Plan

Le **Planner** a démontré sa capacité à :
- 🎯 **Décomposer** une requête complexe en étapes logiques et séquentielles
- 🛠️ **Sélectionner** les outils appropriés parmi ceux disponibles ({tool_count} outil(s))
- 📋 **Structurer** un plan d'action clair avec une étape finale de terminaison

Cette planification intelligente permet à l'agent d'orchestrer efficacement ses ressources pour répondre aux besoins de l'utilisateur.
"""))



# ============================================================================
# EXECUTOR DISPLAYS
# ============================================================================

def display_executor_styles():
    """Display CSS styles for executor test output."""
    display(HTML(_get_common_styles() + """
<style>
.executor-container { margin: 20px 0; }

.executor-header {
    background: linear-gradient(135deg, #10b981 0%, #059669 100%);
    padding: 20px;
    border-radius: 10px 10px 0 0;
    color: white;
    text-align: center;
    box-shadow: 0 4px 12px rgba(16, 185, 129, 0.3);
}

.executor-title {
    margin: 0;
    font-size: 1.5em;
    font-weight: bold;
    text-shadow: 0 2px 4px rgba(0,0,0,0.2);
}

.executor-content {
    background: white;
    border: 2px solid #e0e0e0;
    border-top: none;
    border-radius: 0 0 10px 10px;
    padding: 25px;
    box-shadow: 0 4px 12px rgba(0,0,0,0.08);
}

.executor-section { margin: 20px 0; }

.executor-section-title {
    font-weight: bold;
    color: #059669;
    margin-bottom: 12px;
    font-size: 1.1em;
    display: flex;
    align-items: center;
    gap: 8px;
}

.plan-status {
    background: linear-gradient(90deg, #f0fdf4 0%, #dcfce7 100%);
    border-left: 5px solid #10b981;
    padding: 15px 20px;
    margin: 15px 0;
    border-radius: 6px;
}

.plan-status-label {
    font-weight: bold;
    color: #065f46;
    margin-bottom: 8px;
}

.plan-items {
    display: flex;
    flex-wrap: wrap;
    gap: 10px;
    margin-top: 10px;
}

.plan-item {
    background: #10b981;
    color: white;
    padding: 6px 14px;
    border-radius: 20px;
    font-size: 0.9em;
    font-family: 'Courier New', monospace;
}

.step-output {
    background: #f8fafc;
    border: 1px solid #cbd5e0;
    border-radius: 8px;
    padding: 20px;
    margin: 15px 0;
}

.step-header {
    background: linear-gradient(90deg, #10b981 0%, #059669 100%);
    color: white;
    padding: 12px 18px;
    border-radius: 6px 6px 0 0;
    margin: -20px -20px 15px -20px;
    font-weight: bold;
    display: flex;
    align-items: center;
    gap: 10px;
}

.step-detail {
    margin: 12px 0;
    padding: 10px 0;
}

.step-label {
    font-weight: bold;
    color: #475569;
    margin-bottom: 6px;
    font-size: 0.9em;
}

.step-value {
    background: white;
    border-left: 4px solid #10b981;
    padding: 12px 15px;
    border-radius: 4px;
    font-family: 'Courier New', monospace;
    font-size: 0.95em;
    color: #1e293b;
}

.step-output-data {
    background: #1e293b;
    color: #e2e8f0;
    padding: 15px;
    border-radius: 6px;
    font-family: 'Courier New', monospace;
    font-size: 0.9em;
    overflow-x: auto;
    max-height: 300px;
    overflow-y: auto;
}

.execution-summary {
    background: linear-gradient(90deg, #d1fae5 0%, #a7f3d0 100%);
    border-left: 5px solid #059669;
    padding: 15px 20px;
    margin: 20px 0;
    border-radius: 6px;
    color: #065f46;
}

.summary-metric {
    display: inline-block;
    margin-right: 20px;
    font-weight: bold;
}
</style>
"""))


def display_executor_test(plan: List[str], remaining_plan: List[str], intermediate_steps: List[Dict[str, Any]]):
    """Display executor test results in a formatted way.
    
    Args:
        plan: Original plan before execution
        remaining_plan: Plan after executing one step
        intermediate_steps: Steps executed with their outputs (each dict has tool_name, tool_input, tool_output)
    """
    display_executor_styles()
    
    # Build initial plan items HTML
    plan_items_html = ''.join([f"<span class='plan-item'>Étape {i}: {step}</span>" for i, step in enumerate(plan, 1)])
    
    # Build executed steps HTML
    executed_steps_html = ''.join([
        f"""
        <div class='step-output'>
            <div class='step-header'>
                <span>🔧</span>
                <span>Étape {idx} Exécutée</span>
            </div>
            <div class='step-detail'>
                <div class='step-label'>🛠️ Outil utilisé :</div>
                <div class='step-value'>{step.get('tool_name', 'Unknown')}</div>
            </div>
            <div class='step-detail'>
                <div class='step-label'>📝 Entrée :</div>
                <div class='step-value'>{step.get('tool_input', 'N/A')}</div>
            </div>
            <div class='step-detail'>
                <div class='step-label'>📊 Sortie de l'outil :</div>
                <div class='step-output-data'>{json.dumps(step.get('tool_output', {}), indent=2, ensure_ascii=False)}</div>
            </div>
        </div>"""
        for idx, step in enumerate(intermediate_steps, 1)
    ])
    
    # Build remaining plan HTML
    if remaining_plan:
        remaining_plan_html = "<div class='plan-items'>" + ''.join(
            [f"<span class='plan-item'>{step}</span>" for step in remaining_plan]
        ) + "</div>"
    else:
        remaining_plan_html = "<p style='color: #065f46; font-style: italic;'>✅ Aucune étape restante - Plan terminé</p>"
    
    steps_completed = len(intermediate_steps)
    steps_remaining = len(remaining_plan)
    first_tool_name = intermediate_steps[0]['tool_name'] if intermediate_steps else 'N/A'
    
    display(HTML(f"""
<div class='executor-container'>
    <div class='executor-header'>
        <h2 class='executor-title'>⚙️ Test du Tool Executor Node</h2>
        <p style='margin: 10px 0 0 0; font-size: 0.95em; opacity: 0.95;'>
            Exécution des outils et gestion des états intermédiaires
        </p>
    </div>
    <div class='executor-content'>
        <div class='executor-section'>
            <div class='executor-section-title'>
                <span>📋</span>
                <span>Plan initial :</span>
            </div>
            <div class='plan-items'>
                {plan_items_html}
            </div>
        </div>
        
        {executed_steps_html}
        
        <div class='plan-status'>
            <div class='plan-status-label'>📌 Plan restant après exécution :</div>
            {remaining_plan_html}
        </div>
        
        <div class='execution-summary'>
            <strong>✅ Exécution réussie !</strong><br>
            <div style='margin-top: 10px;'>
                <span class='summary-metric'>📊 {steps_completed} étape(s) exécutée(s)</span>
                <span class='summary-metric'>⏳ {steps_remaining} étape(s) restante(s)</span>
            </div>
        </div>
    </div>
</div>
"""))
    
    display(Markdown(f"""
---
### 🔍 Analyse de l'Exécution

Le **Tool Executor** a démontré sa capacité à :
- ⚙️ **Exécuter** l'outil sélectionné avec succès ({first_tool_name})
- 📦 **Capturer** la sortie de l'outil dans l'état intermédiaire
- 🔄 **Mettre à jour** le plan en retirant l'étape exécutée
- 📊 **Préparer** le système pour la prochaine étape du processus

L'exécuteur agit comme le travailleur du système, transformant les instructions du planificateur en actions concrètes et en gérant l'état de l'agent de manière structurée.
"""))



# ============================================================================
# AUDITOR DISPLAYS
# ============================================================================

def display_auditor_styles():
    """Display CSS styles for auditor test output."""
    display(HTML(_get_common_styles() + """
<style>
.auditor-container { margin: 20px 0; }

.auditor-header {
    background: linear-gradient(135deg, #8b5cf6 0%, #7c3aed 100%);
    padding: 20px;
    border-radius: 10px 10px 0 0;
    color: white;
    text-align: center;
    box-shadow: 0 4px 12px rgba(139, 92, 246, 0.3);
}

.auditor-title {
    margin: 0;
    font-size: 1.5em;
    font-weight: bold;
    text-shadow: 0 2px 4px rgba(0,0,0,0.2);
}

.auditor-content {
    background: white;
    border: 2px solid #e0e0e0;
    border-top: none;
    border-radius: 0 0 10px 10px;
    padding: 25px;
    box-shadow: 0 4px 12px rgba(0,0,0,0.08);
}

.audit-context {
    background: linear-gradient(90deg, #faf5ff 0%, #f3e8ff 100%);
    border-left: 5px solid #8b5cf6;
    padding: 15px 20px;
    margin: 15px 0;
    border-radius: 6px;
}

.audit-label {
    font-weight: bold;
    color: #6b21a8;
    margin-bottom: 8px;
    font-size: 0.95em;
}

.audit-value {
    color: #1e293b;
    font-style: italic;
}

.verification-result {
    background: #f8fafc;
    border: 2px solid #8b5cf6;
    border-radius: 8px;
    padding: 20px;
    margin: 20px 0;
}

.result-header {
    background: linear-gradient(90deg, #8b5cf6 0%, #7c3aed 100%);
    color: white;
    padding: 12px 18px;
    border-radius: 6px 6px 0 0;
    margin: -20px -20px 15px -20px;
    font-weight: bold;
    display: flex;
    align-items: center;
    gap: 10px;
}

.score-display {
    display: flex;
    align-items: center;
    justify-content: center;
    margin: 20px 0;
}

.score-circle {
    width: 120px;
    height: 120px;
    border-radius: 50%;
    display: flex;
    flex-direction: column;
    align-items: center;
    justify-content: center;
    font-size: 2.5em;
    font-weight: bold;
    color: white;
    box-shadow: 0 4px 12px rgba(0,0,0,0.15);
}

.score-label {
    font-size: 0.3em;
    font-weight: normal;
    margin-top: 5px;
}

.score-high { background: linear-gradient(135deg, #10b981 0%, #059669 100%); }
.score-medium { background: linear-gradient(135deg, #f59e0b 0%, #d97706 100%); }
.score-low { background: linear-gradient(135deg, #ef4444 0%, #dc2626 100%); }

.audit-metrics {
    display: grid;
    grid-template-columns: 1fr 1fr;
    gap: 15px;
    margin: 20px 0;
}

.metric-card {
    background: white;
    border: 1px solid #e5e7eb;
    border-radius: 8px;
    padding: 15px;
    text-align: center;
}

.metric-icon {
    font-size: 2em;
    margin-bottom: 8px;
}

.metric-label {
    font-size: 0.9em;
    color: #6b7280;
    margin-bottom: 5px;
}

.metric-value {
    font-size: 1.2em;
    font-weight: bold;
    color: #1e293b;
}

.metric-true { color: #059669; }
.metric-false { color: #dc2626; }

.reasoning-box {
    background: #fafafa;
    border-left: 4px solid #8b5cf6;
    padding: 15px;
    border-radius: 4px;
    margin: 15px 0;
}

.reasoning-text {
    color: #1e293b;
    line-height: 1.6;
    font-style: italic;
}

.audit-summary {
    background: linear-gradient(90deg, #ede9fe 0%, #ddd6fe 100%);
    border-left: 5px solid #7c3aed;
    padding: 15px 20px;
    margin: 20px 0;
    border-radius: 6px;
    color: #5b21b6;
}
</style>
"""))


def display_auditor_test(original_request: str, verification_result: Dict[str, Any]):
    """Display auditor test results in a formatted way.
    
    Args:
        original_request: The original user request
        verification_result: Dict with keys: confidence_score, is_consistent, is_relevant, reasoning
    """
    display_auditor_styles()
    
    # Extract verification data
    confidence_score = verification_result.get('confidence_score', 0)
    is_consistent = verification_result.get('is_consistent', False)
    is_relevant = verification_result.get('is_relevant', False)
    reasoning = verification_result.get('reasoning', 'No reasoning provided')
    
    # Determine score presentation
    if confidence_score >= 4:
        score_class, score_emoji = 'score-high', '🟢'
    elif confidence_score >= 3:
        score_class, score_emoji = 'score-medium', '🟡'
    else:
        score_class, score_emoji = 'score-low', '🔴'
    
    # Determine status
    status_text = "approuvée et peut continuer" if confidence_score >= 3 else "nécessite une replanification"
    status_icon = "✅" if confidence_score >= 3 else "⚠️"
    status_detail = ("Le système peut procéder à l'étape suivante du plan." if confidence_score >= 3 
                     else "Le routeur renverra la requête au planificateur pour essayer une nouvelle approche.")
    
    display(HTML(f"""
<div class='auditor-container'>
    <div class='auditor-header'>
        <h2 class='auditor-title'>🔍 Test du Auditor Node</h2>
        <p style='margin: 10px 0 0 0; font-size: 0.95em; opacity: 0.95;'>
            Vérification de la qualité et auto-correction cognitive
        </p>
    </div>
    <div class='auditor-content'>
        <div class='audit-context'>
            <div class='audit-label'>📝 Requête originale :</div>
            <div class='audit-value'>{original_request}</div>
        </div>
        
        <div class='verification-result'>
            <div class='result-header'>
                <span>✓</span>
                <span>Résultat de la Vérification</span>
            </div>
            
            <div class='score-display'>
                <div class='score-circle {score_class}'>
                    <div>{score_emoji}</div>
                    <div>{confidence_score}/5</div>
                    <div class='score-label'>Confiance</div>
                </div>
            </div>
            
            <div class='audit-metrics'>
                <div class='metric-card'>
                    <div class='metric-icon'>{'✅' if is_consistent else '❌'}</div>
                    <div class='metric-label'>Cohérence interne</div>
                    <div class='metric-value metric-{'true' if is_consistent else 'false'}'>
                        {'Cohérent' if is_consistent else 'Incohérent'}
                    </div>
                </div>
                <div class='metric-card'>
                    <div class='metric-icon'>{'🎯' if is_relevant else '❌'}</div>
                    <div class='metric-label'>Pertinence</div>
                    <div class='metric-value metric-{'true' if is_relevant else 'false'}'>
                        {'Pertinent' if is_relevant else 'Non pertinent'}
                    </div>
                </div>
            </div>
            
            <div style='margin-top: 20px;'>
                <div class='audit-label'>💭 Raisonnement de l'auditeur :</div>
                <div class='reasoning-box'>
                    <div class='reasoning-text'>{reasoning}</div>
                </div>
            </div>
        </div>
        
        <div class='audit-summary'>
            <strong>{status_icon} Décision de l'Auditor</strong><br>
            <div style='margin-top: 10px;'>
                La sortie de l'outil a été {status_text}.
                {status_detail}
            </div>
        </div>
    </div>
</div>
"""))
    
    display(Markdown(f"""
---
### 🔍 Analyse de la Vérification

Le **Auditor** a démontré sa capacité à :
- 🎯 **Évaluer** la pertinence de la sortie par rapport à la requête originale
- 🔍 **Vérifier** la cohérence interne des données retournées
- 📊 **Attribuer** un score de confiance quantitatif ({confidence_score}/5)
- 💭 **Justifier** sa décision avec un raisonnement clair

Cette couche d'auto-correction cognitive permet au système de détecter les sorties de faible qualité et de déclencher une replanification si nécessaire, rendant l'agent plus robuste et fiable.
"""))



# ============================================================================
# ROUTER DISPLAYS
# ============================================================================

def display_router_styles():
    """Display CSS styles for router test output."""
    display(HTML(_get_common_styles() + """
<style>
.router-container { margin: 20px 0; }

.router-header {
    background: linear-gradient(135deg, #ec4899 0%, #db2777 100%);
    padding: 20px;
    border-radius: 10px 10px 0 0;
    color: white;
    text-align: center;
    box-shadow: 0 4px 12px rgba(236, 72, 153, 0.3);
}

.router-title {
    margin: 0;
    font-size: 1.5em;
    font-weight: bold;
    text-shadow: 0 2px 4px rgba(0,0,0,0.2);
}

.router-content {
    background: white;
    border: 2px solid #e0e0e0;
    border-top: none;
    border-radius: 0 0 10px 10px;
    padding: 25px;
    box-shadow: 0 4px 12px rgba(0,0,0,0.08);
}

.router-test-case {
    background: white;
    border: 2px solid #e5e7eb;
    border-radius: 10px;
    margin: 20px 0;
    overflow: hidden;
    transition: transform 0.2s, box-shadow 0.2s;
}

.router-test-case:hover {
    transform: translateY(-2px);
    box-shadow: 0 6px 20px rgba(0,0,0,0.1);
}

.test-case-header {
    padding: 15px 20px;
    font-weight: bold;
    font-size: 1.1em;
    display: flex;
    align-items: center;
    gap: 10px;
}

.case-ambiguity {
    background: linear-gradient(90deg, #fef3c7 0%, #fde68a 100%);
    color: #92400e;
}

.case-verification {
    background: linear-gradient(90deg, #fee2e2 0%, #fecaca 100%);
    color: #991b1b;
}

.case-continue {
    background: linear-gradient(90deg, #dbeafe 0%, #bfdbfe 100%);
    color: #1e40af;
}

.case-finish {
    background: linear-gradient(90deg, #d1fae5 0%, #a7f3d0 100%);
    color: #065f46;
}

.test-case-content { padding: 20px; }

.test-scenario {
    background: #f8fafc;
    border-left: 4px solid #94a3b8;
    padding: 12px 15px;
    margin: 12px 0;
    border-radius: 4px;
}

.scenario-label {
    font-weight: bold;
    color: #475569;
    font-size: 0.9em;
    margin-bottom: 6px;
}

.scenario-value {
    font-family: 'Courier New', monospace;
    color: #1e293b;
    font-size: 0.95em;
}

.router-decision {
    background: linear-gradient(90deg, #f1f5f9 0%, #e2e8f0 100%);
    border: 2px solid #cbd5e0;
    border-radius: 8px;
    padding: 15px;
    margin: 15px 0;
}

.decision-header {
    font-weight: bold;
    color: #334155;
    margin-bottom: 10px;
    display: flex;
    align-items: center;
    gap: 8px;
}

.decision-arrow {
    font-size: 1.5em;
    color: #ec4899;
}

.decision-result {
    display: inline-block;
    background: #ec4899;
    color: white;
    padding: 8px 16px;
    border-radius: 20px;
    font-weight: bold;
    font-family: 'Courier New', monospace;
}

.decision-explanation {
    margin-top: 10px;
    padding-top: 10px;
    border-top: 1px dashed #cbd5e0;
    color: #475569;
    font-size: 0.95em;
    line-height: 1.6;
}

.router-flow-diagram {
    background: linear-gradient(135deg, #fdf4ff 0%, #fae8ff 100%);
    border: 2px solid #e879f9;
    border-radius: 8px;
    padding: 20px;
    margin: 25px 0;
}

.flow-title {
    font-weight: bold;
    color: #a21caf;
    margin-bottom: 15px;
    font-size: 1.1em;
    text-align: center;
}

.flow-steps {
    display: flex;
    flex-direction: column;
    gap: 10px;
}

.flow-step {
    background: white;
    border-left: 4px solid #ec4899;
    padding: 12px 15px;
    border-radius: 4px;
    display: flex;
    align-items: center;
    gap: 10px;
}

.flow-step-icon { font-size: 1.3em; }
.flow-step-text { color: #1e293b; }

.router-summary {
    background: linear-gradient(90deg, #fce7f3 0%, #fbcfe8 100%);
    border-left: 5px solid #db2777;
    padding: 15px 20px;
    margin: 20px 0;
    border-radius: 6px;
    color: #831843;
}
</style>
"""))


def display_router_test(test_cases: List[Dict[str, Any]]):
    """Display router test results in a formatted way.
    
    Args:
        test_cases: List of test case dicts with keys: 
            - name: str (test case name)
            - icon: str (emoji icon)
            - color_class: str (CSS class for color)
            - state: Dict (state passed to router)
            - result: str (router decision)
            - explanation: str (explanation of the decision)
    """
    display_router_styles()
    
    # Build test cases HTML
    test_cases_html = ''
    for case in test_cases:
        # Format state for display
        state_items = []
        for key, value in case['state'].items():
            if value is not None:
                if isinstance(value, list):
                    state_items.append(f"<strong>{key}:</strong> {value}")
                else:
                    state_items.append(f"<strong>{key}:</strong> '{value}'")
        state_display = '<br>'.join(state_items) if state_items else '<em>État vide</em>'
        
        test_cases_html += f"""
        <div class='router-test-case'>
            <div class='test-case-header {case['color_class']}'>
                <span style='font-size: 1.3em;'>{case['icon']}</span>
                <span>{case['name']}</span>
            </div>
            <div class='test-case-content'>
                <div class='test-scenario'>
                    <div class='scenario-label'>📊 État du système :</div>
                    <div class='scenario-value'>{state_display}</div>
                </div>
                
                <div class='router-decision'>
                    <div class='decision-header'>
                        <span class='decision-arrow'>➜</span>
                        <span>Décision du routeur :</span>
                    </div>
                    <div style='text-align: center; margin: 15px 0;'>
                        <span class='decision-result'>{case['result']}</span>
                    </div>
                    <div class='decision-explanation'>
                        {case['explanation']}
                    </div>
                </div>
            </div>
        </div>
        """
    
    display(HTML(f"""
<div class='router-container'>
    <div class='router-header'>
        <h2 class='router-title'>🧭 Test du Router Node</h2>
        <p style='margin: 10px 0 0 0; font-size: 0.95em; opacity: 0.95;'>
            Logique de navigation et gestion des flux conditionnels
        </p>
    </div>
    <div class='router-content'>
        {test_cases_html}
        
        <div class='router-flow-diagram'>
            <div class='flow-title'>🗺️ Flux de Décision du Routeur</div>
            <div class='flow-steps'>
                <div class='flow-step'>
                    <span class='flow-step-icon'>1️⃣</span>
                    <span class='flow-step-text'>Vérifier si une question de clarification existe → <strong>END</strong></span>
                </div>
                <div class='flow-step'>
                    <span class='flow-step-icon'>2️⃣</span>
                    <span class='flow-step-text'>Vérifier si le score de confiance est trop faible (&lt; 3) → <strong>planner</strong></span>
                </div>
                <div class='flow-step'>
                    <span class='flow-step-icon'>3️⃣</span>
                    <span class='flow-step-text'>Vérifier si le plan contient encore des étapes → <strong>execute_tool</strong></span>
                </div>
                <div class='flow-step'>
                    <span class='flow-step-icon'>4️⃣</span>
                    <span class='flow-step-text'>Si le plan est terminé (FINISH) → <strong>synthesize</strong></span>
                </div>
            </div>
        </div>
        
        <div class='router-summary'>
            <strong>✅ Tous les cas de test ont été validés !</strong><br>
            <div style='margin-top: 10px;'>
                Le routeur conditionnel gère correctement tous les états clés du système :
                <ul style='margin: 10px 0 0 20px;'>
                    <li>🛑 Arrêt pour clarification utilisateur</li>
                    <li>🔄 Boucle de rétroaction vers le planificateur</li>
                    <li>⚙️ Continuation de l'exécution du plan</li>
                    <li>🎯 Passage à la synthèse finale</li>
                </ul>
            </div>
        </div>
    </div>
</div>
"""))
    
    display(Markdown(f"""
---
### 🔍 Analyse du Routeur

Le **Router** est le système nerveux de notre agent. Il a démontré sa capacité à :
- 🧠 **Analyser** l'état courant du système de manière hiérarchique
- 🔀 **Décider** du prochain nœud à exécuter selon une logique conditionnelle sophistiquée
- 🔄 **Gérer** les boucles de rétroaction pour l'auto-correction
- 🎯 **Optimiser** le flux d'exécution pour maximiser la qualité des résultats

Cette logique de routage transforme notre graphe en un véritable moteur de raisonnement cognitif capable d'adaptation et d'auto-amélioration.
"""))



# ============================================================================
# SYNTHESIZER/STRATEGIST DISPLAYS
# ============================================================================

def display_synthesizer_styles():
    """Display CSS styles for synthesizer test output."""
    display(HTML(_get_common_styles() + """
<style>
.synthesizer-container { margin: 20px 0; }

.synthesizer-header {
    background: linear-gradient(135deg, #f59e0b 0%, #d97706 100%);
    padding: 25px;
    border-radius: 12px 12px 0 0;
    color: white;
    text-align: center;
    box-shadow: 0 4px 16px rgba(245, 158, 11, 0.4);
}

.synthesizer-title {
    margin: 0;
    font-size: 1.6em;
    font-weight: bold;
    text-shadow: 0 2px 4px rgba(0,0,0,0.3);
}

.synthesizer-subtitle {
    margin: 10px 0 0 0;
    font-size: 0.95em;
    opacity: 0.95;
}

.synthesizer-content {
    background: white;
    border: 2px solid #e0e0e0;
    border-top: none;
    border-radius: 0 0 12px 12px;
    padding: 30px;
    box-shadow: 0 4px 16px rgba(0,0,0,0.08);
}

.request-section {
    background: linear-gradient(90deg, #fef3e8 0%, #fff9f0 100%);
    border-left: 6px solid #f59e0b;
    padding: 18px 24px;
    margin: 20px 0;
    border-radius: 8px;
}

.request-label {
    font-weight: bold;
    color: #92400e;
    margin-bottom: 10px;
    font-size: 1em;
    display: flex;
    align-items: center;
    gap: 8px;
}

.request-text {
    color: #1e293b;
    font-size: 1.05em;
    line-height: 1.6;
    font-style: italic;
}

.context-section {
    margin: 25px 0;
}

.context-title {
    font-weight: bold;
    color: #2c3e50;
    margin-bottom: 15px;
    font-size: 1.1em;
    display: flex;
    align-items: center;
    gap: 8px;
}

.tool-output-card {
    background: #f8fafc;
    border: 2px solid #e2e8f0;
    border-radius: 8px;
    margin: 12px 0;
    overflow: hidden;
}

.tool-output-header {
    background: linear-gradient(90deg, #64748b 0%, #475569 100%);
    color: white;
    padding: 12px 18px;
    font-weight: bold;
    display: flex;
    align-items: center;
    gap: 10px;
}

.tool-output-body {
    padding: 15px 20px;
}

.tool-info-line {
    margin: 8px 0;
    color: #475569;
    font-size: 0.95em;
}

.tool-info-label {
    font-weight: bold;
    color: #334155;
}

.tool-info-value {
    font-family: 'Courier New', monospace;
    color: #1e293b;
}

.response-section {
    margin: 30px 0;
}

.response-title {
    background: linear-gradient(90deg, #f59e0b 0%, #d97706 100%);
    color: white;
    padding: 15px 20px;
    border-radius: 8px 8px 0 0;
    font-weight: bold;
    font-size: 1.15em;
    display: flex;
    align-items: center;
    gap: 10px;
    box-shadow: 0 2px 8px rgba(245, 158, 11, 0.3);
}

.response-content {
    background: #fffbf5;
    border: 2px solid #f59e0b;
    border-top: none;
    border-radius: 0 0 8px 8px;
    padding: 25px;
    line-height: 1.8;
    color: #1e293b;
}

.response-content h1,
.response-content h2,
.response-content h3 {
    color: #d97706;
    margin-top: 20px;
    margin-bottom: 12px;
}

.response-content h1 { font-size: 1.4em; }
.response-content h2 { font-size: 1.25em; }
.response-content h3 { font-size: 1.1em; }

.response-content p {
    margin: 12px 0;
}

.response-content ul,
.response-content ol {
    margin: 12px 0 12px 25px;
}

.response-content li {
    margin: 6px 0;
}

.response-content strong {
    color: #92400e;
}

.response-content em {
    color: #b45309;
}

.synthesizer-summary {
    background: linear-gradient(90deg, #fef3e8 0%, #fde68a 100%);
    border-left: 5px solid #d97706;
    padding: 20px 25px;
    margin: 25px 0;
    border-radius: 8px;
    color: #78350f;
}

.summary-highlight {
    background: rgba(245, 158, 11, 0.15);
    border-left: 3px solid #f59e0b;
    padding: 12px 15px;
    margin: 15px 0;
    border-radius: 4px;
}

.insight-badge {
    display: inline-block;
    background: #f59e0b;
    color: white;
    padding: 4px 12px;
    border-radius: 12px;
    font-size: 0.85em;
    font-weight: bold;
    margin-right: 8px;
}
</style>
"""))


def display_synthesizer_test(original_request: str, intermediate_steps: List[Dict[str, Any]], 
                             final_response: str):
    """Display synthesizer/strategist test results in a formatted way.
    
    Args:
        original_request: The original user request
        intermediate_steps: List of tool executions with their outputs
        final_response: The synthesized final response with causal inference
    """
    display_synthesizer_styles()
    
    # Build tool outputs HTML
    tools_html = ''
    for idx, step in enumerate(intermediate_steps, 1):
        tool_name = step.get('tool_name', 'Unknown')
        tool_input = step.get('tool_input', 'N/A')
        tool_output = step.get('tool_output', {})
        
        # Format output preview
        if isinstance(tool_output, str):
            output_preview = tool_output[:200] + ('...' if len(tool_output) > 200 else '')
        elif isinstance(tool_output, list):
            output_preview = f"{len(tool_output)} résultat(s) trouvé(s)"
        else:
            output_preview = json.dumps(tool_output, indent=2)[:200]
        
        tools_html += f"""
        <div class='tool-output-card'>
            <div class='tool-output-header'>
                <span>🔧</span>
                <span>Outil #{idx}: {tool_name}</span>
            </div>
            <div class='tool-output-body'>
                <div class='tool-info-line'>
                    <span class='tool-info-label'>Entrée:</span>
                    <span class='tool-info-value'>{tool_input}</span>
                </div>
                <div class='tool-info-line'>
                    <span class='tool-info-label'>Sortie:</span>
                    <pre style='background: #f1f5f9; padding: 10px; border-radius: 4px; margin: 8px 0; overflow-x: auto; font-size: 0.9em;'>{output_preview}</pre>
                </div>
            </div>
        </div>
        """
    
    display(HTML(f"""
<div class='synthesizer-container'>
    <div class='synthesizer-header'>
        <h2 class='synthesizer-title'>🧠 Test du Strategist (Synthesizer) Node</h2>
        <p class='synthesizer-subtitle'>
            Synthèse avec inférence causale et génération d'insights
        </p>
    </div>
    <div class='synthesizer-content'>
        <div class='request-section'>
            <div class='request-label'>
                <span>📋</span>
                <span>Requête originale de l'utilisateur :</span>
            </div>
            <div class='request-text'>{original_request}</div>
        </div>
        
        <div class='context-section'>
            <div class='context-title'>
                <span>📊</span>
                <span>Contexte des agents spécialisés ({len(intermediate_steps)} outil(s) exécuté(s)) :</span>
            </div>
            {tools_html}
        </div>
        
        <div class='context-section'>
            <div class='context-title'>
                <span>📊</span>
                <span>Contexte des agents spécialisés ({len(intermediate_steps)} outil(s) exécuté(s)) :</span>
            </div>
            {tools_html}
        </div>
        
        <div class='synthesizer-summary'>
            <strong>✅ Synthèse réussie avec inférence causale !</strong>
            <div class='summary-highlight' style='margin-top: 15px;'>
                <span class='insight-badge'>💡 Insight</span>
                <strong>Le Strategist ne se contente pas de compiler les données.</strong><br>
                <div style='margin-top: 10px;'>
                    Il analyse les connexions entre les différentes informations recueillies par les outils spécialisés 
                    et génère des hypothèses causales fondées sur les données, imitant le raisonnement d'un analyste expert.
                </div>
            </div>
        </div>
    </div>
</div>
"""))
    
    # Display the final response in a separate section with proper Markdown rendering
    display(HTML("""
<div style='margin: 20px 0;'>
    <div style='background: linear-gradient(90deg, #f59e0b 0%, #d97706 100%); color: white; padding: 15px 20px; border-radius: 8px 8px 0 0; font-weight: bold; font-size: 1.15em; display: flex; align-items: center; gap: 10px; box-shadow: 0 2px 8px rgba(245, 158, 11, 0.3);'>
        <span>✨</span>
        <span>Réponse Finale Synthétisée</span>
    </div>
</div>
"""))
    
    display(Markdown(final_response))
    
    display(Markdown(f"""
---
### 🔍 Analyse de la Synthèse

Le **Strategist** a démontré sa capacité à :
- 📊 **Compiler** les résultats de {len(intermediate_steps)} outil(s) spécialisé(s) de manière cohérente
- 🔗 **Connecter** les informations provenant de sources différentes (données quantitatives et qualitatives)
- 💭 **Générer** des hypothèses causales et des insights au-delà de la simple compilation
- 📝 **Articuler** une réponse claire, structurée et à haute valeur ajoutée

Cette capacité d'**inférence causale** transforme notre agent d'un simple agrégateur de données en un véritable **moteur de raisonnement** capable de générer des perspectives analytiques comparables à celles d'un expert humain.
"""))



# ============================================================================
# RED TEAMING DISPLAYS
# ============================================================================

def display_red_team_styles():
    """Display CSS styles for red teaming output."""
    display(HTML(_get_common_styles() + """
<style>
.red-team-container { margin: 20px 0; }

.red-team-header {
    background: linear-gradient(135deg, #dc2626 0%, #991b1b 100%);
    padding: 25px;
    border-radius: 12px 12px 0 0;
    color: white;
    text-align: center;
    box-shadow: 0 4px 16px rgba(220, 38, 38, 0.4);
}

.red-team-title {
    margin: 0;
    font-size: 1.6em;
    font-weight: bold;
    text-shadow: 0 2px 4px rgba(0,0,0,0.3);
    display: flex;
    align-items: center;
    justify-content: center;
    gap: 12px;
}

.red-team-subtitle {
    margin: 10px 0 0 0;
    font-size: 0.95em;
    opacity: 0.95;
}

.red-team-content {
    background: white;
    border: 2px solid #fee2e2;
    border-top: none;
    border-radius: 0 0 12px 12px;
    padding: 30px;
    box-shadow: 0 4px 16px rgba(0,0,0,0.08);
}

.attack-vector-card {
    background: white;
    border: 2px solid #fecaca;
    border-radius: 10px;
    margin: 20px 0;
    overflow: hidden;
    transition: transform 0.2s, box-shadow 0.2s;
}

.attack-vector-card:hover {
    transform: translateY(-2px);
    box-shadow: 0 6px 20px rgba(220, 38, 38, 0.15);
}

.attack-header {
    background: linear-gradient(90deg, #fef2f2 0%, #fee2e2 100%);
    border-bottom: 3px solid #dc2626;
    padding: 15px 20px;
    font-weight: bold;
    font-size: 1.15em;
    color: #991b1b;
    display: flex;
    align-items: center;
    gap: 10px;
}

.attack-content { padding: 20px; }

.prompt-box {
    background: #fffbeb;
    border-left: 5px solid #fbbf24;
    padding: 15px 20px;
    margin: 15px 0;
    border-radius: 6px;
}

.prompt-label {
    font-weight: bold;
    color: #92400e;
    margin-bottom: 8px;
    font-size: 0.95em;
}

.prompt-text {
    color: #1e293b;
    font-style: italic;
    line-height: 1.6;
}

.reasoning-box {
    background: #f3f4f6;
    border-left: 4px solid #6b7280;
    padding: 12px 15px;
    margin: 10px 0;
    border-radius: 4px;
}

.reasoning-text {
    color: #374151;
    font-size: 0.95em;
    line-height: 1.5;
}

.response-test-box {
    background: #fafafa;
    border: 2px solid #e5e7eb;
    border-radius: 8px;
    padding: 18px;
    margin: 15px 0;
}

.response-test-label {
    font-weight: bold;
    color: #1f2937;
    margin-bottom: 10px;
    display: flex;
    align-items: center;
    gap: 8px;
}

.response-test-text {
    background: white;
    border-left: 3px solid #4b5563;
    padding: 12px 15px;
    border-radius: 4px;
    color: #1e293b;
    line-height: 1.6;
}

.evaluation-result {
    background: white;
    border: 2px solid #e5e7eb;
    border-radius: 10px;
    margin: 20px 0;
    overflow: hidden;
}

.eval-header {
    padding: 15px 20px;
    font-weight: bold;
    font-size: 1.1em;
    display: flex;
    align-items: center;
    gap: 10px;
}

.eval-robust {
    background: linear-gradient(90deg, #d1fae5 0%, #a7f3d0 100%);
    border-bottom: 3px solid #059669;
    color: #065f46;
}

.eval-vulnerable {
    background: linear-gradient(90deg, #fee2e2 0%, #fecaca 100%);
    border-bottom: 3px solid #dc2626;
    color: #991b1b;
}

.eval-content { padding: 20px; }

.eval-badge {
    display: inline-block;
    padding: 6px 14px;
    border-radius: 20px;
    font-size: 0.9em;
    font-weight: bold;
    color: white;
}

.badge-robust { background: #059669; }
.badge-vulnerable { background: #dc2626; }
.badge-neutral { background: #6b7280; }

.eval-metrics {
    display: grid;
    grid-template-columns: 1fr 1fr;
    gap: 15px;
    margin: 20px 0;
}

.eval-metric-card {
    background: #f9fafb;
    border: 1px solid #e5e7eb;
    border-radius: 8px;
    padding: 15px;
}

.metric-title {
    font-size: 0.85em;
    color: #6b7280;
    margin-bottom: 8px;
    text-transform: uppercase;
    letter-spacing: 0.5px;
}

.metric-value {
    font-size: 1.3em;
    font-weight: bold;
    color: #1e293b;
}

.summary-table-wrapper {
    background: white;
    border: 2px solid #e5e7eb;
    border-radius: 10px;
    padding: 25px;
    margin: 25px 0;
    box-shadow: 0 4px 12px rgba(0,0,0,0.08);
}

.summary-table-title {
    font-size: 1.3em;
    font-weight: bold;
    color: #1f2937;
    margin-bottom: 20px;
    display: flex;
    align-items: center;
    gap: 10px;
    padding-bottom: 15px;
    border-bottom: 3px solid #dc2626;
}

.red-team-summary {
    background: linear-gradient(135deg, #fef2f2 0%, #fee2e2 100%);
    border-left: 6px solid #dc2626;
    padding: 25px 30px;
    margin: 25px 0;
    border-radius: 8px;
}

.summary-title {
    font-size: 1.2em;
    font-weight: bold;
    color: #991b1b;
    margin-bottom: 15px;
    display: flex;
    align-items: center;
    gap: 10px;
}

.summary-stats {
    display: grid;
    grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
    gap: 15px;
    margin: 20px 0;
}

.stat-card {
    background: white;
    border-radius: 8px;
    padding: 15px;
    text-align: center;
    border: 2px solid #fecaca;
}

.stat-number {
    font-size: 2.5em;
    font-weight: bold;
    margin: 10px 0;
}

.stat-label {
    color: #6b7280;
    font-size: 0.9em;
    text-transform: uppercase;
    letter-spacing: 0.5px;
}

.stat-success { color: #059669; }
.stat-warning { color: #f59e0b; }
.stat-danger { color: #dc2626; }

.vector-breakdown {
    background: white;
    border-radius: 8px;
    padding: 20px;
    margin: 20px 0;
}

.vector-item {
    padding: 12px 15px;
    margin: 10px 0;
    border-radius: 6px;
    border-left: 4px solid #dc2626;
    background: #fafafa;
    display: flex;
    justify-content: space-between;
    align-items: center;
}

.vector-name {
    font-weight: bold;
    color: #1f2937;
}

.vector-result {
    font-weight: bold;
    padding: 4px 12px;
    border-radius: 12px;
    font-size: 0.9em;
}

.result-pass {
    background: #d1fae5;
    color: #065f46;
}

.result-fail {
    background: #fee2e2;
    color: #991b1b;
}
</style>
"""))


def display_red_team_header(attack_vector: str):
    """Display header for red team prompt generation.
    
    Args:
        attack_vector: The attack vector being tested
    """
    display_red_team_styles()
    
    display(HTML(f"""
<div class='red-team-container'>
    <div class='red-team-header'>
        <h2 class='red-team-title'>
            <span>🎯</span>
            <span>Génération de Prompts Adversariaux</span>
            <span>🎯</span>
        </h2>
        <p class='red-team-subtitle'>Test Red Team - Vecteur d'Attaque: {attack_vector}</p>
    </div>
</div>
"""))


def display_generated_prompts(attack_vector: str, prompts: List[Dict[str, str]]):
    """Display generated adversarial prompts.
    
    Args:
        attack_vector: The attack vector tested
        prompts: List of prompt dicts with 'prompt' and 'reasoning' keys
    """
    prompts_html = ''
    for idx, p in enumerate(prompts, 1):
        prompts_html += f"""
        <div class='attack-vector-card'>
            <div class='attack-header'>
                <span>⚠️</span>
                <span>Prompt Adversarial #{idx}</span>
            </div>
            <div class='attack-content'>
                <div class='prompt-box'>
                    <div class='prompt-label'>📝 Prompt:</div>
                    <div class='prompt-text'>"{p['prompt']}"</div>
                </div>
                <div class='reasoning-box'>
                    <strong style='color: #374151;'>💭 Raisonnement:</strong>
                    <div class='reasoning-text'>{p['reasoning']}</div>
                </div>
            </div>
        </div>
        """
    
    display(HTML(f"""
<div class='red-team-content'>
    <h3 style='color: #991b1b; margin-bottom: 20px; display: flex; align-items: center; gap: 10px;'>
        <span>🎯</span>
        <span>Vecteur d'Attaque: {attack_vector}</span>
    </h3>
    {prompts_html}
</div>
"""))


def display_red_team_test_result(attack_vector: str, prompt: str, response: str, 
                                 evaluation: Optional[Dict[str, Any]] = None):
    """Display a single red team test result.
    
    Args:
        attack_vector: The attack vector tested
        prompt: The adversarial prompt
        response: Agent's response
        evaluation: Optional evaluation dict with keys: is_vulnerable, vulnerability_type, reasoning
    """
    eval_html = ''
    if evaluation:
        is_vulnerable = evaluation.get('is_vulnerable', False)
        vuln_type = evaluation.get('vulnerability_type', 'N/A')
        reasoning = evaluation.get('reasoning', 'No reasoning provided')
        
        eval_class = 'eval-vulnerable' if is_vulnerable else 'eval-robust'
        eval_icon = '❌' if is_vulnerable else '✅'
        eval_status = 'VULNÉRABLE' if is_vulnerable else 'ROBUSTE'
        badge_class = 'badge-vulnerable' if is_vulnerable else 'badge-robust'
        
        eval_html = f"""
        <div class='evaluation-result'>
            <div class='eval-header {eval_class}'>
                <span>{eval_icon}</span>
                <span>Évaluation: {eval_status}</span>
            </div>
            <div class='eval-content'>
                <div style='margin-bottom: 15px;'>
                    <span class='eval-badge {badge_class}'>{eval_status}</span>
                    <span class='eval-badge badge-neutral'>{vuln_type}</span>
                </div>
                <div class='reasoning-box'>
                    <strong style='color: #374151;'>💭 Analyse:</strong>
                    <div class='reasoning-text'>{reasoning}</div>
                </div>
            </div>
        </div>
        """
    
    display(HTML(f"""
<div class='attack-vector-card'>
    <div class='attack-header'>
        <span>🎯</span>
        <span>{attack_vector}</span>
    </div>
    <div class='attack-content'>
        <div class='prompt-box'>
            <div class='prompt-label'>⚠️ Prompt Adversarial:</div>
            <div class='prompt-text'>"{prompt}"</div>
        </div>
        <div class='response-test-box'>
            <div class='response-test-label'>
                <span>🤖</span>
                <span>Réponse de l'Agent:</span>
            </div>
            <div class='response-test-text'>{response}</div>
        </div>
        {eval_html}
    </div>
</div>
"""))


def display_red_team_summary(summary_df: pd.DataFrame, all_evaluations: List[Dict[str, Any]]):
    """Display comprehensive red team evaluation summary.
    
    Args:
        summary_df: Pandas DataFrame with summary statistics (from pivot table)
        all_evaluations: List of evaluation dicts with 'attack_vector' and 'is_vulnerable' keys
    """
    # Calculate overall statistics
    total_tests = len(all_evaluations)
    total_robust = sum(1 for e in all_evaluations if not e['is_vulnerable'])
    total_vulnerable = total_tests - total_robust
    success_rate = (total_robust / total_tests * 100) if total_tests > 0 else 0
    
    # Build vector breakdown
    vector_stats = {}
    for eval_item in all_evaluations:
        vector = eval_item['attack_vector']
        if vector not in vector_stats:
            vector_stats[vector] = {'robust': 0, 'vulnerable': 0}
        
        if eval_item['is_vulnerable']:
            vector_stats[vector]['vulnerable'] += 1
        else:
            vector_stats[vector]['robust'] += 1
    
    vector_html = ''
    for vector, stats in vector_stats.items():
        total = stats['robust'] + stats['vulnerable']
        rate = (stats['robust'] / total * 100) if total > 0 else 0
        result_class = 'result-pass' if rate == 100 else 'result-fail'
        
        vector_html += f"""
        <div class='vector-item'>
            <span class='vector-name'>{vector}</span>
            <span class='vector-result {result_class}'>
                {stats['robust']}/{total} Robuste ({rate:.0f}%)
            </span>
        </div>
        """
    
    # Determine overall status
    if success_rate == 100:
        status_color = 'stat-success'
        status_icon = '🟢'
        status_text = 'EXCELLENT'
    elif success_rate >= 80:
        status_color = 'stat-success'
        status_icon = '🟢'
        status_text = 'BON'
    elif success_rate >= 60:
        status_color = 'stat-warning'
        status_icon = '🟡'
        status_text = 'MOYEN'
    else:
        status_color = 'stat-danger'
        status_icon = '🔴'
        status_text = 'FAIBLE'
    
    display(HTML(f"""
<div class='red-team-summary'>
    <div class='summary-title'>
        <span>📊</span>
        <span>Résumé de l'Évaluation Red Team</span>
    </div>
    
    <div class='summary-stats'>
        <div class='stat-card'>
            <div class='stat-label'>Tests Totaux</div>
            <div class='stat-number' style='color: #3b82f6;'>{total_tests}</div>
        </div>
        <div class='stat-card'>
            <div class='stat-label'>Réponses Robustes</div>
            <div class='stat-number stat-success'>{total_robust}</div>
        </div>
        <div class='stat-card'>
            <div class='stat-label'>Vulnérabilités</div>
            <div class='stat-number stat-danger'>{total_vulnerable}</div>
        </div>
        <div class='stat-card'>
            <div class='stat-label'>Taux de Réussite</div>
            <div class='stat-number {status_color}'>{success_rate:.1f}%</div>
            <div style='margin-top: 8px;'><strong>{status_icon} {status_text}</strong></div>
        </div>
    </div>
    
    <div class='vector-breakdown'>
        <h4 style='color: #1f2937; margin-bottom: 15px; display: flex; align-items: center; gap: 8px;'>
            <span>🎯</span>
            <span>Résultats par Vecteur d'Attaque</span>
        </h4>
        {vector_html}
    </div>
</div>
"""))
    
    # Display DataFrame table
    display(HTML("""
<div class='summary-table-wrapper'>
    <div class='summary-table-title'>
        <span>📈</span>
        <span>Tableau Récapitulatif Détaillé</span>
    </div>
</div>
"""))
    
    display(summary_df)
    
    # Display insights
    insights = []
    
    if success_rate == 100:
        insights.append("✅ <strong>Excellente robustesse</strong> : L'agent a résisté à tous les vecteurs d'attaque testés.")
    elif success_rate >= 80:
        insights.append("✅ <strong>Bonne robustesse globale</strong> : L'agent montre une bonne résistance aux attaques adversariales.")
    else:
        insights.append("⚠️ <strong>Améliorations nécessaires</strong> : L'agent présente des vulnérabilités qui doivent être corrigées.")
    
    for vector, stats in vector_stats.items():
        if stats['vulnerable'] > 0:
            insights.append(f"🔍 <strong>{vector}</strong> : {stats['vulnerable']} vulnérabilité(s) détectée(s).")
    
    if not any(stats['vulnerable'] > 0 for stats in vector_stats.values()):
        insights.append("🛡️ <strong>Protection complète</strong> : Aucune vulnérabilité détectée sur tous les vecteurs d'attaque.")
    
    insights_html = '<br>'.join(f"<div style='margin: 8px 0;'>{insight}</div>" for insight in insights)
    
    display(HTML(f"""
<div style='background: linear-gradient(90deg, #eff6ff 0%, #dbeafe 100%); border-left: 5px solid #3b82f6; padding: 20px 25px; margin: 25px 0; border-radius: 8px;'>
    <h4 style='color: #1e40af; margin: 0 0 15px 0; display: flex; align-items: center; gap: 8px;'>
        <span>💡</span>
        <span>Insights & Recommandations</span>
    </h4>
    {insights_html}
</div>
"""))


# ============================================================================
# RUN APP DISPLAYS
# ============================================================================

def display_run_app_styles():
    """Display CSS styles for run app test output."""
    display(HTML(_get_common_styles() + """
<style>
.run-app-container {
    margin: 30px 0;
    border-radius: 12px;
    overflow: hidden;
    box-shadow: 0 6px 24px rgba(0,0,0,0.12);
}

.run-app-header {
    background: linear-gradient(135deg, #6366f1 0%, #4f46e5 100%);
    padding: 25px;
    color: white;
    text-align: center;
}

.run-app-title {
    margin: 0;
    font-size: 1.8em;
    font-weight: bold;
    text-shadow: 0 2px 6px rgba(0,0,0,0.3);
    display: flex;
    align-items: center;
    justify-content: center;
    gap: 15px;
}

.run-app-query-box {
    background: rgba(255,255,255,0.15);
    border: 2px solid rgba(255,255,255,0.3);
    padding: 15px 20px;
    margin: 15px 0 0 0;
    border-radius: 8px;
}

.run-app-query-label {
    font-size: 0.9em;
    opacity: 0.9;
    margin-bottom: 8px;
    font-weight: 600;
}

.run-app-query-text {
    font-size: 1.15em;
    font-style: italic;
    line-height: 1.5;
}

.run-app-body {
    background: white;
    padding: 30px;
}

.test-type-badge {
    display: inline-block;
    padding: 8px 18px;
    border-radius: 20px;
    font-weight: bold;
    font-size: 0.9em;
    margin-bottom: 20px;
}

.badge-ambiguous {
    background: linear-gradient(90deg, #fbbf24 0%, #f59e0b 100%);
    color: #78350f;
}

.badge-specific {
    background: linear-gradient(90deg, #34d399 0%, #10b981 100%);
    color: #065f46;
}

.clarification-container {
    background: linear-gradient(135deg, #fff3cd 0%, #fff9e6 100%);
    border: 3px solid #fbbf24;
    border-radius: 12px;
    padding: 25px;
    margin: 20px 0;
}

.clarification-header {
    display: flex;
    align-items: center;
    gap: 12px;
    margin-bottom: 15px;
}

.clarification-icon {
    font-size: 2.5em;
}

.clarification-title {
    font-size: 1.3em;
    font-weight: bold;
    color: #92400e;
    margin: 0;
}

.clarification-content {
    background: white;
    border-left: 5px solid #fbbf24;
    padding: 18px 22px;
    border-radius: 6px;
    color: #1e293b;
    font-size: 1.05em;
    line-height: 1.7;
}

.response-container {
    background: #f8fafc;
    border: 3px solid #10b981;
    border-radius: 12px;
    padding: 25px;
    margin: 20px 0;
}

.response-header {
    display: flex;
    align-items: center;
    gap: 12px;
    margin-bottom: 20px;
}

.response-icon {
    font-size: 2.5em;
}

.response-title {
    font-size: 1.3em;
    font-weight: bold;
    color: #065f46;
    margin: 0;
}

.response-content {
    background: white;
    border-left: 5px solid #10b981;
    padding: 22px 26px;
    border-radius: 8px;
    color: #1e293b;
    line-height: 1.8;
}

.response-content h1,
.response-content h2,
.response-content h3,
.response-content h4 {
    color: #059669;
    margin-top: 20px;
    margin-bottom: 12px;
}

.response-content p {
    margin: 12px 0;
}

.response-content ul,
.response-content ol {
    margin: 12px 0 12px 25px;
}

.response-content li {
    margin: 8px 0;
}

.response-content strong {
    color: #047857;
    font-weight: 600;
}

.response-content em {
    color: #059669;
    font-style: italic;
}

.response-content code {
    background: #f1f5f9;
    padding: 2px 6px;
    border-radius: 3px;
    font-family: 'Courier New', monospace;
    font-size: 0.9em;
    color: #0f172a;
}

.run-summary {
    background: linear-gradient(90deg, #ede9fe 0%, #ddd6fe 100%);
    border-left: 5px solid #8b5cf6;
    padding: 20px 25px;
    margin: 25px 0;
    border-radius: 8px;
    color: #5b21b6;
}

.run-summary strong {
    color: #6b21a8;
}

.execution-stats {
    display: grid;
    grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
    gap: 15px;
    margin: 20px 0;
}

.stat-card {
    background: white;
    border: 2px solid #e5e7eb;
    border-radius: 8px;
    padding: 15px;
    text-align: center;
}

.stat-icon {
    font-size: 2em;
    margin-bottom: 8px;
}

.stat-label {
    font-size: 0.85em;
    color: #6b7280;
    margin-bottom: 5px;
}

.stat-value {
    font-size: 1.3em;
    font-weight: bold;
    color: #1e293b;
}

.separator {
    height: 3px;
    background: linear-gradient(90deg, transparent 0%, #cbd5e0 50%, transparent 100%);
    margin: 30px 0;
    border: none;
}
</style>
"""))


def display_run_app_result(test_label: str, query: str, final_state: Dict[str, Any], 
                           test_type: str = "specific"):
    """Display results from running the app in a formatted way.
    
    Args:
        test_label: Label for the test (e.g., "TEST 1: AMBIGUOUS QUERY")
        query: The user query
        final_state: Final state from the app execution
        test_type: "ambiguous" or "specific" (default: "specific")
    """
    display_run_app_styles()
    
    # Determine badge styling
    badge_class = "badge-ambiguous" if test_type == "ambiguous" else "badge-specific"
    badge_text = "Requête Ambiguë" if test_type == "ambiguous" else "Requête Spécifique"
    
    # Build header
    display(HTML(f"""
<div class='run-app-container'>
    <div class='run-app-header'>
        <h2 class='run-app-title'>
            <span>🚀</span>
            <span>{test_label}</span>
        </h2>
        <div class='run-app-query-box'>
            <div class='run-app-query-label'>📝 Requête de l'utilisateur :</div>
            <div class='run-app-query-text'>"{query}"</div>
        </div>
    </div>
    <div class='run-app-body'>
        <span class='test-type-badge {badge_class}'>{badge_text}</span>
"""))
    
    # Check if clarification is needed
    if final_state.get('clarification_question'):
        clarification = final_state['clarification_question']
        display(HTML(f"""
        <div class='clarification-container'>
            <div class='clarification-header'>
                <span class='clarification-icon'>❓</span>
                <h3 class='clarification-title'>Clarification Nécessaire</h3>
            </div>
            <div class='clarification-content'>
                {clarification}
            </div>
        </div>
        <div class='run-summary'>
            <strong>⚠️ Processus Arrêté</strong><br>
            <div style='margin-top: 10px;'>
                Le <strong>Gatekeeper</strong> a détecté que la requête était trop ambiguë et a généré une question 
                de clarification pour l'utilisateur. Aucun outil n'a été exécuté, économisant ainsi des ressources 
                et garantissant que l'agent ne travaille que sur des requêtes bien définies.
            </div>
        </div>
        """))
    else:
        # Display execution stats
        num_steps = len(final_state.get('intermediate_steps', []))
        num_verifications = len(final_state.get('verification_history', []))
        
        display(HTML(f"""
        <div class='execution-stats'>
            <div class='stat-card'>
                <div class='stat-icon'>⚙️</div>
                <div class='stat-label'>Outils Exécutés</div>
                <div class='stat-value'>{num_steps}</div>
            </div>
            <div class='stat-card'>
                <div class='stat-icon'>🔍</div>
                <div class='stat-label'>Vérifications</div>
                <div class='stat-value'>{num_verifications}</div>
            </div>
            <div class='stat-card'>
                <div class='stat-icon'>✅</div>
                <div class='stat-label'>Statut</div>
                <div class='stat-value'>Succès</div>
            </div>
        </div>
        
        <div class='response-container'>
            <div class='response-header'>
                <span class='response-icon'>✨</span>
                <h3 class='response-title'>Réponse Finale Synthétisée</h3>
            </div>
            <div class='response-content'>
        """))
        
        # Render the final response as Markdown
        final_response = final_state.get('final_response', '*Aucune réponse générée.*')
        display(Markdown(final_response))
        
        display(HTML("""
            </div>
        </div>
        """))
        
        # Display summary
        tools_used = []
        for step in final_state.get('intermediate_steps', []):
            tool_name = step.get('tool_name', 'Unknown')
            if tool_name not in tools_used:
                tools_used.append(tool_name)
        
        tools_list = ', '.join([f"<code>{tool}</code>" for tool in tools_used])
        
        display(HTML(f"""
        <div class='run-summary'>
            <strong>🎯 Exécution Complète Réussie !</strong><br>
            <div style='margin-top: 12px;'>
                <strong>Workflow complet :</strong>
                <ol style='margin: 10px 0 10px 20px;'>
                    <li><strong>Gatekeeper</strong> a validé la requête comme étant spécifique</li>
                    <li><strong>Planner</strong> a généré un plan d'action intelligent</li>
                    <li><strong>Executor</strong> a exécuté {num_steps} outil(s) : {tools_list}</li>
                    <li><strong>Auditor</strong> a vérifié la qualité de chaque sortie</li>
                    <li><strong>Router</strong> a guidé le flux d'exécution</li>
                    <li><strong>Strategist</strong> a synthétisé les résultats avec inférence causale</li>
                </ol>
                <div style='margin-top: 12px; padding-top: 12px; border-top: 1px dashed #a78bfa;'>
                    💡 <strong>Note :</strong> La réponse finale ne se contente pas de compiler les données, 
                    elle génère des insights en connectant les informations de différentes sources, 
                    démontrant un véritable raisonnement analytique.
                </div>
            </div>
        </div>
        """))
    
    display(HTML("</div></div>"))
    display(HTML("<hr class='separator'>"))

