from services.tutoring.mcq_service import (
    generate_mcqs
)

response = generate_mcqs(
    topic="Lipids",
    difficulty="advanced"
)

print("\n--- GENERATED MCQS ---\n")

print(response["mcqs"])

