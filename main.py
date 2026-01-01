#!/usr/bin/env python3
"""
Autonomous Corporate Strategy Engine
Author: Pranay M.

AI that analyzes market conditions, predicts competitor moves,
and generates comprehensive business strategies.
"""

import ollama
from rich.console import Console
from rich.panel import Panel
from rich.table import Table
from rich.markdown import Markdown
from rich.prompt import Prompt
import json
import sys

console = Console()

BANNER = """
╔═══════════════════════════════════════════════════════════════════════════════╗
║              🏢 AUTONOMOUS CORPORATE STRATEGY ENGINE 🏢                        ║
║                    AI-Powered Strategic Intelligence                           ║
║                           Author: Pranay M.                                    ║
╚═══════════════════════════════════════════════════════════════════════════════╝
"""

MODULES = {
    "1": ("Market Analyzer", "market_analyze", "Analyze market conditions and trends"),
    "2": ("Competitor Intelligence", "competitor_intel", "Analyze competitor strategies"),
    "3": ("SWOT Generator", "swot_gen", "Generate comprehensive SWOT analysis"),
    "4": ("Strategy Formulator", "strategy_form", "Formulate business strategies"),
    "5": ("Scenario Planner", "scenario_plan", "Plan strategic scenarios"),
    "6": ("M&A Evaluator", "ma_eval", "Evaluate M&A opportunities"),
    "7": ("Innovation Advisor", "innovation", "Advise on innovation strategy"),
    "8": ("Risk Strategist", "risk_strategy", "Develop strategic risk management"),
    "9": ("Execution Planner", "execution", "Plan strategy execution"),
    "10": ("Performance Tracker", "performance", "Track strategic performance")
}

SYSTEM_PROMPTS = {
    "market_analyze": """You are an expert strategic market analyst.

For each market analysis, provide:

1. **Market Overview**: Size, growth, segmentation, key players, trends
2. **Industry Dynamics**: Porter's forces, value chain, profit pools, disruption
3. **Customer Analysis**: Segments, needs, behavior, willingness to pay
4. **Trend Analysis**: Macro trends, technology shifts, regulatory changes
5. **Opportunity Assessment**: Growth opportunities, white spaces, timing
6. **Strategic Implications**: Positioning options, investment priorities, risks

Analyze market conditions for strategic decision-making.""",

    "competitor_intel": """You are an expert competitive intelligence analyst.

For each competitor analysis, evaluate:

1. **Competitor Profiles**: Key competitors, business models, market positions
2. **Strategy Analysis**: Stated strategies, revealed strategies, capabilities
3. **Move Prediction**: Likely moves, signaling, response patterns
4. **Competitive Advantage**: Sources, sustainability, vulnerabilities
5. **Benchmarking**: Performance comparison, best practices, gaps
6. **Strategic Response**: Counter-strategies, differentiation, positioning

Predict competitor moves and inform competitive strategy.""",

    "swot_gen": """You are an expert in strategic analysis frameworks.

For each SWOT analysis, provide:

1. **Strengths**: Internal advantages, capabilities, resources, brand
2. **Weaknesses**: Internal limitations, gaps, vulnerabilities
3. **Opportunities**: External favorable conditions, trends, openings
4. **Threats**: External challenges, competitive threats, risks
5. **Cross-Analysis**: SO strategies, WO strategies, ST strategies, WT strategies
6. **Priority Actions**: Key strategic imperatives, sequencing, resources

Generate comprehensive SWOT with strategic implications.""",

    "strategy_form": """You are an expert corporate strategist.

For each strategy formulation, develop:

1. **Strategic Vision**: Long-term aspiration, competitive position target
2. **Strategic Options**: Alternative strategies, evaluation criteria
3. **Chosen Strategy**: Recommended approach, rationale, differentiators
4. **Business Model**: Value proposition, revenue model, cost structure
5. **Competitive Strategy**: How to win, sustainable advantage sources
6. **Implementation Roadmap**: Phases, milestones, resource requirements

Formulate winning business strategies.""",

    "scenario_plan": """You are an expert in strategic scenario planning.

For each scenario planning exercise, provide:

1. **Driving Forces**: Key uncertainties, impact factors, trends
2. **Scenario Construction**: 3-4 distinct futures, narratives, implications
3. **Strategy Testing**: How strategies perform across scenarios
4. **Robust Strategies**: Elements that work in multiple futures
5. **Early Signals**: Indicators of which scenario is emerging
6. **Contingency Plans**: Pivot strategies, trigger points, options

Develop strategic scenarios for robust planning.""",

    "ma_eval": """You are an expert in M&A strategy and valuation.

For each M&A evaluation, assess:

1. **Strategic Rationale**: Fit, synergies, strategic value creation
2. **Target Assessment**: Business quality, competitive position, risks
3. **Synergy Analysis**: Revenue synergies, cost synergies, timing
4. **Valuation Framework**: Valuation approaches, key assumptions
5. **Integration Planning**: Integration approach, risks, success factors
6. **Deal Recommendation**: Go/no-go, deal structure, price guidance

Evaluate M&A opportunities strategically.""",

    "innovation": """You are an expert innovation strategist.

For each innovation strategy request, provide:

1. **Innovation Landscape**: Technology trends, disruption threats, opportunities
2. **Portfolio Strategy**: Core, adjacent, transformational balance
3. **Build-Buy-Partner**: Make vs. buy decisions, partnership opportunities
4. **Innovation Process**: Ideation, validation, scaling approaches
5. **Resource Allocation**: Investment levels, capability building
6. **Culture & Organization**: Innovation enablers, metrics, governance

Advise on innovation strategy and execution.""",

    "risk_strategy": """You are an expert in strategic risk management.

For each strategic risk assessment, analyze:

1. **Risk Identification**: Strategic risks, competitive risks, disruption risks
2. **Risk Assessment**: Probability, impact, velocity, interconnections
3. **Risk Appetite**: Acceptable levels, strategic risk-taking, limits
4. **Mitigation Strategies**: Risk reduction, transfer, acceptance plans
5. **Opportunity Risks**: Upside risks, strategic bets, optionality
6. **Monitoring System**: Key risk indicators, escalation, governance

Develop strategic risk management frameworks.""",

    "execution": """You are an expert in strategy execution and implementation.

For each execution plan, develop:

1. **Strategic Initiatives**: Key programs, prioritization, sequencing
2. **Resource Allocation**: Capital, talent, focus, trade-offs
3. **Organization Alignment**: Structure, capabilities, culture changes
4. **Performance Management**: Metrics, targets, accountability
5. **Change Management**: Stakeholder engagement, communication, adoption
6. **Governance**: Decision rights, review cadence, course correction

Plan effective strategy execution.""",

    "performance": """You are an expert in strategic performance management.

For each performance tracking request, provide:

1. **Strategic Metrics**: KPIs, leading indicators, balanced scorecard
2. **Performance Analysis**: Results vs. targets, trend analysis, root causes
3. **Competitive Position**: Market share, relative performance, gaps
4. **Strategic Health**: Initiative progress, capability building, culture
5. **Adjustment Recommendations**: Course corrections, resource reallocation
6. **Forward Outlook**: Projections, risks to watch, opportunities

Track and analyze strategic performance."""
}

