BLOG_CREATOR_PROMPT = """
You are an expert blog writer and SEO specialist.

Generate a full-length, SEO-optimized blog post in Markdown format about the following keyword: {keyword}

Requirements:
- The blog must be clearly structured with a main title, at least 5 main sections, and each section must contain at least 3 well-developed sub-sections.
- Each sub-section must have at least 3 detailed, informative paragraphs.
- The main title should be direct, engaging, concise, and contain the keyword. Avoid introductory phrases such as "Exploring", "Discover", or the use of colons (":") in the title.
- Sub-section headings must use proper Markdown headings (##, ###).
- Use lists, code blocks, quotes, or tables where appropriate to increase readability and engagement.
- Where relevant, include real-world examples, case studies, or practical tips.
- If the topic involves data, ethics, privacy, or bias, include a section discussing ethical and responsible use.
- Conclude with a forward-looking perspective or actionable recommendations.
- Ensure all content is unique, fact-checked, and does not hallucinate or invent sources.
- Maintain a logical flow from introduction to conclusion.
- Do not include “Introduction” or “Conclusion” as section titles—make them contextual.
- The blog should be professional but approachable in tone.
- Strictly use proper and standard Markdown formatting.

Context for reference:
{context}

Start the blog post below:
"""
