"""Crew execution and orchestration."""

import sys
from pathlib import Path
from typing import Dict, Any, List
import time

import click
from crewai import Crew

from ..file_operations import load_environment, get_output_file_path, create_pid_file
from ..demo import demo_pause, demo_display_agent_info, demo_display_task_info, demo_section_separator
from .tasks import (
    create_lifecycle_workflow_task,
    create_delegation_workflow_task,
    create_delegation_crew_agents,
    create_discovery_phase_tasks,  # Legacy compatibility
    create_solution_design_phase_tasks,  # Legacy compatibility
    create_breakdown_phase_tasks,  # Legacy compatibility
    create_integration_task,  # Legacy compatibility
    create_print_paths_task  # Legacy compatibility
)
from .lifecycle import LifecycleContext, ProductLifecycleController
from .agents import create_path_printer_agent  # Legacy compatibility


def calculate_quality_score(results: List[str]) -> float:
    """Calculate quality score based on output completeness and coherence."""
    if not results:
        return 0.0
    
    score = 0.0
    total_checks = 0
    
    for result in results:
        if not result or len(result.strip()) < 100:  # Too short
            score += 0.0
        elif len(result.strip()) < 500:  # Basic content
            score += 0.3
        elif len(result.strip()) < 1000:  # Good content
            score += 0.7
        else:  # Comprehensive content
            score += 1.0
        total_checks += 1
    
    return (score / total_checks) * 10 if total_checks > 0 else 0.0


def check_consensus(results: List[str], threshold: float = 0.6) -> bool:
    """Check if there's consensus among agent outputs (simplified)."""
    if len(results) < 2:
        return True
    
    # Simple consensus check based on content length consistency
    lengths = [len(r.strip()) for r in results if r]
    if not lengths:
        return False
    
    avg_length = sum(lengths) / len(lengths)
    consistency = sum(1 for l in lengths if abs(l - avg_length) / avg_length < 0.5) / len(lengths)
    
    return consistency >= threshold


def run_lifecycle_workflow(requirements_path: Path, pid_path: Path, overwrite: bool, 
                          demo: bool = False, model: str = 'gpt-4o') -> str:
    """Run the 7-phase product refinement lifecycle workflow."""
    load_environment()
    
    # Read PID content
    try:
        pid_content = pid_path.read_text(encoding='utf-8')
    except Exception:
        pid_content = "# Product Initiative Document\n\n*No existing content found*"
    
    # Create lifecycle context
    context = LifecycleContext(
        requirements_path=requirements_path,
        pid_path=pid_path,
        original_pid_content=pid_content,
        model=model
    )
    
    # Create and run lifecycle controller
    controller = ProductLifecycleController(context, demo=demo)
    return controller.execute_lifecycle()


def run_delegation_workflow(requirements_path: Path, pid_path: Path, overwrite: bool, 
                           demo: bool = False, model: str = 'gpt-4o') -> str:
    """Run the delegation-based workflow where Product Manager orchestrates all other agents."""
    load_environment()
    
    if demo:
        demo_section_separator("PRODUCT CREW DELEGATION WORKFLOW")
        click.echo(f"{click.style('🎯 Starting Delegation-Based Product Crew Analysis', fg='bright_green', bold=True)}")
        click.echo(f"{click.style('Orchestrator:', fg='cyan')} Product Manager")
        click.echo(f"{click.style('Specialists:', fg='cyan')} Market Analyst, Engineering Manager, Product Designer, Functional Analyst, Scrum Master")
        demo_pause("Delegation workflow initialized", "Starting delegation orchestration")
    
    # Create the delegation task and all agents
    delegation_task = create_delegation_workflow_task(requirements_path, pid_path, model)
    all_agents = create_delegation_crew_agents(model)
    
    if demo:
        demo_section_separator("DELEGATION ORCHESTRATION")
        click.echo(f"\n{click.style('🎭 DELEGATION WORKFLOW', fg='yellow', bold=True)}")
        click.echo(f"{click.style('Product Manager will delegate to:', fg='cyan')}")
        for agent in all_agents[1:]:  # Skip the Product Manager (first agent)
            click.echo(f"  • {agent.role}")
        demo_pause("All agents ready for delegation", "Starting orchestrated execution")
    
    # Create and run the crew with delegation
    delegation_crew = Crew(
        agents=all_agents,
        tasks=[delegation_task],
        verbose=demo
    )
    
    delegation_start = time.time()
    delegation_results = delegation_crew.kickoff()
    delegation_time = time.time() - delegation_start
    
    if demo:
        demo_section_separator("DELEGATION COMPLETION")
        click.echo(f"{click.style('✅ Delegation Workflow Complete!', fg='bright_green', bold=True)}")
        click.echo(f"{click.style('Execution Time:', fg='cyan')} {delegation_time:.1f}s")
        click.echo(f"{click.style('Orchestrator:', fg='cyan')} Product Manager successfully coordinated all specialists")
        demo_pause("Comprehensive PID created through delegation", "Workflow completion")
    
    return str(delegation_results)