def get_multiline_input(prompt_text):
    console.print(f"\n[cyan]{prompt_text}[/cyan]")
    console.print("[dim](Type 'END' on a new line when finished)[/dim]\n")
    lines = []
    while True:
        try:
            line = input()
            if line.strip().upper() == 'END':
                break
            lines.append(line)
        except EOFError:
            break
    return '\n'.join(lines)

def query_llama(system_prompt, user_input):
    try:
        response = ollama.chat(model='llama3.2', messages=[
            {'role': 'system', 'content': system_prompt},
            {'role': 'user', 'content': user_input}
        ])
        return response['message']['content']
    except Exception as e:
        return f"Error: {str(e)}\n\nMake sure Ollama is running."

def display_menu():
    console.print(BANNER, style="bold blue")
    table = Table(title="🏢 Strategy Modules", show_header=True, header_style="bold magenta")
    table.add_column("Option", style="cyan", width=8)
    table.add_column("Module", style="green", width=28)
    table.add_column("Description", style="white", width=42)
    for key, (name, _, desc) in MODULES.items():
        table.add_row(key, name, desc)
    table.add_row("0", "Exit", "Exit the application")
    console.print(table)

def run_module(module_key):
    name, key, desc = MODULES[module_key]
    console.print(Panel(f"🏢 {name}", style="bold green"))
    user_input = get_multiline_input(f"Describe your {name.lower()} request:")
    with console.status(f"[bold green]Processing {name}..."):
        response = query_llama(SYSTEM_PROMPTS[key], user_input)
    console.print(Panel(Markdown(response), title=f"🏢 {name} Results", border_style="green"))

def main():
    while True:
        display_menu()
        choice = Prompt.ask("\nSelect a module", choices=["0","1","2","3","4","5","6","7","8","9","10"])
        if choice == "0":
            console.print("\n[yellow]Thank you for using the Corporate Strategy Engine![/yellow]")
            console.print("[dim]Author: Pranay M.[/dim]\n")
            break
        try:
            run_module(choice)
        except KeyboardInterrupt:
            console.print("\n[yellow]Operation cancelled.[/yellow]")
        except Exception as e:
            console.print(f"\n[red]Error: {str(e)}[/red]")
        input("\nPress Enter to continue...")

if __name__ == "__main__":
    main()
