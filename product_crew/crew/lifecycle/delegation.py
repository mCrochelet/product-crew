"""Conditional delegation decision engine."""

from typing import Dict, Any
from .context import LifecycleContext


class DelegationDecisionEngine:
    """Determines when and how to delegate to specific agents."""
    
    @staticmethod
    def should_delegate_market_research(context: LifecycleContext, phase: int) -> bool:
        """Determine if Market Analyst delegation is needed."""
        
        if phase == 1:  # Understand Problem
            # Check data completeness
            data_completeness = DelegationDecisionEngine._assess_data_completeness(context)
            return data_completeness < 0.7  # Threshold for sufficient data
            
        elif phase == 2:  # Define Problem  
            # Check problem statement clarity
            return context.problem_clarity_score < 0.8
            
        elif phase == 4:  # Validate Solutions - Value Assessment
            # Only if we need market validation
            return len(context.solutions) > 1  # Multiple solutions need market input
            
        return False
    
    @staticmethod
    def should_delegate_functional_analysis(context: LifecycleContext, phase: int) -> bool:
        """Determine if Functional Analyst delegation is needed."""
        
        if phase == 2:  # Define Problem
            # Check if problem domain needs clarification
            return not context.problem_domain or len(context.problem_domain) < 50
            
        elif phase == 5:  # Refine Solutions
            # Always needed for requirements refinement
            return True
            
        elif phase == 7:  # Plan Implementation
            # Always needed for implementation breakdown
            return True
            
        return False
    
    @staticmethod
    def should_delegate_engineering_management(context: LifecycleContext, phase: int) -> bool:
        """Determine if Engineering Manager delegation is needed."""
        
        if phase == 4:  # Validate Solutions - Feasibility Assessment
            return True  # Always needed for feasibility assessment
            
        elif phase == 5:  # Refine Solutions  
            return True  # Always needed for technical refinement
            
        elif phase == 7:  # Plan Implementation
            return True  # Always needed for technical planning
            
        return False
    
    @staticmethod
    def should_delegate_product_design(context: LifecycleContext, phase: int) -> bool:
        """Determine if Product Designer delegation is needed."""
        
        if phase == 4:  # Validate Solutions - Usability Assessment
            return True  # Always needed for usability assessment
            
        elif phase == 5:  # Refine Solutions
            return True  # Always needed for UX refinement
            
        return False
    
    @staticmethod
    def should_delegate_scrum_master(context: LifecycleContext, phase: int) -> bool:
        """Determine if Scrum Master delegation is needed."""
        
        if phase == 7:  # Plan Implementation
            return True  # Always needed for delivery planning
            
        return False
    
    @staticmethod
    def get_required_delegations(context: LifecycleContext, phase: int) -> Dict[str, bool]:
        """Get all required delegations for a phase."""
        
        return {
            "market_analyst": DelegationDecisionEngine.should_delegate_market_research(context, phase),
            "functional_analyst": DelegationDecisionEngine.should_delegate_functional_analysis(context, phase),
            "engineering_manager": DelegationDecisionEngine.should_delegate_engineering_management(context, phase),
            "product_designer": DelegationDecisionEngine.should_delegate_product_design(context, phase),
            "scrum_master": DelegationDecisionEngine.should_delegate_scrum_master(context, phase)
        }
    
    @staticmethod
    def _assess_data_completeness(context: LifecycleContext) -> float:
        """Assess completeness of available data (0.0 to 1.0)."""
        
        score = 0.0
        checks = 0
        
        # Check original PID content quality
        if context.original_pid_content:
            content_length = len(context.original_pid_content.strip())
            if content_length > 200:
                score += 0.3
            elif content_length > 100:
                score += 0.2
            elif content_length > 50:
                score += 0.1
        checks += 1
        
        # Check for problem statement
        if "problem" in context.original_pid_content.lower():
            score += 0.3
        checks += 1
        
        # Check for solution hints
        if "solution" in context.original_pid_content.lower():
            score += 0.2
        checks += 1
        
        # Check for user/customer mentions
        if any(term in context.original_pid_content.lower() for term in ["user", "customer", "client"]):
            score += 0.2
        checks += 1
        
        return score / checks if checks > 0 else 0.0