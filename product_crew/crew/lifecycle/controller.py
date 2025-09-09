"""Product lifecycle controller - orchestrates the 7-phase product refinement lifecycle."""

import time
from typing import Dict, Any, List
from pathlib import Path
from crewai import Crew

from .context import LifecycleContext, PhaseStatus
from .delegation import DelegationDecisionEngine
from .evaluation import SolutionEvaluator
from .validation import PhaseValidator, PhaseTransitionManager, ValidationResult
from .phases import (
    create_problem_understanding_task,
    create_problem_definition_task,
    create_solution_ideation_task,
    create_solution_validation_task,
    create_solution_refinement_task,
    create_solution_selection_task,
    create_implementation_planning_task
)


class ProductLifecycleController:
    """Controls execution of the 7-phase product refinement lifecycle."""
    
    def __init__(self, context: LifecycleContext, demo: bool = False):
        self.context = context
        self.demo = demo
        self.transition_manager = PhaseTransitionManager(context)
        self.agents = self._create_agent_pool()
        self.results = {}
        
    def _create_agent_pool(self) -> Dict[str, Any]:
        """Create pool of all available agents."""
        from ..agents import (
            create_product_manager_agent,
            create_market_analyst_agent,
            create_engineering_manager_agent,
            create_product_designer_agent,
            create_functional_analyst_agent,
            create_scrum_master_agent
        )
        
        return {
            "product_manager": create_product_manager_agent(self.context.model),
            "market_analyst": create_market_analyst_agent(self.context.model),
            "engineering_manager": create_engineering_manager_agent(self.context.model),
            "product_designer": create_product_designer_agent(self.context.model),
            "functional_analyst": create_functional_analyst_agent(self.context.model),
            "scrum_master": create_scrum_master_agent(self.context.model)
        }
    
    def execute_lifecycle(self) -> str:
        """Execute complete 7-phase lifecycle."""
        
        if self.demo:
            self._display_lifecycle_start()
        
        # Execute each phase sequentially
        for phase_num in range(1, 8):
            try:
                if self.demo:
                    self._display_phase_start(phase_num)
                
                # Execute the specific phase
                self.context.current_phase = phase_num
                self.context.phase_status[phase_num] = PhaseStatus.IN_PROGRESS
                
                phase_result = self._execute_phase(phase_num)
                
                # Store results and update context
                self.context.set_phase_result(phase_num, "raw_output", phase_result)
                self.results[phase_num] = phase_result
                
                # Update context based on phase results
                self._update_context_from_phase(phase_num, phase_result)
                
                # Validate phase completion
                validation_result, message = PhaseValidator().validate_phase_1(self.context) if phase_num == 1 else \
                                           getattr(PhaseValidator(), f"validate_phase_{phase_num}")(self.context) if hasattr(PhaseValidator(), f"validate_phase_{phase_num}") else \
                                           (ValidationResult.PASSED, "No validation available")
                
                if validation_result == ValidationResult.FAILED:
                    self.context.phase_status[phase_num] = PhaseStatus.FAILED
                    if self.demo:
                        self._display_phase_error(phase_num, f"Validation failed: {message}")
                    break
                else:
                    self.context.phase_status[phase_num] = PhaseStatus.COMPLETED
                    if self.demo:
                        self._display_phase_completion(phase_num, validation_result == ValidationResult.WARNINGS)
                
                # Transition to next phase
                if phase_num < 7:
                    success, transition_message = self.transition_manager.execute_phase_transition(phase_num + 1)
                    if not success and self.demo:
                        self._display_phase_error(phase_num, f"Transition failed: {transition_message}")
                
            except Exception as e:
                self.context.phase_status[phase_num] = PhaseStatus.FAILED
                if self.demo:
                    self._display_phase_error(phase_num, str(e))
                break
        
        # Generate final PID
        final_pid = self._generate_final_pid()
        
        if self.demo:
            self._display_lifecycle_completion()
        
        return final_pid
    
    def _execute_phase(self, phase_num: int) -> str:
        """Execute a specific phase with appropriate task creation and delegation."""
        
        # Create phase-specific task
        task = self._create_phase_task(phase_num)
        
        # Get required agents for this phase
        required_agents = self._get_phase_agents(phase_num)
        
        # Create and run crew for this phase
        phase_crew = Crew(
            agents=required_agents,
            tasks=[task],
            verbose=self.demo
        )
        
        # Execute the crew
        phase_start = time.time()
        result = phase_crew.kickoff()
        phase_time = time.time() - phase_start
        
        if self.demo:
            print(f"Phase {phase_num} completed in {phase_time:.1f}s")
        
        return str(result)
    
    def _create_phase_task(self, phase_num: int):
        """Create the appropriate task for the given phase."""
        
        task_creators = {
            1: create_problem_understanding_task,
            2: create_problem_definition_task,
            3: create_solution_ideation_task,
            4: create_solution_validation_task,
            5: create_solution_refinement_task,
            6: create_solution_selection_task,
            7: create_implementation_planning_task
        }
        
        creator = task_creators.get(phase_num)
        if not creator:
            raise ValueError(f"No task creator found for phase {phase_num}")
        
        return creator(self.context)
    
    def _get_phase_agents(self, phase_num: int) -> List[Any]:
        """Get the required agents for a specific phase based on delegation logic."""
        
        # Product Manager is always the primary agent
        required_agents = [self.agents["product_manager"]]
        
        # Get delegation requirements for this phase
        delegations = DelegationDecisionEngine.get_required_delegations(self.context, phase_num)
        
        # Add required specialist agents
        agent_mapping = {
            "market_analyst": self.agents["market_analyst"],
            "engineering_manager": self.agents["engineering_manager"],
            "product_designer": self.agents["product_designer"],
            "functional_analyst": self.agents["functional_analyst"],
            "scrum_master": self.agents["scrum_master"]
        }
        
        for agent_type, is_required in delegations.items():
            if is_required and agent_type in agent_mapping:
                required_agents.append(agent_mapping[agent_type])
        
        return required_agents
    
    def _update_context_from_phase(self, phase_num: int, phase_result: str) -> None:
        """Update lifecycle context based on phase results."""
        
        # This is a simplified version - in a full implementation, you would parse
        # the phase results more thoroughly to extract structured data
        
        result_lower = phase_result.lower()
        
        if phase_num == 1:
            # Update problem clarity score based on phase 1 results
            if "clarity score" in result_lower:
                # Try to extract clarity score from results
                import re
                match = re.search(r'clarity score.*?(\d+\.?\d*)', result_lower)
                if match:
                    self.context.problem_clarity_score = float(match.group(1)) / 10.0
            else:
                # Default scoring based on content quality
                if len(phase_result) > 500:
                    self.context.problem_clarity_score = 0.8
                elif len(phase_result) > 300:
                    self.context.problem_clarity_score = 0.6
                else:
                    self.context.problem_clarity_score = 0.4
        
        elif phase_num == 2:
            # Extract problem statement and domain from results
            if "problem statement" in result_lower:
                lines = phase_result.split('\n')
                for line in lines:
                    if "problem statement" in line.lower() and ":" in line:
                        self.context.problem_statement = line.split(':', 1)[1].strip()
                        break
            
            if "problem domain" in result_lower:
                lines = phase_result.split('\n')
                for line in lines:
                    if "domain" in line.lower() and ":" in line:
                        self.context.problem_domain = line.split(':', 1)[1].strip()
                        break
            
            # Update clarity score after definition
            self.context.problem_clarity_score = min(self.context.problem_clarity_score + 0.3, 1.0)
        
        elif phase_num == 3:
            # Parse solutions from ideation results
            # This is simplified - in practice you'd have more structured parsing
            if "solution" in result_lower and not self.context.solutions:
                # Create mock solutions based on result content
                solution_count = result_lower.count("solution")
                for i in range(min(solution_count, 5)):  # Cap at 5 solutions
                    self.context.solutions.append({
                        "id": f"solution_{i+1}",
                        "description": f"Solution {i+1} extracted from ideation results",
                        "complexity": "medium"
                    })
        
        elif phase_num == 4:
            # Parse evaluation results
            if "evaluation" in result_lower and not self.context.solution_evaluations:
                # Create mock evaluations based on solution count
                evaluator = SolutionEvaluator(self.context)
                self.context.solution_evaluations = evaluator.evaluate_solutions()
        
        elif phase_num == 6:
            # Extract selected solution
            if "selected solution" in result_lower and not self.context.selected_solution:
                # Mock solution selection
                if self.context.solution_evaluations:
                    best_solution_id = max(
                        self.context.solution_evaluations.keys(),
                        key=lambda k: getattr(self.context.solution_evaluations[k], "composite_score", 0)
                        if hasattr(self.context.solution_evaluations[k], "composite_score")
                        else self.context.solution_evaluations[k].get("composite_score", 0)
                    )
                    self.context.selected_solution = {
                        "solution_id": best_solution_id,
                        "rationale": "Selected based on highest composite evaluation score",
                        "selection_date": time.strftime("%Y-%m-%d")
                    }
        
        elif phase_num == 7:
            # Extract implementation plan
            if "implementation" in result_lower and not self.context.implementation_plan:
                self.context.implementation_plan = {
                    "tasks": "Implementation tasks extracted from phase 7 results",
                    "timeline": "Timeline extracted from phase 7 results",
                    "resources": "Resource requirements extracted from phase 7 results",
                    "risks": "Risk assessment extracted from phase 7 results"
                }
    
    def _generate_final_pid(self) -> str:
        """Generate final comprehensive PID from all phase results."""
        
        pid_sections = []
        
        # Header
        pid_sections.append("# Product Initiative Document")
        pid_sections.append(f"*Generated through 7-phase product refinement lifecycle*\n")
        pid_sections.append(f"**Generation Date**: {time.strftime('%Y-%m-%d %H:%M:%S')}\n")
        
        # Executive Summary
        pid_sections.append("## Executive Summary")
        if self.context.selected_solution:
            pid_sections.append(f"**Selected Solution**: {self.context.selected_solution.get('solution_id', 'Not specified')}")
            pid_sections.append(f"**Selection Rationale**: {self.context.selected_solution.get('rationale', 'Not specified')}")
        pid_sections.append(f"**Lifecycle Completion**: {self.transition_manager.get_completion_status()['completion_percentage']:.0f}%\n")
        
        # Problem Space (Phases 1-2)
        pid_sections.append("## Problem Space")
        pid_sections.append("### Problem Understanding")
        if 1 in self.results:
            pid_sections.append(self.results[1])
        
        pid_sections.append("\n### Problem Definition")
        if 2 in self.results:
            pid_sections.append(self.results[2])
        
        if self.context.problem_statement:
            pid_sections.append(f"\n**Defined Problem Statement**: {self.context.problem_statement}")
        if self.context.problem_domain:
            pid_sections.append(f"**Problem Domain**: {self.context.problem_domain}")
        
        # Solution Space (Phases 3-6)
        pid_sections.append("\n## Solution Space")
        pid_sections.append("### Solution Ideation")
        if 3 in self.results:
            pid_sections.append(self.results[3])
        
        pid_sections.append("\n### Solution Validation")
        if 4 in self.results:
            pid_sections.append(self.results[4])
        
        pid_sections.append("\n### Solution Refinement")
        if 5 in self.results:
            pid_sections.append(self.results[5])
        
        pid_sections.append("\n### Solution Selection")
        if 6 in self.results:
            pid_sections.append(self.results[6])
        
        # Implementation Planning (Phase 7)
        pid_sections.append("\n## Implementation Planning")
        if 7 in self.results:
            pid_sections.append(self.results[7])
        
        # Lifecycle Summary
        pid_sections.append("\n## Lifecycle Summary")
        completion_status = self.transition_manager.get_completion_status()
        pid_sections.append(f"**Completed Phases**: {len(completion_status['completed_phases'])}/7")
        pid_sections.append(f"**Current Phase**: {completion_status['current_phase']}")
        if completion_status['failed_phases']:
            pid_sections.append(f"**Failed Phases**: {completion_status['failed_phases']}")
        
        # Quality Metrics
        pid_sections.append("\n## Quality Metrics")
        pid_sections.append(f"**Problem Clarity Score**: {self.context.problem_clarity_score:.1f}/1.0")
        if self.context.solutions:
            pid_sections.append(f"**Solutions Generated**: {len(self.context.solutions)}")
        if self.context.solution_evaluations:
            pid_sections.append(f"**Solutions Evaluated**: {len(self.context.solution_evaluations)}")
        
        return "\n".join(pid_sections)
    
    def _display_lifecycle_start(self) -> None:
        """Display lifecycle start information in demo mode."""
        print("=" * 80)
        print("🚀 PRODUCT REFINEMENT LIFECYCLE EXECUTION")
        print("=" * 80)
        print(f"Requirements Path: {self.context.requirements_path}")
        print(f"PID Path: {self.context.pid_path}")
        print(f"Model: {self.context.model}")
        print(f"Phases: 7-phase structured approach")
        print("-" * 80)
    
    def _display_phase_start(self, phase_num: int) -> None:
        """Display phase start information in demo mode."""
        phase_names = {
            1: "Problem Understanding",
            2: "Problem Definition", 
            3: "Solution Ideation",
            4: "Solution Validation",
            5: "Solution Refinement",
            6: "Solution Selection",
            7: "Implementation Planning"
        }
        
        print(f"\n🔄 PHASE {phase_num}: {phase_names.get(phase_num, 'Unknown')}")
        print("-" * 60)
        
        # Show delegation information
        delegations = DelegationDecisionEngine.get_required_delegations(self.context, phase_num)
        active_delegations = [agent for agent, required in delegations.items() if required]
        
        if active_delegations:
            print(f"Delegating to: {', '.join(active_delegations)}")
        else:
            print("No delegations required - Product Manager only")
    
    def _display_phase_completion(self, phase_num: int, has_warnings: bool = False) -> None:
        """Display phase completion information in demo mode."""
        status = "⚠️ COMPLETED WITH WARNINGS" if has_warnings else "✅ COMPLETED"
        print(f"{status} - Phase {phase_num}")
    
    def _display_phase_error(self, phase_num: int, error_message: str) -> None:
        """Display phase error information in demo mode."""
        print(f"❌ FAILED - Phase {phase_num}: {error_message}")
    
    def _display_lifecycle_completion(self) -> None:
        """Display lifecycle completion information in demo mode."""
        completion_status = self.transition_manager.get_completion_status()
        
        print("\n" + "=" * 80)
        print("🏁 PRODUCT REFINEMENT LIFECYCLE COMPLETE")
        print("=" * 80)
        print(f"Completion Status: {completion_status['completion_percentage']:.0f}%")
        print(f"Completed Phases: {len(completion_status['completed_phases'])}/7")
        
        if completion_status['failed_phases']:
            print(f"Failed Phases: {completion_status['failed_phases']}")
        
        if self.context.selected_solution:
            print(f"Selected Solution: {self.context.selected_solution.get('solution_id', 'Unknown')}")
        
        print("=" * 80)