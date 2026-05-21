from services.tutoring.tutor_service import (
    generate_tutor_response
)

response = generate_tutor_response(
    "What are phospholipids?"
)

print("\n--- TUTOR RESPONSE ---\n")

print(response["answer"])