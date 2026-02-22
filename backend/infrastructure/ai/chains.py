from langchain_core.output_parsers import JsonOutputParser, StrOutputParser
from infrastructure.ai.llm import chat_model
from infrastructure.ai.prompts import student_prompt, teacher_prompt, admin_prompt, teacher_chat_prompt
from shared.schemas import (
    StudentGenAIOutput,
    TeacherGenAIOutput,
    AdminGenAIOutput
)


# ---------------- STUDENT ----------------
student_parser = JsonOutputParser(pydantic_object=StudentGenAIOutput)

student_chain = (
    student_prompt.partial(
        format_instructions=student_parser.get_format_instructions()
    )
    | chat_model
    | student_parser
)


# ---------------- TEACHER ----------------
teacher_parser = JsonOutputParser(pydantic_object=TeacherGenAIOutput)

teacher_chain = (
    teacher_prompt.partial(
        format_instructions=teacher_parser.get_format_instructions()
    )
    | chat_model
    | teacher_parser
)



# ---------------- ADMIN ----------------
admin_parser = JsonOutputParser(pydantic_object=AdminGenAIOutput)

admin_chain = (
    admin_prompt.partial(
        format_instructions=admin_parser.get_format_instructions()
    )
    | chat_model
    | admin_parser
)


# ---------------- TEACHER CHAT ----------------
teacher_chat_chain = (
    teacher_chat_prompt
    | chat_model
    | StrOutputParser()
)
