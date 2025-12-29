def build_prompt(query, docs):
    context = "\n\n".join([
        f"""
        Job Title: {d['title']}
        Company: {d['company']}
        Location: {d['location']}
        Level: {d['level']}
        Category: {d['category']}
        """
        for d in docs
    ])

    return f"""
    You are an intelligent job search assistant.

    User Query:
    {query}

    Based ONLY on the job listings below, return the most relevant jobs.
    Use bullet points.

    Job Listings:
    {context}
    """
