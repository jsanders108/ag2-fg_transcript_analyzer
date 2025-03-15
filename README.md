# AG2: Focus Group Transcript Analyzer

## Project Objective
I developed this project to demonstrate the power of the **AG2** framework in assisting market researchers with challenging tasks such as summarizing and analyzing focus group transcripts. By leveraging multiple AI agents working in concert, I showcase how complex analytical tasks can be completed quickly and efficiently.

The primary goals of this project are:
- To automate the process of summarizing focus group transcripts  
- To perform in-depth analysis of the summarized content  
- To generate a comprehensive report with actionable insights  

By achieving these objectives, I illustrate how AG2 can significantly enhance the productivity and effectiveness of market research processes.

---

## Focus Group Background
For this project, I used mock focus group data, simulating real-world market research scenarios for the launch of a new premium product: **white strawberries**. The discussion captures reactions and opinions about the proposed product concepts.

**Focus Group Transcript File:**  
`data/transcripts.md`  

**Focus Group Objectives File:**  
`data/objectives.md`  

These resources simulate the kind of qualitative data that market researchers often need to analyze quickly and effectively.

---

## Focus Group Objectives
The mock focus groups were centered around the following key objectives:

1. **Evaluate Potential Product Names and Marketing Copy**  
   - **"Snowberry Bliss"**  
   - **"Ivory Nectar"**  
   - **"Pearlberry Prime"**  

2. **Improve the "Winning" Concept Based on Participant Feedback**  
   - Gather suggestions to refine the chosen name and copy  
   - Identify additional features or benefits to emphasize  
   - Explore potential modifications to align with consumer expectations  

3. **Assess Willingness to Buy**  
   - Explore interest in white strawberries as a premium offering  
   - Gauge price sensitivity and perceived value  
   - Identify potential barriers to purchase and ways to overcome them  

The transcripts contain participants’ discussions and feedback, simulating data that researchers often analyze with time and resource constraints.

---

## Code Walkthrough
In this project, I utilized **AG2**, showcasing how agents can work together in a sequential workflow. The main components of this implementation are in the `fg_transcript_swarm.py` file.

### 1. Shared Context and Utility Functions
```python
# fg_transcript_swarm.py (excerpt)

shared_context = {
    "fg_transcripts": "",
    "fg_objectives": "",
    "fg_analysis_draft": "",
    "fg_analysis_final": "",
    "fg_report": "",
}
 
def read_data(context_variables: dict) -> SwarmResult:
    """Read the transcripts and objectives files"""
    with open('data/transcripts.md', 'r') as file:
        transcripts = file.read()
    context_variables['fg_transcripts'] = transcripts
    
    with open('data/objectives.md', 'r') as file:
        objectives = file.read()
    context_variables['fg_objectives'] = objectives
 
    return SwarmResult(
        context_variables=context_variables,
        values=f"Read transcripts and objectives."
    )
```

###2. Defining and Recording Outputs
python
Copy
Edit
def record_analysis_draft(transcript_analysis_draft: str, context_variables: dict) -> SwarmResult:
    context_variables['fg_analysis_draft'] = transcript_analysis_draft
    return SwarmResult(
        context_variables=context_variables,
        values="Transcript stored in fg_analysis_draft."
    )

def record_analysis_final(transcript_analysis_final: str, context_variables: dict) -> SwarmResult:
    context_variables['fg_analysis_final'] = transcript_analysis_final
    return SwarmResult(
        context_variables=context_variables,
        values="Transcript stored in fg_analysis_final."
    )

def record_report(report: str, context_variables: dict) -> SwarmResult:
    context_variables['fg_report'] = report
    return SwarmResult(
        context_variables=context_variables,
        values="Report stored in fg_report."
    )
3. Accessors and File Output
```python

def get_transcripts(context_variables: dict) -> str:
    return context_variables.get('fg_transcripts', '')

def get_analysis_draft(context_variables: dict) -> str:
    return context_variables.get('fg_analysis_draft', '')

def get_analysis_final(context_variables: dict) -> str:
    return context_variables.get('fg_analysis_final', '')

def get_objectives(context_variables: dict) -> str:
    return context_variables.get('fg_objectives', '')

def write_report_to_file(report: str, filename: str) -> SwarmResult:
    # Writes the final report to a markdown file under 'reports' folder
```

4. Agent Definition and Handoff
python
Copy
Edit
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
5. Execution Flow
python
Copy
Edit
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

chat_result, context_variables, last_agent = initiate_swarm_chat(
    initial_agent=ingestion_agent,
    agents=[ingestion_agent, analyzer_agent, quality_control_agent, report_writer_agent],
    messages="start",
    context_variables=shared_context,
    after_work=AfterWork(AfterWorkOption.TERMINATE),
)
Output Showcase
markdown
Copy
Edit
# White Strawberry Product Launch - Focus Group Report

## 1. Executive Summary
The focus group analysis indicates a strong preference for the "Snowberry Bliss" concept among participants, appreciated for its catchy and enticing name. Key inquiries centered around the justification for a premium price, with visual appeal and versatility being major purchasing factors.

## 3. Key Findings
### Preferred Concept: Snowberry Bliss
- Universally well-received for its catchy name and appealing description.
- Significant curiosity about its unique flavor profile and application possibilities.

### Skepticism on Premium Pricing
- Questions arose concerning the unique value proposition and price justification.
- Doubts related to the perceived uniqueness in taste compared to traditional strawberries.

### Importance of Visual and Culinary Versatility
- Participants valued the potential to use white strawberries in various culinary settings, enhancing both visual and taste experiences.

## 6. Recommendations
- Enhance storytelling in marketing, focusing on cultivation methods and usage ideas.
- Develop smaller package sizes to encourage trial without significant investment.
- Collaborate with chefs and influencers to diversify usage demonstrations, catering to premium market expectations.

## 7. Conclusions
"Snowberry Bliss" offers a strong market entry, provided it addresses flavor differentiation and premium pricing concerns. Visual appeal and culinary versatility will be key in positioning the product as a luxury item.


## Conclusion
Through this project, I’ve demonstrated how AG2 can be leveraged to automate and enhance market research processes. By dividing the tasks among specialized agents—ingestion, analysis, quality control, and report writing—researchers can rapidly transform raw transcript data into meaningful reports and strategies.

The modular nature of AG2 allows for easy adaptation to various research contexts, making it a valuable tool for any organization looking to gain deeper insights from qualitative data more efficiently.