def run_collaborative_workflow(requirements_path: Path, pid_path: Path, overwrite: bool, 
                              demo: bool = False, model: str = 'gpt-4o') -> str:
    """Run the full collaborative product crew workflow."""
    load_environment()
    
    max_iterations = 5
    current_iteration = 1
    quality_threshold = 7.0
    all_results = []
    
    if demo:
        demo_section_separator("PRODUCT CREW COLLABORATIVE WORKFLOW")
        click.echo(f"{click.style('🚀 Starting Product Crew Analysis', fg='bright_green', bold=True)}")
        click.echo(f"{click.style('Max Iterations:', fg='cyan')} {max_iterations}")
        click.echo(f"{click.style('Quality Threshold:', fg='cyan')} {quality_threshold}/10")
        demo_pause("Workflow initialized", f"Starting Iteration 1/{max_iterations}")
    
    while current_iteration <= max_iterations:
        if demo:
            demo_section_separator(f"ITERATION {current_iteration}")
            click.echo(f"{click.style(f'🔄 Iteration {current_iteration}/{max_iterations}', fg='bright_blue', bold=True)}")
            demo_pause("Starting iteration phases", f"Iteration {current_iteration} - Phase 1/4")
        
        # Phase 1: Discovery (Product Manager + Market Analyst)
        if demo:
            click.echo(f"\n{click.style('📊 DISCOVERY PHASE', fg='yellow', bold=True)}")
        
        discovery_tasks = create_discovery_phase_tasks(requirements_path, pid_path, model)
        discovery_crew = Crew(
            agents=[task.agent for task in discovery_tasks],
            tasks=discovery_tasks,
            verbose=demo
        )
        
        discovery_start = time.time()
        discovery_results = discovery_crew.kickoff()
        discovery_time = time.time() - discovery_start
        
        if demo:
            click.echo(f"{click.style('✅ Discovery Phase Complete', fg='green')} ({discovery_time:.1f}s)")
            demo_pause("Discovery insights generated", f"Iteration {current_iteration} - Phase 2/4")
        
        # Phase 2: Solution Design (Engineering Manager + Product Designer)
        if demo:
            click.echo(f"\n{click.style('🏗️ SOLUTION DESIGN PHASE', fg='yellow', bold=True)}")
        
        solution_tasks = create_solution_design_phase_tasks(str(discovery_results), model)
        solution_crew = Crew(
            agents=[task.agent for task in solution_tasks],
            tasks=solution_tasks,
            verbose=demo
        )
        
        solution_start = time.time()
        solution_results = solution_crew.kickoff()
        solution_time = time.time() - solution_start
        
        if demo:
            click.echo(f"{click.style('✅ Solution Design Complete', fg='green')} ({solution_time:.1f}s)")
            demo_pause("Technical and UX strategy defined", f"Iteration {current_iteration} - Phase 3/4")
        
        # Phase 3: Breakdown (Functional Analyst + Scrum Master)
        if demo:
            click.echo(f"\n{click.style('📋 BREAKDOWN PHASE', fg='yellow', bold=True)}")
        
        breakdown_tasks = create_breakdown_phase_tasks(str(solution_results), model)
        breakdown_crew = Crew(
            agents=[task.agent for task in breakdown_tasks],
            tasks=breakdown_tasks,
            verbose=demo
        )
        
        breakdown_start = time.time()
        breakdown_results = breakdown_crew.kickoff()
        breakdown_time = time.time() - breakdown_start
        
        if demo:
            click.echo(f"{click.style('✅ Breakdown Phase Complete', fg='green')} ({breakdown_time:.1f}s)")
            demo_pause("Requirements and delivery plan ready", f"Iteration {current_iteration} - Phase 4/4")
        
        # Phase 4: Integration and Quality Assessment
        if demo:
            click.echo(f"\n{click.style('🔗 INTEGRATION PHASE', fg='yellow', bold=True)}")
        
        phase_results = [str(discovery_results), str(solution_results), str(breakdown_results)]
        combined_results = "\n\n".join(phase_results)
        
        integration_task = create_integration_task(combined_results, requirements_path, pid_path, model)
        integration_crew = Crew(
            agents=[integration_task.agent],
            tasks=[integration_task],
            verbose=demo
        )
        
        integration_start = time.time()
        integration_results = integration_crew.kickoff()
        integration_time = time.time() - integration_start
        
        all_results.extend(phase_results)
        all_results.append(str(integration_results))
        
        # Calculate quality metrics
        quality_score = calculate_quality_score(all_results)
        consensus = check_consensus(phase_results)
        
        if demo:
            click.echo(f"{click.style('✅ Integration Complete', fg='green')} ({integration_time:.1f}s)")
            click.echo(f"\n{click.style('📈 QUALITY METRICS', fg='bright_blue', bold=True)}")
            click.echo(f"{click.style('Quality Score:', fg='cyan')} {quality_score:.1f}/10")
            click.echo(f"{click.style('Consensus:', fg='cyan')} {'✅ Achieved' if consensus else '❌ Not achieved'}")
            
            total_time = discovery_time + solution_time + breakdown_time + integration_time
            click.echo(f"{click.style('Total Time:', fg='cyan')} {total_time:.1f}s")
        
        # Check exit criteria
        if quality_score >= quality_threshold:
            if demo:
                click.echo(f"\n{click.style('🎯 Quality threshold achieved!', fg='bright_green', bold=True)}")
            break
        elif consensus and current_iteration >= 2:
            if demo:
                click.echo(f"\n{click.style('🤝 Consensus achieved with acceptable quality', fg='bright_green', bold=True)}")
            break
        elif current_iteration >= max_iterations:
            if demo:
                click.echo(f"\n{click.style('⏱️ Maximum iterations reached', fg='yellow', bold=True)}")
            break
        
        current_iteration += 1
        
        if demo and current_iteration <= max_iterations:
            demo_pause(f"Iteration {current_iteration-1} complete. Quality: {quality_score:.1f}/10", 
                      f"Preparing Iteration {current_iteration}/{max_iterations}")
    
    final_result = str(integration_results) if 'integration_results' in locals() else "\n\n".join(all_results)
    
    if demo:
        demo_section_separator("WORKFLOW COMPLETION")
        click.echo(f"{click.style('🏁 Workflow Complete!', fg='bright_green', bold=True)}")
        click.echo(f"{click.style('Total Iterations:', fg='cyan')} {current_iteration}")
        click.echo(f"{click.style('Final Quality Score:', fg='cyan')} {quality_score:.1f}/10")
    
    return final_result


