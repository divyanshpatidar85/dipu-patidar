def make_prompt(role="employee", length="short"):
    role_map = {
        "employee": "You are an HR policy assistant answering for an internal employee. Be factual and cite pages.",
        "client": "You are a client-facing support assistant. Provide a concise, professional answer; do not expose internal-only sections."
    }
    length_map = {
        "short": "Answer in 2-3 short bullet points.",
        "medium": "Answer in 4-6 sentences with a short explanation.",
        "long": "Provide a detailed explanation and suggest next steps if any."
    }
    return role_map.get(role, role_map["employee"]) + " " + length_map.get(length, length_map["short"])
