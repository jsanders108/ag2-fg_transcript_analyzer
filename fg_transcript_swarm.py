from autogen import (
    AfterWork,
    ConversableAgent,
    AfterWorkOption,
    SwarmResult,
    initiate_swarm_chat,
    register_hand_off,
)

import os

from utils import get_openai_api_key
OPENAI_API_KEY = get_openai_api_key()
llm_config = {"api_type": "openai", "model": "gpt-4o"}


# Context: Shared state among agents
shared_context = {
    "fg_transcripts": "",
    "fg_objectives": "",
    "fg_analysis_draft": "",
    "fg_analysis_final": "",
    "fg_report": "",
}
 
# Function to read Transcripts and Objectives
def read_data(context_variables: dict) -> SwarmResult:
    """Read the transcripts and objectives files"""
    # Read transcripts
    with open('data/transcripts.md', 'r') as file:
        transcripts = file.read()
    context_variables['fg_transcripts'] = transcripts
    
    # Read objectives
    with open('data/objectives.md', 'r') as file:
        objectives = file.read()
    context_variables['fg_objectives'] = objectives
 
    return SwarmResult(
        context_variables=context_variables,
        values=f"Read transcripts and objectives.",
    )

# Functions to store intermediate and final analysis reports.
def record_analysis_draft(transcript_analysis_draft: str, context_variables: dict) -> SwarmResult:
    """
    Record the transcript analysis draft.
    """
    context_variables['fg_analysis_draft'] = transcript_analysis_draft
    
    return SwarmResult(
        context_variables=context_variables,
        values="Transcript stored in fg_analysis_draft."
    )


def record_analysis_final(transcript_analysis_final: str, context_variables: dict) -> SwarmResult:
    """
    Record the transcript analysis final.
    """
    context_variables['fg_analysis_final'] = transcript_analysis_final
    
    return SwarmResult(
        context_variables=context_variables,
        values="Transcript stored in fg_analysis_final."
    )


def record_report(report: str, context_variables: dict) -> SwarmResult:
    """
    Record the report.
    """
    context_variables['fg_report'] = report
    
    return SwarmResult(
        context_variables=context_variables,
        values="Report stored in fg_report."
    )


# Utility functions to retrieve stored data.
def get_transcripts(context_variables: dict) -> str:
    return context_variables.get('fg_transcripts', '')

def get_analysis_draft(context_variables: dict) -> str:
    return context_variables.get('fg_analysis_draft', '')

def get_analysis_final(context_variables: dict) -> str:
    return context_variables.get('fg_analysis_final', '')

def get_objectives(context_variables: dict) -> str:
    return context_variables.get('fg_objectives', '')


# Function to write the final report to a markdown file.
def write_report_to_file(report: str, filename: str) -> SwarmResult:
    """Write the final report to a markdown file in the 'reports' directory."""
    # Create the 'reports' directory if it doesn't exist
    reports_dir = os.path.join(os.getcwd(), "reports")
    if not os.path.exists(reports_dir):
        os.makedirs(reports_dir)
    
    filepath = os.path.join(reports_dir, filename)
    with open(filepath, 'w') as f:
        f.write(report)
    
    return SwarmResult(
        values=f"Report written to {filepath}",
        context_variables={}
    )

# Messages guiding different agents in their tasks.
analyzer_message = """
   
    Analyze the focus group transcripts. Use the get_transcripts function to access the transcripts. 
    Review the content in the context of the research objectives. Use the get_objectives function to access the objectives.
    Identify key themes, patterns, and insights that emerge from the summary. Pay particular attention 
    to how the discussion points relate to the research objectives.
    
    expected_output: 
    A comprehensive analysis report that includes:
    1. Identified key themes and patterns from the focus group summary
    2. Insights derived from the discussion, especially those relating to the research objectives
    3. Notable trends or unexpected findings
    4. Areas of consensus or disagreement among participants
    5. Potential implications of the findings
    6. Any gaps in the information or areas that may require further investigation
    7. Initial recommendations based on the analysis

    **After completing the analysis, use the "record_analysis_draft" function to record it.**

"""

