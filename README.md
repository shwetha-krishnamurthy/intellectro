## Intellectro - Simplifying Research Using RAG

#### Try v1.0 here: https://intellectro.streamlit.app/

### Purpose

The main goal of the Research Paper Reading AI is to assist users in understanding research papers, save time on finding relevant papers, and keep track of citations.

### How does this work?

#### Index Creation:
1. Created word embeddings using Eden AI's API of 10 papers from arXiv on 1 topic (LLMs)
2. Built a Pinecone index out of it

Note: I'm on a student budget so I only created embeddings of 10 papers. Ideal case would be storing all of arXiv with constant updates.

#### Querying
1. Whenever someone queries for a topic, this converts that query into an embedding, once again using Eden's API
2. Then it searches the Pinecone index for the best match
3. The best match is then summarized, mainly covering the problem, assumptions, methodology, and the results of the paper

My budget constraints have:
1. Restricted the search space by a lot. See note above.
2. Reduced the context window which makes it hard to track citations on a paper.

I hope to overcome constraints in the future and that I'm able to add all the features described in detail below.

#### TODO
[X]Create embeddings of just the summaries and not the whole paper (Allows for more papers this  way)\
[X]Search on the summaries\
[X]Fetch the best match paper from arXiv\
[X]Summarize it

### Users

- **Noobs**: Individuals new to the field of research or students beginning to explore academic papers.
- **Researchers**: Experienced individuals in academia or industry who regularly engage with research literature.

### Pain Points

#### Noobs

- Difficulty in finding relevant research papers.
- Challenges in understanding the content of the papers.
- Procrastination on reading and understanding citations.

#### Researchers

- Time-consuming process of finding relevant research.
- Slow and meticulous necessity to read every paper and its citations.
- Understanding the inspirations and context behind the research.

### Solution

- **Natural Language Search**: Implement a search feature that allows users to find the most relevant papers using natural language queries.
- **Summarization**: Provide a summarization tool that condenses the paper into a digestible format.
- **Understanding Calibration**: Offer different levels of summarization to cater to various understanding levels, such as a 13-year-old, a university student, or a doctorate in the subject. This feature can be self-calibrated using data from a resume or LinkedIn profile.
- **Citation Summarization**: Summarize the citations within the papers and indicate how the author has utilized them.
- **Inspiration Levels**: Analyze and present the inspiration levels of different citations to understand their impact on the paper.

### Requirements

1. **Natural Language Processing (NLP)**: The AI must be capable of interpreting and processing natural language queries to return relevant search results.
2. **Summarization Algorithms**: Implement algorithms capable of summarizing research papers and citations at varying levels of complexity.
3. **User Profile Integration**: Ability to integrate with professional profiles to calibrate the understanding level required for summarization.
4. **User Interface (UI)**: A user-friendly interface that allows easy navigation and interaction with the AI's features.
5. **Database**: A comprehensive and up-to-date database of research papers from various fields.
6. **Feedback Mechanism**: A system for users to provide feedback on the relevance and quality of search results and summaries.

### Acceptance Criteria

- The AI must accurately interpret natural language search queries.
- Summaries must be coherent, concise, and reflect the key points of the original papers.
- The AI should provide summaries that are appropriate for the calibrated understanding level of the user.
- The system must be able to handle a high volume of queries and summarization requests without significant delays.

### Constraints and Assumptions

- The AI relies on the availability and accessibility of research paper databases.
- Summarization quality is dependent on the clarity and structure of the original papers.
- User engagement may vary based on the effectiveness of the summarization and search features.

Given the constraint of a 3-week timeline, the focus is towards creating a Minimum Viable Product (MVP) that demonstrates the core functionality of the Research Paper Reading AI with simplified features. The MVP will prioritize essential components that provide immediate value to users while laying the groundwork for future enhancements.

### MVP Scope

1. **Basic Natural Language Search**: Implement a simplified version of the search feature that can handle direct queries for research papers without advanced contextual understanding.
2. **Summarization of Papers**: Develop a basic summarization tool that provides a concise overview of research papers, focusing on abstracts and conclusions to save development time.
3. **Manual Calibration of Understanding Levels**: Instead of an automated calibration system, provide users with a simple option to choose their preferred summarization level (basic, intermediate, advanced) without integrating external profiles.
4. **Static Citation Information**: For the MVP, instead of summarizing citations within the papers, provide a list of cited works with links where users can access them if interested.

### Risk Management and Future Considerations

- **Quality and Relevance**: The basic natural language search and summarization may not meet all user expectations. Collect feedback for future improvements.
- **Scalability**: The MVP's simplified features should be designed with scalability in mind to accommodate future enhancements without significant rework.
- **User Engagement**: Engage with early users to understand their needs and how well the MVP addresses them. Use this feedback to prioritize future development.