def run_crew(requirements_path: Path, pid_path: Path, overwrite: bool, demo: bool = False, model: str = 'gpt-4o') -> None:
    """Run CrewAI crew to process PID file and create enhanced output."""
    try:
        # Determine output file path
        output_path = get_output_file_path(pid_path, overwrite)
        
        if demo:
            demo_section_separator("INITIALIZATION")
            click.echo(f"\n{click.style('🎯 EXECUTION PARAMETERS', fg='green', bold=True)}")
            click.echo(f"{click.style('Requirements Path:', fg='cyan')} {requirements_path}")
            click.echo(f"{click.style('Input PID File:', fg='cyan')} {pid_path}")
            click.echo(f"{click.style('Output File:', fg='cyan')} {output_path}")
            click.echo(f"{click.style('Overwrite Mode:', fg='cyan')} {overwrite}")
            click.echo(f"{click.style('Model:', fg='cyan')} {model}")
            demo_pause("Configuration validated", "Starting collaborative workflow")
        
        # Run the 7-phase lifecycle workflow
        enhanced_content = run_lifecycle_workflow(requirements_path, pid_path, overwrite, demo, model)
        
        if demo:
            demo_section_separator("OUTPUT GENERATION")
            click.echo(f"\n{click.style('📝 FILE PROCESSING', fg='bright_green', bold=True)}")
            click.echo(f"{click.style('Creating enhanced PID file:', fg='cyan')} {output_path}")
        
        # Create the output file with enhanced content
        create_pid_file(output_path, enhanced_content)

        if demo:
            click.echo(f"{click.style('✅ Enhanced PID file created successfully!', fg='bright_green', bold=True)}")
            demo_pause("Product crew execution completed successfully!", "Completion")

        # Print the expected output format for compatibility
        print(str(requirements_path))
        print(str(pid_path))
        print(overwrite)

    except Exception as e:
        if demo:
            demo_section_separator("ERROR HANDLING")
            click.echo(f"\n{click.style('❌ ERROR ENCOUNTERED', fg='red', bold=True)}")
            click.echo(f"{click.style('Error Details:', fg='red')} {str(e)}")
            click.echo(f"{click.style('Fallback:', fg='yellow')} Using legacy mode")
            demo_pause("Error handled. Using fallback approach...", "Error Recovery")
        
        click.echo(f"CrewAI execution error: {e}", err=True)
        
        # Fallback to legacy behavior
        try:
            load_environment()
            output_path = get_output_file_path(pid_path, overwrite)
            
            # Read and copy original content as fallback
            with open(pid_path, 'r', encoding='utf-8') as f:
                original_content = f.read()
            create_pid_file(output_path, original_content)
        except Exception as fallback_error:
            click.echo(f"Fallback also failed: {fallback_error}", err=True)
        
        # Always print the expected output format
        print(str(requirements_path))
        print(str(pid_path))
        print(overwrite)