quality_control_message = """
    Retrieve the full focus group analysis draft using the **get_analysis_draft** function 
    
    Retrieve the research objectives using the **get_objectives** function.
    
    Thoroughly review the entire analysis draft for accuracy, completeness, and consistency with the research objectives. 
    Instead of merely providing feedback, revise and update the complete analysis to address any identified gaps, inconsistencies, 
    or ambiguities.
    
    Ensure your revised analysis includes:
    1. Validation and correction of any errors or oversights from the initial draft.
    2. Integration of any missing insights, themes, or recommendations aligned with the research objectives.
    3. A cohesive and comprehensive narrative that unifies all improvements into a final, polished analysis.
    
    expected_output:
    A final, revised analysis report that:
    1. Clearly validates and enhances the initial analysis.
    2. Identifies and corrects gaps or inconsistencies.
    3. Presents a refined analysis ready to be used for report generation.
    
    **After revising the analysis, use the "record_analysis_final" function to record the updated, complete analysis.**
"""



report_writer_message = """
    Use the get_analysis_final function to access the focus group analysis.
    Use the get_objectives function to access the research objectives.

    Based on the focus group analysis, create a polished, well-structured markdown report that 
    effectively communicates the focus group findings, insights, and recommendations. The report should be 
    tailored for stakeholders and decision-makers, presenting information in a clear, 
    engaging, and actionable format.

    expected_output:
    A final markdown report that includes:
    1. Executive Summary: A brief overview of key findings and recommendations
    2. Introduction: Background on the focus group objectives and methodology
    3. Key Findings: Detailed presentation of main insights, organized by themes
    4. Analysis: In-depth discussion of patterns, trends, and their implications
    5. Participant Quotes: Relevant verbatim quotes to illustrate key points
    6. Recommendations: Actionable suggestions based on the insights
    7. Conclusions: Summary of the most important takeaways
    8. Next Steps: Suggested actions or areas for further research
    9. Appendices: Any additional relevant information

    The report should use markdown formatting for headers, lists, emphasis, and 
    links where appropriate. Ensure the document is well-organized, easy to navigate, 
    and visually appealing within the constraints of markdown.

    **After completing the report:**
    1. Use the **record_report** function to record it.
    2. Use the **write_report_to_file** function to save the report as a markdown file.
       Provide the report content and filename (e.g., 'focus_group_report.md').
"""

# Creating agents to handle different stages of analysis.
ingestion_agent = ConversableAgent(
    name="ingestion_agent",
    llm_config=llm_config,
    system_message="You are a helpful assistant that reads the transcripts and objectives files.",
    functions=[read_data]
)

analyzer_agent = ConversableAgent(
    name="analyzer_agent",
    llm_config=llm_config,
    system_message=analyzer_message,
    functions=[record_analysis_draft, get_transcripts, get_objectives]
)

quality_control_agent = ConversableAgent(
    name="quality_control_agent",
    llm_config=llm_config,
    system_message=quality_control_message,
    functions=[record_analysis_final, get_transcripts, get_objectives, get_analysis_draft]
)


report_writer_agent = ConversableAgent(
    name="report_writer_agent",
    llm_config=llm_config,
    system_message=report_writer_message,
    functions=[record_report, get_analysis_final, write_report_to_file]
)

# Registering handoffs between agents to ensure sequential execution.
register_hand_off(
    agent=ingestion_agent,
    hand_to=[
        AfterWork(analyzer_agent)
    ]
)

register_hand_off(
    agent=analyzer_agent,
    hand_to=[
        AfterWork(quality_control_agent)
    ]
) 

register_hand_off(
    agent=quality_control_agent,
    hand_to=[
        AfterWork(report_writer_agent)
    ]
)

register_hand_off(
    agent=report_writer_agent,
    hand_to=[
        AfterWork(AfterWorkOption.TERMINATE)
    ]
)


# Initiating the swarm chat process with the first agent.
chat_result, context_variables, last_agent = initiate_swarm_chat(
    initial_agent=ingestion_agent,
    agents=[ingestion_agent, analyzer_agent, quality_control_agent, report_writer_agent],
    messages="start",
    context_variables=shared_context,
    after_work=AfterWork(AfterWorkOption.TERMINATE),
)


