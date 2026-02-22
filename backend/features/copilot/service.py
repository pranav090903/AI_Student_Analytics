
from infrastructure.ai.chains import student_chain, teacher_chain, teacher_chat_chain
from infrastructure.database import student_records_collection


def student_copilot_chat(student_data, prediction, confidence, question):
    """
    Handles Student Chat where data is provided manually (e.g. from sliders)
    """
    response = student_chain.invoke({
        "message": question,
        "attendance": student_data.get("attendance_percentage", 0),
        "quiz": student_data.get("quiz_avg", 0),
        "assignment": student_data.get("assignment_avg", 0),
        "midterm": student_data.get("midterm_score", 0),
        "prediction": prediction
    })
    
    if isinstance(response, dict):
        return response.get("content", response)
    return response


def teacher_copilot_chat(message, username):
    """
    Handles Teacher Chat where data is retrieved from the database
    """
    # ---------------- CONTEXT RETRIEVAL ----------------
    student_context = "No specific student data found."
    
    message_lower = message.lower()
    class_keywords = ["all students", "entire class", "everyone", "weakest", "best", "comparison", "compare", "class performance"]
    
    is_class_query = any(k in message_lower for k in class_keywords)
    
    if is_class_query:
        # FETCH ALL STUDENTS
        all_students = list(student_records_collection.find({}, {"_id": 0}))
        if all_students:
             student_context = "Here is the data for ALL students in the class:\n" + "\n\n".join([str(s) for s in all_students])
    
    else:
        # CHECK FOR SPECIFIC STUDENTS
        all_students_meta = list(student_records_collection.find({}, {"student_id": 1, "_id": 0}))
        
        found_students = []
        for stu in all_students_meta:
            s_id = stu.get("student_id")
            if s_id and s_id in message:
                full_record = student_records_collection.find_one(
                    {"student_id": s_id}, 
                    {"_id": 0}
                )
                if full_record:
                    found_students.append(str(full_record))

        if found_students:
            student_context = "\n\n".join(found_students)

    # ---------------- GENERATE RESPONSE ----------------
    response = teacher_chat_chain.invoke({
        "message": message,
        "student_context": student_context
    })

    return response
