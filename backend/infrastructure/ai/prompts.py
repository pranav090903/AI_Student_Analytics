from langchain_core.prompts import ChatPromptTemplate

student_prompt = ChatPromptTemplate.from_template("""
You are Academic AI Copilot.

Student Data:
Prediction: {prediction}
Attendance: {attendance}
Quiz: {quiz}
Assignment: {assignment}
Midterm: {midterm}

Student Question:
{message}

Give personalized academic advice.

Return ONLY valid JSON.

{format_instructions}
""")


teacher_prompt = ChatPromptTemplate.from_template("""
You are an academic performance analyst AI.

Student Risk Prediction: {prediction}
Confidence Score: {confidence}
Student Data: {features}

Return ONLY valid JSON.

{format_instructions}
""")



admin_prompt = ChatPromptTemplate.from_template("""
You are an institutional academic analyst AI.

Student Risk Prediction: {prediction}
Confidence Score: {confidence}
Student Data: {features}

Return ONLY valid JSON.

{format_instructions}
""")


teacher_chat_prompt = ChatPromptTemplate.from_template("""
You are a helpful academic assistant for teachers.
You provide detailed academic advice and guidance.

If student data is provided below, use it to answer the teacher's question about that specific student. The student's ID or Name might be mentioned in the question.

Student Data Context:
{student_context}

Teacher Question:
{message}

Answer:
""")
