"""Phase validation and transition management for the product refinement lifecycle."""

from typing import Dict, Any, Tuple, List
from enum import Enum
from .context import LifecycleContext, PhaseStatus


class ValidationResult(Enum):
    """Results of phase validation."""
    PASSED = "passed"
    FAILED = "failed"
    WARNINGS = "warnings"


class PhaseValidator:
    """Validates phase completion and determines transition readiness."""
    
    @staticmethod
    def validate_phase_1(context: LifecycleContext) -> Tuple[ValidationResult, str]:
        """Validate Problem Understanding phase completion."""
        
        issues = []
        warnings = []
        
        # Check if phase 1 results exist
        phase_1_data = context.get_phase_result(1)
        if not phase_1_data:
            issues.append("Phase 1 results are missing")
            return ValidationResult.FAILED, "; ".join(issues)
        
        # Check problem clarity score
        if context.problem_clarity_score <= 0.3:
            issues.append("Problem clarity score too low (≤0.3)")
        elif context.problem_clarity_score <= 0.5:
            warnings.append("Problem clarity score is moderate (≤0.5)")
        
        # Check if research decision was made
        if context.research_needed is None:
            issues.append("No decision made about additional research needs")
        
        # Check analysis content length
        analysis_content = phase_1_data.get("analysis", "")
        if len(analysis_content) < 100:
            issues.append("Problem analysis is too brief (<100 characters)")
        elif len(analysis_content) < 200:
            warnings.append("Problem analysis could be more detailed (<200 characters)")
        
        # Determine result
        if issues:
            return ValidationResult.FAILED, f"Issues: {'; '.join(issues)}"
        elif warnings:
            return ValidationResult.WARNINGS, f"Warnings: {'; '.join(warnings)}"
        else:
            return ValidationResult.PASSED, "Phase 1 validation passed"
    
    @staticmethod  
    def validate_phase_2(context: LifecycleContext) -> Tuple[ValidationResult, str]:
        """Validate Problem Definition phase completion."""
        
        issues = []
        warnings = []
        
        # Check problem statement exists and has content
        if not context.problem_statement:
            issues.append("Problem statement is missing")
        elif len(context.problem_statement) < 50:
            issues.append("Problem statement is too brief (<50 characters)")
        elif len(context.problem_statement) < 100:
            warnings.append("Problem statement could be more detailed (<100 characters)")
        
        # Check problem domain definition
        if not context.problem_domain:
            issues.append("Problem domain definition is missing")
        elif len(context.problem_domain) < 50:
            issues.append("Problem domain definition is too brief (<50 characters)")
        
        # Check updated problem clarity score
        if context.problem_clarity_score <= 0.5:
            issues.append("Problem clarity score still too low after definition phase (≤0.5)")
        elif context.problem_clarity_score <= 0.7:
            warnings.append("Problem clarity score should be higher after definition (≤0.7)")
        
        # Check phase 2 results
        phase_2_data = context.get_phase_result(2)
        if not phase_2_data:
            issues.append("Phase 2 results are missing")
        
        # Determine result
        if issues:
            return ValidationResult.FAILED, f"Issues: {'; '.join(issues)}"
        elif warnings:
            return ValidationResult.WARNINGS, f"Warnings: {'; '.join(warnings)}"
        else:
            return ValidationResult.PASSED, "Phase 2 validation passed"
    
    @staticmethod
    def validate_phase_3(context: LifecycleContext) -> Tuple[ValidationResult, str]:
        """Validate Solution Ideation phase completion."""
        
        issues = []
        warnings = []
        
        # Check minimum number of solutions
        if len(context.solutions) < 2:
            issues.append("Insufficient solutions generated (minimum 2 required)")
        elif len(context.solutions) < 3:
            warnings.append("Only 2 solutions generated; 3+ recommended for better options")
        
        # Check solution content quality
        insufficient_solutions = []
        for i, solution in enumerate(context.solutions):
            solution_id = f"Solution {i+1}"
            
            if "description" not in solution:
                issues.append(f"{solution_id} missing description")
                continue
                
            if len(solution["description"]) < 100:
                insufficient_solutions.append(solution_id)
        
        if insufficient_solutions:
            if len(insufficient_solutions) == len(context.solutions):
                issues.append("All solutions have insufficient descriptions (<100 characters)")
            else:
                warnings.append(f"Some solutions have brief descriptions: {', '.join(insufficient_solutions)}")
        
        # Check for solution diversity
        if len(context.solutions) >= 2:
            descriptions = [s.get("description", "").lower() for s in context.solutions]
            if len(set(descriptions)) < len(descriptions):
                warnings.append("Some solutions appear very similar")
        
        # Check phase 3 results
        phase_3_data = context.get_phase_result(3)
        if not phase_3_data:
            issues.append("Phase 3 results are missing")
        
        # Determine result
        if issues:
            return ValidationResult.FAILED, f"Issues: {'; '.join(issues)}"
        elif warnings:
            return ValidationResult.WARNINGS, f"Warnings: {'; '.join(warnings)}"
        else:
            return ValidationResult.PASSED, "Phase 3 validation passed"
    
    @staticmethod
    def validate_phase_4(context: LifecycleContext) -> Tuple[ValidationResult, str]:
        """Validate Solution Validation phase completion."""
        
        issues = []
        warnings = []
        
        # Check if evaluations exist
        if not context.solution_evaluations:
            issues.append("No solution evaluations found")
            return ValidationResult.FAILED, f"Issues: {'; '.join(issues)}"
        
        # Check evaluation completeness
        expected_evaluations = len(context.solutions)
        actual_evaluations = len(context.solution_evaluations)
        
        if actual_evaluations != expected_evaluations:
            issues.append(f"Evaluation count mismatch: {actual_evaluations} evaluations for {expected_evaluations} solutions")
        
        # Check evaluation quality
        low_scoring_solutions = []
        unscored_solutions = []
        
        for solution_id, evaluation in context.solution_evaluations.items():
            if isinstance(evaluation, dict):
                composite_score = evaluation.get("composite_score", 0)
            else:
                composite_score = getattr(evaluation, "composite_score", 0)
            
            if composite_score <= 0:
                unscored_solutions.append(solution_id)
            elif composite_score < 4.0:
                low_scoring_solutions.append(solution_id)
        
        if unscored_solutions:
            issues.append(f"Solutions without valid scores: {', '.join(unscored_solutions)}")
        
        if low_scoring_solutions:
            warnings.append(f"Low-scoring solutions (<4.0): {', '.join(low_scoring_solutions)}")
        
        # Check if at least one solution is viable (score >= 6.0)
        viable_solutions = []
        for solution_id, evaluation in context.solution_evaluations.items():
            if isinstance(evaluation, dict):
                composite_score = evaluation.get("composite_score", 0)
            else:
                composite_score = getattr(evaluation, "composite_score", 0)
            
            if composite_score >= 6.0:
                viable_solutions.append(solution_id)
        
        if not viable_solutions:
            issues.append("No solutions meet viability threshold (≥6.0)")
        elif len(viable_solutions) == 1:
            warnings.append("Only one viable solution identified; limited options for selection")
        
        # Check phase 4 results
        phase_4_data = context.get_phase_result(4)
        if not phase_4_data:
            issues.append("Phase 4 results are missing")
        
        # Determine result
        if issues:
            return ValidationResult.FAILED, f"Issues: {'; '.join(issues)}"
        elif warnings:
            return ValidationResult.WARNINGS, f"Warnings: {'; '.join(warnings)}"
        else:
            return ValidationResult.PASSED, "Phase 4 validation passed"
    
    @staticmethod
    def validate_phase_5(context: LifecycleContext) -> Tuple[ValidationResult, str]:
        """Validate Solution Refinement phase completion."""
        
        issues = []
        warnings = []
        
        # Check phase 5 results exist
        phase_5_data = context.get_phase_result(5)
        if not phase_5_data:
            issues.append("Phase 5 results are missing")
            return ValidationResult.FAILED, f"Issues: {'; '.join(issues)}"
        
        # Check if refinements were made
        refinement_content = phase_5_data.get("refinements", "")
        if not refinement_content or len(refinement_content) < 200:
            issues.append("Insufficient refinement documentation (<200 characters)")
        
        # Check if solutions were improved (this would require tracking before/after scores)
        # For now, we'll check if refinement results indicate improvements
        improvements_mentioned = False
        if isinstance(refinement_content, str):
            improvements_mentioned = any(word in refinement_content.lower() 
                                       for word in ["improve", "enhance", "better", "optimiz", "refin"])
        
        if not improvements_mentioned:
            warnings.append("No clear improvements mentioned in refinement results")
        
        # Check if top solutions were addressed
        if context.solution_evaluations:
            top_solutions = sorted(
                context.solution_evaluations.items(),
                key=lambda x: getattr(x[1], "composite_score", 0) if hasattr(x[1], "composite_score") 
                             else x[1].get("composite_score", 0),
                reverse=True
            )[:3]  # Top 3 solutions
            
            if len(top_solutions) > 1 and "solution" not in refinement_content.lower():
                warnings.append("Refinement results don't clearly reference specific solutions")
        
        # Determine result
        if issues:
            return ValidationResult.FAILED, f"Issues: {'; '.join(issues)}"
        elif warnings:
            return ValidationResult.WARNINGS, f"Warnings: {'; '.join(warnings)}"
        else:
            return ValidationResult.PASSED, "Phase 5 validation passed"
    
    @staticmethod
    def validate_phase_6(context: LifecycleContext) -> Tuple[ValidationResult, str]:
        """Validate Solution Selection phase completion."""
        
        issues = []
        warnings = []
        
        # Check if solution was selected
        if not context.selected_solution:
            issues.append("No solution has been selected")
            return ValidationResult.FAILED, f"Issues: {'; '.join(issues)}"
        
        # Check selection rationale
        if isinstance(context.selected_solution, dict):
            rationale = context.selected_solution.get("rationale", "")
            if not rationale:
                issues.append("No selection rationale provided")
            elif len(rationale) < 100:
                issues.append("Selection rationale is too brief (<100 characters)")
            elif len(rationale) < 200:
                warnings.append("Selection rationale could be more detailed (<200 characters)")
        
        # Check phase 6 results
        phase_6_data = context.get_phase_result(6)
        if not phase_6_data:
            issues.append("Phase 6 results are missing")
        
        # Check if selection is from evaluated solutions
        if context.solution_evaluations:
            selected_id = None
            if isinstance(context.selected_solution, dict):
                selected_id = context.selected_solution.get("solution_id")
            
            if selected_id and selected_id not in context.solution_evaluations:
                warnings.append("Selected solution ID doesn't match any evaluated solution")
        
        # Determine result
        if issues:
            return ValidationResult.FAILED, f"Issues: {'; '.join(issues)}"
        elif warnings:
            return ValidationResult.WARNINGS, f"Warnings: {'; '.join(warnings)}"
        else:
            return ValidationResult.PASSED, "Phase 6 validation passed"
    
    @staticmethod
    def validate_phase_7(context: LifecycleContext) -> Tuple[ValidationResult, str]:
        """Validate Implementation Planning phase completion."""
        
        issues = []
        warnings = []
        
        # Check if implementation plan exists
        if not context.implementation_plan:
            issues.append("Implementation plan is missing")
            return ValidationResult.FAILED, f"Issues: {'; '.join(issues)}"
        
        # Check required plan sections
        required_sections = ["tasks", "timeline", "resources", "risks"]
        missing_sections = []
        
        for section in required_sections:
            if section not in context.implementation_plan:
                missing_sections.append(section)
        
        if missing_sections:
            issues.append(f"Implementation plan missing required sections: {', '.join(missing_sections)}")
        
        # Check plan content quality
        plan = context.implementation_plan
        
        # Check tasks
        if "tasks" in plan:
            tasks = plan["tasks"]
            if isinstance(tasks, str) and len(tasks) < 200:
                warnings.append("Task breakdown appears insufficient (<200 characters)")
            elif isinstance(tasks, list) and len(tasks) < 3:
                warnings.append("Very few tasks identified (<3 tasks)")
        
        # Check timeline
        if "timeline" in plan:
            timeline = plan["timeline"]
            if isinstance(timeline, str) and len(timeline) < 100:
                warnings.append("Timeline information is very brief (<100 characters)")
        
        # Check resources
        if "resources" in plan:
            resources = plan["resources"]
            if isinstance(resources, str) and len(resources) < 100:
                warnings.append("Resource planning is very brief (<100 characters)")
        
        # Check phase 7 results
        phase_7_data = context.get_phase_result(7)
        if not phase_7_data:
            issues.append("Phase 7 results are missing")
        
        # Determine result
        if issues:
            return ValidationResult.FAILED, f"Issues: {'; '.join(issues)}"
        elif warnings:
            return ValidationResult.WARNINGS, f"Warnings: {'; '.join(warnings)}"
        else:
            return ValidationResult.PASSED, "Phase 7 validation passed"


