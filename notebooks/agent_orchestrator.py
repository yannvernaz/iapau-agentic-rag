"""
Agent Orchestrator Module
Implements the LangGraph-based agent orchestration from Phase 3
"""

import os
import json
from typing import Dict, Any, List, Optional, TypedDict
from langchain_openai import ChatOpenAI
from pydantic import BaseModel, Field
from langgraph.graph import StateGraph, END

from config import Config
from specialist_tools_gui import (
    librarian_rag_tool,
    analyst_sql_tool,
    analyst_trend_tool,
    tools,
    tool_map
)


class AgentState(TypedDict):
    """Defines the state of our agent graph."""
    original_request: str
    clarification_question: Optional[str]
    plan: List[str]
    intermediate_steps: List[Dict[str, Any]]
    verification_history: List[Dict[str, Any]]
    final_response: str


class VerificationResult(BaseModel):
    """Structured output for the Auditor node."""
    confidence_score: int = Field(description="Score from 1-5 on confidence in the tool's output.")
    is_consistent: bool = Field(description="Is the output internally consistent?")
    is_relevant: bool = Field(description="Is the output relevant to the original user request?")
    reasoning: str = Field(description="Brief reasoning for the scores.")


class FinancialAgentOrchestrator:
    """
    Main orchestrator for the financial analysis agent system.
    Implements the LangGraph workflow from Phase 3.
    """
    
    def __init__(self):
        """Initialize the orchestrator with all nodes and compile the graph."""
        # Initialize LLMs
        self.ambiguity_llm = ChatOpenAI(
            base_url=Config.LLM_BASE_URL,
            model=Config.LLM_MODEL_GATEKEEPER,
            api_key=Config.LLM_API_KEY,
            temperature=0.
        )
        
        self.supervisor_llm = ChatOpenAI(
            base_url=Config.LLM_BASE_URL,
            model=Config.LLM_MODEL_SUPERVISIOR,
            api_key=Config.LLM_API_KEY,
            temperature=0.
        )
        
        self.auditor_llm = ChatOpenAI(
            base_url=Config.LLM_BASE_URL,
            model=Config.LLM_MODEL_AUDITOR,
            api_key=Config.LLM_API_KEY,
            temperature=0.
        ).with_structured_output(VerificationResult)
        
        self.synthesizer_llm = ChatOpenAI(
            base_url=Config.LLM_BASE_URL,
            model=Config.LLM_MODEL_SYNTHETISER,
            api_key=Config.LLM_API_KEY,
            temperature=0.2
        )
        
        # Build the graph
        self.app = self._build_graph()
        
        print("✓ Agent orchestrator initialized successfully!")
    
    def _ambiguity_check_node(self, state: AgentState) -> Dict[str, Any]:
        """Checks if the user's request is ambiguous and requires clarification."""
        print("\n-- Gatekeeper (Ambiguity Check) Node --")
        request = state['original_request']
        
        prompt = f"""You are an expert at identifying ambiguity. Given the user's request, is it specific enough to be answered with high precision using financial company data?
        - A specific request asks for a number, a date, a named risk, or a comparison, a person etc. relative to the company (e.g., 'What was revenue in Q4 2023?').
        - An ambiguous request is open-ended (e.g., 'How is Nvidia doing?', 'What's the outlook?').

        If the request is ambiguous, formulate a single, polite question to the user that would provide the necessary clarification. Otherwise, respond with just 'OK'.

        User Request: "{request}"\nResponse:"""
        
        response = self.ambiguity_llm.invoke(prompt).content
        
        if response.strip() == "OK":
            print("  - Request is specific. Proceeding to planner.")
            return {"clarification_question": None}
        else:
            print(f"  - Request is ambiguous. Generating clarification question.")
            return {"clarification_question": response}
    
    def _create_planner_prompt(self):
        """Create the prompt template for the planner."""
        tool_descriptions = "\n".join([f"- {tool.name}: {tool.description.strip()}" for tool in tools])
        return f"""You are a master financial analyst agent, the Supervisor. Your task is to create a step-by-step plan to answer the user's request by intelligently selecting from the available tools.

**Available Tools:**
{tool_descriptions}

**Instructions:**
1. Analyze the user's request.
2. Create a clear, step-by-step plan. Each step must be a call to one of the available tools.
3. The final step in your plan should ALWAYS be 'FINISH'.

**Output Format:**
Return ONLY a valid JSON array of strings. Each string should be a tool call.
For tool calls, use this exact format: tool_name('query text here')
Do NOT include any explanation, markdown formatting, or extra text.

Example output:
["analyst_trend_tool('analyze revenue')", "FINISH"]

Another example:
["librarian_rag_tool('AI risks')", "analyst_sql_tool('Q4 2023 revenue')", "FINISH"]

---
User Request: {{request}}

Plan (JSON array only):"""
    
    def _planner_node(self, state: AgentState) -> Dict[str, Any]:
        """Creates a step-by-step plan to answer the user's request."""
        print("\n-- Planner Node --")
        request = state['original_request']
        planner_prompt_template = self._create_planner_prompt()
        prompt = planner_prompt_template.format(request=request)
        plan_str = self.supervisor_llm.invoke(prompt).content
        
        print(f"  - Raw plan response: {plan_str}")
        
        try:
            # Try to parse as JSON first (more robust)
            import json
            import ast
            
            # Clean up the response - remove markdown code blocks if present
            cleaned_plan = plan_str.strip()
            if cleaned_plan.startswith('```'):
                # Remove markdown code block markers
                lines = cleaned_plan.split('\n')
                cleaned_plan = '\n'.join([line for line in lines if not line.strip().startswith('```')])
                cleaned_plan = cleaned_plan.strip()
            
            # Try JSON parsing first
            try:
                plan = json.loads(cleaned_plan)
            except json.JSONDecodeError:
                # Fall back to ast.literal_eval (safer than eval)
                plan = ast.literal_eval(cleaned_plan)
            
            # Validate that plan is a list
            if not isinstance(plan, list):
                raise ValueError(f"Plan must be a list, got {type(plan)}")
            
            print(f"  - Generated Plan: {plan}")
            return {"plan": plan}
        except Exception as e:
            print(f"Error parsing plan: {e}. Falling back to FINISH.")
            print(f"  - Failed plan string: {plan_str}")
            return {"plan": ["FINISH"]}
    
    def _tool_executor_node(self, state: AgentState) -> Dict[str, Any]:
        """Executes the next step in the plan."""
        print("\n-- Tool Executor Node --")
        next_step = state['plan'][0]
        
        try:
            # Parse the tool call
            if '(' not in next_step or ')' not in next_step:
                raise ValueError(f"Invalid tool call format: {next_step}")
            
            tool_name = next_step.split('(')[0].strip()
            tool_input_str = next_step[len(tool_name)+1:-1].strip()
            
            # Handle quoted strings properly
            import ast
            try:
                tool_input = ast.literal_eval(tool_input_str)
            except (ValueError, SyntaxError):
                # If literal_eval fails, treat it as a plain string
                tool_input = tool_input_str.strip('\'"')
            
        except Exception as e:
            print(f"  - Error parsing tool call '{next_step}': {e}. Skipping step.")
            return {"plan": state['plan'][1:], "intermediate_steps": state.get('intermediate_steps', [])}

        print(f"  - Executing tool: {tool_name} with input: '{tool_input}'")
        
        # Verify tool exists
        if tool_name not in tool_map:
            print(f"  - Error: Tool '{tool_name}' not found in tool_map. Available tools: {list(tool_map.keys())}")
            return {"plan": state['plan'][1:], "intermediate_steps": state.get('intermediate_steps', [])}
        
        tool_to_call = tool_map[tool_name]
        result = tool_to_call.invoke(tool_input)
        
        new_intermediate_step = {
            'tool_name': tool_name,
            'tool_input': tool_input,
            'tool_output': result
        }
        
        current_steps = state.get('intermediate_steps', [])
        return {
            "intermediate_steps": current_steps + [new_intermediate_step],
            "plan": state['plan'][1:]
        }
    
    def _verification_node(self, state: AgentState) -> Dict[str, Any]:
        """Audits the most recent tool output for quality and relevance."""
        print("\n-- Auditor (Self-Correction) Node --")
        request = state['original_request']
        last_step = state['intermediate_steps'][-1]
        
        prompt = f"""You are a meticulous fact-checker and auditor. Given the user's original request and the output from a tool, please audit the output.
        
        **User Request:** {request}
        **Tool:** {last_step['tool_name']}
        **Tool Output:** {json.dumps(last_step['tool_output'])}
        
        **Audit Checklist:**
        1.  **Relevance:** Is this output directly relevant to answering the user's request? (Score 1-5, where 5 is highly relevant).
        2.  **Consistency:** Is the data internally consistent? (e.g., no contradictory statements).
        
        Based on this, provide a confidence score and a brief reasoning.
        """
        
        audit_result = self.auditor_llm.invoke(prompt)
        print(f"  - Audit Confidence Score: {audit_result.confidence_score}/5")
        
        current_history = state.get('verification_history', [])
        return {"verification_history": current_history + [audit_result.model_dump()]}
    
    def _router_node(self, state: AgentState) -> str:
        """Decides the next step in the graph based on the current state."""
        print("\n-- Advanced Router Node --")

        # Check for clarification first, this is a terminal state
        if state.get("clarification_question"):
            print("  - Decision: Ambiguity detected. Halting to ask user.")
            return END

        # Check if we need to start the main workflow
        if not state.get("plan"):
            print("  - Decision: New request. Routing to planner.")
            return "planner"

        # Check the last verification result if it exists
        if state.get("verification_history"):
            last_verification = state["verification_history"][-1]
            if last_verification["confidence_score"] < 3:
                print("  - Decision: Verification failed. Returning to planner.")
                # Clear the plan to force replanning
                state['plan'] = [] 
                return "planner"

        # Check if the plan is complete
        if not state.get("plan") or state["plan"][0] == "FINISH":
            print("  - Decision: Plan is complete. Routing to synthesizer.")
            return "synthesize"
        else:
            print("  - Decision: Plan has more steps. Routing to tool executor.")
            return "execute_tool"
    
    def _synthesizer_node(self, state: AgentState) -> Dict[str, Any]:
        """Synthesizes the final response with causal inference."""
        print("\n-- Strategist (Synthesizer) Node --")
        request = state['original_request']
        context = "\n\n".join([f"## Tool: {step['tool_name']}\nInput: {step['tool_input']}\nOutput: {json.dumps(step['tool_output'], indent=2)}" for step in state['intermediate_steps']])

        prompt = f"""You are an expert financial analyst acting as a strategist. Your task is to synthesize a comprehensive answer to the user's request based on the context provided by your specialist agents, generating novel insights where possible.

**User Request:**
{request}

**Context from Agents:**
---
{context}
---

**Instructions:**
1.  Carefully review the context from the tool outputs.
2.  Construct a clear, well-written, and accurate answer to the user's original request.
3.  **Connect the Dots (Causal Inference):** After summarizing the findings, analyze the combined information. Is there a plausible causal link or correlation between different pieces of data (e.g., a risk mentioned by the Librarian and a financial trend from the Analyst)?
4.  **Frame as Hypothesis:** Clearly state this connection as a data-grounded hypothesis, using phrases like 'The data suggests a possible link...' or 'One potential hypothesis is...'. This is your key value-add.

Final Answer:
"""
        
        final_answer = self.synthesizer_llm.invoke(prompt).content
        print("  - Generated final answer with causal inference.")
        return {"final_response": final_answer}
    
    def _build_graph(self) -> StateGraph:
        """Build and compile the LangGraph workflow."""
        graph_builder = StateGraph(AgentState)

        # Add nodes
        graph_builder.add_node("ambiguity_check", self._ambiguity_check_node)
        graph_builder.add_node("planner", self._planner_node)
        graph_builder.add_node("execute_tool", self._tool_executor_node)
        graph_builder.add_node("verify", self._verification_node)
        graph_builder.add_node("synthesize", self._synthesizer_node)

        # Define the entry point
        graph_builder.set_entry_point("ambiguity_check")

        # Define the conditional edge from the ambiguity checker
        graph_builder.add_conditional_edges(
            "ambiguity_check",
            lambda state: "planner" if state.get("clarification_question") is None else END,
            {"planner": "planner", END: END}
        )

        # After planning, always execute a tool
        graph_builder.add_edge("planner", "execute_tool")

        # After execution, always verify
        graph_builder.add_edge("execute_tool", "verify")

        # The ADVANCED ROUTER connects the verification step to the next logical node
        graph_builder.add_conditional_edges(
            "verify",
            self._router_node,
            {
                "planner": "planner",
                "execute_tool": "execute_tool",
                "synthesize": "synthesize",
            }
        )

        # The synthesizer is a terminal node
        graph_builder.add_edge("synthesize", END)

        # Compile the graph
        app = graph_builder.compile()
        
        print("✓ Graph compiled successfully!")
        return app
    
    def run(self, query: str, show_intermediate: bool = True, max_iterations: int = 5) -> Dict[str, Any]:
        """
        Run the agent orchestrator on a query.
        
        Args:
            query: The user's question
            show_intermediate: Whether to include intermediate steps in output
            max_iterations: Maximum number of iterations (safety limit)
            
        Returns:
            Dictionary containing the result and metadata
        """
        print("\n" + "="*80)
        print("🚀 RUNNING AGENT ORCHESTRATOR")
        print("="*80)
        print(f"📝 Query: {query}")
        print("="*80 + "\n")
        
        # Ensure initial state has empty lists for accumulation
        inputs = {
            "original_request": query,
            "verification_history": [],
            "intermediate_steps": []
        }
        final_state = {}
        
        # Stream and capture the last state
        iteration = 0
        for output in self.app.stream(inputs, stream_mode="values"):
            final_state.update(output)
            iteration += 1
            if iteration > max_iterations:
                print(f"⚠️ Max iterations ({max_iterations}) reached. Stopping.")
                break
        
        print("\n" + "="*80)
        if final_state.get('clarification_question'):
            print("❓ CLARIFICATION NEEDED")
        else:
            print("✅ COMPLETED")
        print("="*80 + "\n")
        
        return final_state
    
    def test_vector_search(self, query: str, top_k: int = 5) -> List[Dict[str, Any]]:
        """
        Test the vector search functionality directly.
        
        Args:
            query: Search query
            top_k: Number of results to return
            
        Returns:
            List of search results
        """
        return librarian_rag_tool.invoke(query)[:top_k]
