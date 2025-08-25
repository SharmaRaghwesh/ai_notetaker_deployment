import google.generativeai as genai

PROMPTS = {
            "minimal": """Transcribe the meeting audio word-for-word.  
        Then summarize it into clear, well-structured meeting notes.  
        Include:
        - Key discussion points
        - Decisions made
        - Action items with assignee (if mentioned) and deadlines (if any).
        """,

            "business": """First, transcribe the audio accurately.  
        Then provide a structured summary in this format:

        📌 **Meeting Summary**
        - Purpose
        - Key Topics Discussed
        - Major Decisions

        ✅ **Action Items**
        - [Task] → [Person Responsible], [Deadline if mentioned]

        💡 **Follow-ups Needed**
        - List unclear points or open questions

        Keep the notes concise, professional, and easy to scan.
        """,

            "advanced": """You are an AI meeting assistant.

        1. Transcribe the entire meeting audio accurately.  
        2. Then summarize it into structured notes with these sections:
        - **Participants** (if mentioned)  
        - **Agenda / Purpose**  
        - **Key Discussion Points** (grouped by topic)  
        - **Decisions Made**  
        - **Action Items** (Task → Assignee → Deadline)  
        - **Risks / Concerns Raised**  
        - **Next Steps**

        Format in Markdown with bullet points and bold headings.
        """
        }

def transcribe_and_summarize(audio_file,api_key, style="business"):      
    genai.configure(api_key=api_key)
    model = genai.GenerativeModel("gemini-1.5-flash")
    prompt = PROMPTS[style]

    response = model.generate_content([
        {"mime_type": "audio/wav", "data": open(audio_file, "rb").read()},
        prompt
    ])
    return response.text