class PhaseTransitionManager:
    """Manages transitions between lifecycle phases."""
    
    def __init__(self, context: LifecycleContext):
        self.context = context
        self.validator = PhaseValidator()
    
    def can_transition_to_phase(self, target_phase: int) -> Tuple[bool, str]:
        """Check if ready to transition to target phase."""
        
        current_phase = self.context.current_phase
        
        # Can't skip phases (must be sequential)
        if target_phase != current_phase + 1:
            return False, f"Cannot skip from phase {current_phase} to {target_phase}"
        
        # Can't go beyond phase 7
        if target_phase > 7:
            return False, f"Phase {target_phase} does not exist (maximum is 7)"
        
        # Validate current phase completion
        validation_method = getattr(self.validator, f"validate_phase_{current_phase}", None)
        if validation_method:
            result, message = validation_method(self.context)
            
            if result == ValidationResult.FAILED:
                return False, f"Phase {current_phase} validation failed: {message}"
            elif result == ValidationResult.WARNINGS:
                # Allow transition with warnings but log them
                return True, f"Phase {current_phase} validated with warnings: {message}"
        
        return True, f"Ready to transition from phase {current_phase} to {target_phase}"
    
    def execute_phase_transition(self, target_phase: int) -> Tuple[bool, str]:
        """Execute transition to target phase."""
        
        can_transition, message = self.can_transition_to_phase(target_phase)
        if not can_transition:
            return False, message
        
        # Update context for new phase
        previous_phase = self.context.current_phase
        self.context.phase_status[previous_phase] = PhaseStatus.COMPLETED
        self.context.current_phase = target_phase
        self.context.phase_status[target_phase] = PhaseStatus.IN_PROGRESS
        
        return True, f"Successfully transitioned from phase {previous_phase} to {target_phase}"
    
    def get_next_phase(self) -> int:
        """Get the next phase number."""
        return min(self.context.current_phase + 1, 7)
    
    def is_lifecycle_complete(self) -> bool:
        """Check if entire lifecycle is complete."""
        return (self.context.current_phase == 7 and 
                self.context.phase_status.get(7) == PhaseStatus.COMPLETED)
    
    def get_completion_status(self) -> Dict[str, Any]:
        """Get overall lifecycle completion status."""
        completed_phases = [
            phase for phase, status in self.context.phase_status.items()
            if status == PhaseStatus.COMPLETED
        ]
        
        failed_phases = [
            phase for phase, status in self.context.phase_status.items()
            if status == PhaseStatus.FAILED
        ]
        
        return {
            "current_phase": self.context.current_phase,
            "completed_phases": completed_phases,
            "failed_phases": failed_phases,
            "completion_percentage": len(completed_phases) / 7 * 100,
            "is_complete": self.is_lifecycle_complete(),
            "next_phase": self.get_next_phase() if not self.is_lifecycle_complete() else None
        }
    
    def validate_all_phases(self) -> Dict[int, Tuple[ValidationResult, str]]:
        """Validate all completed phases."""
        results = {}
        
        for phase in range(1, 8):
            if self.context.phase_status.get(phase) == PhaseStatus.COMPLETED:
                validation_method = getattr(self.validator, f"validate_phase_{phase}", None)
                if validation_method:
                    results[phase] = validation_method(self.context)
                else:
                    results[phase] = (ValidationResult.PASSED, "No validation method available")
        
        return results
    
    def get_blocking_issues(self) -> List[str]:
        """Get list of issues blocking lifecycle progression."""
        issues = []
        
        current_phase = self.context.current_phase
        
        # Check current phase validation
        validation_method = getattr(self.validator, f"validate_phase_{current_phase}", None)
        if validation_method:
            result, message = validation_method(self.context)
            if result == ValidationResult.FAILED:
                issues.append(f"Phase {current_phase} validation failed: {message}")
        
        # Check for any failed phases
        for phase, status in self.context.phase_status.items():
            if status == PhaseStatus.FAILED:
                issues.append(f"Phase {phase} has failed status")
        
        return issues